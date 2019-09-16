from inference import get_prediction

with open('IMG_5862_cr.jpg', 'rb') as f:
    image_bytes = f.read()

scores, labels, masks = get_prediction(image_bytes)

print(scores) # list of float
print(labels) # list of string
print(masks)  # list of numpy array (height, width) 0.0 -> 1.0