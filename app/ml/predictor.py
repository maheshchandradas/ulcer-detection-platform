import torch
from PIL import Image
from torchvision import transforms
from app.ml.model_loader import load_model


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])


def predict_ulcer(image_path):

    model, class_to_index = load_model()

    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():

        outputs = model(image_tensor)

        probs = torch.softmax(outputs, dim=1)

        confidence, predicted = torch.max(probs, 1)

    index_to_class = {v: k for k, v in class_to_index.items()}

    return {
        "prediction": index_to_class[predicted.item()],
        "confidence": float(confidence.item())
    }