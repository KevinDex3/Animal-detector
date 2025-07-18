import torch
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from PIL import Image
import json
import requests
import cgi
from io import BytesIO

# Carica i pesi e la trasformazione
weights = MobileNet_V2_Weights.IMAGENET1K_V1
model = mobilenet_v2(weights=weights)
model.eval()
transform = weights.transforms()

# Carica le etichette ImageNet
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
LABELS = requests.get(LABELS_URL).text.strip().split("\n")

def handle(event, context):
    try:
        # Converti event.body in bytes se è stringa
        body = event.body
        if isinstance(body, str):
            body = body.encode('utf-8')

        # Prepara le variabili d'ambiente richieste da cgi.FieldStorage
        headers = dict(event.headers)
        content_type = headers.get("content-type") or headers.get("Content-Type", "")
        content_length = str(len(body))

        environ = {
            "REQUEST_METHOD": "POST",
            "CONTENT_TYPE": content_type,
            "CONTENT_LENGTH": content_length
        }

        # Parsing multipart/form-data
        fs = cgi.FieldStorage(
            fp=BytesIO(body),
            environ=environ,
            keep_blank_values=True
        )

        if 'file' not in fs:
            return {
                "statusCode": 400,
                "body": "Errore: nessun file trovato nella richiesta."
            }

        # Estrai il file e prepara il tensor
        file_item = fs['file']
        image = Image.open(file_item.file).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(input_tensor)
            
            # Ottieni i primi 3 risultati (classi e probabilità)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            top3_probs, top3_classes = torch.topk(probabilities, 3)

        # Prepara il risultato per la risposta
        top3_results = []
        for i in range(3):
            class_idx = top3_classes[0][i].item()
            class_name = LABELS[class_idx]
            prob = top3_probs[0][i].item()
            top3_results.append({"class": class_name, "probability": prob})

        return {
            "statusCode": 200,
            "body": json.dumps({"top_3_predictions": top3_results}),
            "headers": {"Content-type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Errore durante l'elaborazione: {str(e)}"
        }

