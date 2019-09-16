import io
import json
import os

from PIL import Image
from torchvision import models
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
import torchvision.transforms as transforms

def load_json(file='categories.json'):
    #Find relative path to 'categories.json'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    with open(filename, 'r') as f:
        data = f.read()
        categories = json.loads(data)
        return categories

def get_model(num_classes):
    # load an instance segmentation model pre-trained on COCO
    model = models.detection.maskrcnn_resnet50_fpn(pretrained_backbone=False)

    # get the number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    
    # now get the number of input features for the mask classifier
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    # and replace the mask predictor with a new one
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
                                                       hidden_layer,
                                                       num_classes)
    
    return model


def transform_image(image_bytes):
    trfs = transforms.Compose([transforms.ToTensor()])
    image = Image.open(io.BytesIO(image_bytes))
    return trfs(image)


def format_label_name(label_name):
    label_name = label_name.replace('_', ' ')
    label_name = label_name.title()
    return label_name