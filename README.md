# 🐾 Animal Detector (MobileNetV2 + PyTorch)

Questa funzione utilizza **MobileNetV2** pre-addestrato su **ImageNet** per classificare immagini, restituendo le **prime 3 predizioni** con le rispettive probabilità.

## 📦 Funzionalità

- Accetta una richiesta `POST` multipart/form-data con un'immagine (`file`)
- Usa `torchvision.models.mobilenet_v2` con i pesi `IMAGENET1K_V1`
- Restituisce le 3 classi più probabili dell'immagine
- Supporta ambienti serverless (es. AWS Lambda)

## 🧠 Esempio di risposta JSON

```json
{
  "top_3_predictions": [
    {"class": "tabby cat", "probability": 0.92},
    {"class": "tiger cat", "probability": 0.06},
    {"class": "Egyptian cat", "probability": 0.01}
  ]
}

## ⌨️​ Esempio di input

curl -X POST http://INDIRIZZO/function/animal-detector   -H "Content-Type: multipart/form-data"   -F "file=@/home/kevin/Immagini/cane.jpeg"
Occorre prima salvare un'immagine e successivamente specificare il percorso appropriato!

