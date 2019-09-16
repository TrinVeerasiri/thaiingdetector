from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from base64 import b64encode
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import torch

from .inference import get_prediction


def upload(request):
    context = {}
    if request.method == 'POST':
        #Save upload file to media folder
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)

        #Get to media folder which store the pictures
        media_path = os.getcwd() 
        media_path = os.path.join(media_path, 'media')
        #Join the upload file name to the path
        filename = os.path.join(media_path, name)

        #Prediction
        #Load test image
        with open(filename, 'rb') as f:
            image_bytes = f.read()

        scores, labels, masks = get_prediction(image_bytes)

        # print(scores) # list of float
        # print(labels) # list of string
        # print(masks)  # list of numpy array (height, width) 0.0 -> 1.0

        #Return the result to frontend
        original = b64encode(image_bytes).decode("utf-8")
        context['original'] = original
        context['scores'] = scores
        context['url'] = labels

        #Return mask image
        listOfMasks = {}
        i=0
        for mask in masks: 
            mask = Image.fromarray((mask*255).astype('uint8'), 'P')
            buffer = BytesIO()
            mask.save(buffer,format="PNG")
            buff_image = buffer.getvalue()                     
            mask = b64encode(buff_image).decode("utf-8")
            listOfMasks[labels[i]] = mask
            i=i+1
        context['result'] = listOfMasks
        

    return render(request, 'upload.html', context)
