from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from django.http import HttpResponse
import cv2
import face_recognition
import os
import shutil
import sys

# Create your views here.

# To show the images in which you are present
def home(request):

    # image to compare with
    data1 = SImg.objects.all()
    # images to be compared
    data2 = MulImg.objects.all()

    # To store matched faces pictures
    yourImg=[]

    for f in data1:
        # Project Directory 
        projLocation=os.getcwd()
        imgLn=str(f.image.url).replace('/', '\\')
        # Image location
        imgLocation=projLocation+imgLn

        # Reading an image in default mode
        img = cv2.imread(imgLocation)
        
        # To convert a BGR image to RGB
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # to get the first found face
        img_encoding = face_recognition.face_encodings(rgb_img)[0]


        # to check all the images
        for f in data2:

            imgLn=str(f.images.url).replace('/', '\\')
            # Image location
            imgLocation=projLocation+imgLn
            img2 = cv2.imread(imgLocation)

            image = face_recognition.load_image_file(imgLocation)
            # locations of all faces present in the image
            face_locations = face_recognition.face_locations(image)
            # Number of faces present in the image
            noOfPeople=len(face_locations)
            
            if noOfPeople==0:
                continue

            # To match with every faces in the image
            for i in range(0,noOfPeople):
                rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
                img_encoding2 = face_recognition.face_encodings(rgb_img2)[i]

                # To compare the two faces
                result = face_recognition.compare_faces([img_encoding], img_encoding2)

                # If person is found then add in 'yourImg' list
                if str(result)=='[True]':
                    yourImg.append(f.images)
                    
    context = {
        "data" : yourImg
    }

    return render(request,"home.html",context)

# To upload all the images
def index(request):

    context = {
        "data1":SImg.objects.all(),
        "data2":MulImg.objects.all(),
    }
   
    return render(request, "index.html",context)

# To upload the single image with which you want to compare all the other images
def simgUpload(request):
    if request.method == "POST":
        
        # Get the selected image
        simage=request.FILES.get('simage')

        # if an image is selected
        if str(simage)!='None':
            # if an image is already present then delete it and store the new one
            SImg.objects.all().delete()
            simg=SImg(name='myimg',image=simage)
            simg.save()

        return redirect("index")

# To upload all the images from which you want to find yourself
def mulimgUpload(request):
    if request.method == "POST":
        
        # Get the selected images
        images=request.FILES.getlist('images')
        
        # saving all the selected images
        for f in images:
            mimg = MulImg(name='toCheck', images=f)
            mimg.save()

        return redirect("index")

# To delete all the uploaded images
def deletePics(request):
    if request.method == "POST":
        
        # Deleting media folder
        imageL=os.getcwd()
        imgLoc=str(imageL)+'\\'
        path=os.path.join(imgLoc, "media")

        # Deleting media folder if exists
        if os.path.isdir(path):
            shutil.rmtree(path)

        # Deleting from database
        SImg.objects.all().delete()
        MulImg.objects.all().delete()
   
    return redirect("index")

# To go back from the home page to index page
def gback(request):
    if request.method == "POST":
        return redirect("index")
