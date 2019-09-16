import os
import torch

from .commons import *


device = torch.device('cpu')
categories = load_json(file='categories.json')
num_classes = len(categories)
threshold = 0.5

#Find relative path to 'model.pt'
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'model.pt')

model = get_model(num_classes)
chekpoint = torch.load(filename, map_location=device.type)
model.load_state_dict(chekpoint['model_state_dict'])
model.to(device)
model.eval()


###
# with open('IMG_5862_cr.jpg', 'rb') as f:
#     image_bytes = f.read()
###

def get_prediction(image_bytes):
    try:
        tensor = transform_image(image_bytes=image_bytes)
        # print(tensor)
        with torch.no_grad():
            prediction = model([tensor.to(device)])[0]
            # print(prediction)
    except Exception:
        return 0, 'error'
    
    idxs = prediction['scores'] > threshold
    scores = prediction['scores'][idxs]
    scores = [score.item() for score in scores]
    labels = prediction['labels'][idxs]
    labels = [format_label_name(categories[str(label.item())]) for label in labels]
    masks = prediction['masks'][idxs]
    masks = [mask.squeeze().numpy() for mask in masks]
    # print(scores)
    # print(labels)
    return scores, labels, masks

###
# if __name__ == '__main__':
#     get_prediction(image_bytes)
###