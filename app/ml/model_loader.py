import torch
from torchvision import models

MODEL_PATH = "app/models/ulcer_classification_mobilenetv3.pth"

model = None
class_to_index = None


def load_model():
    global model, class_to_index

    if model is None:

        checkpoint = torch.load(MODEL_PATH, map_location="cpu")

        # Initialize MobileNetV3 Small
        model = models.mobilenet_v3_small(
            weights=models.MobileNet_V3_Small_Weights.IMAGENET1K_V1
        )

        # Modify classifier layer
        num_ftrs = model.classifier[3].in_features
        model.classifier[3] = torch.nn.Linear(
            num_ftrs,
            len(checkpoint["class_to_index"])
        )

        # Load trained weights
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()

        class_to_index = checkpoint["class_to_index"]

    return model, class_to_index