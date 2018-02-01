# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from snippets.faceapi import Face
from snippets.faceapi import FaceApi

from PIL import Image
import os




class SnippetsConfig(AppConfig):
    name = 'snippets'
    def ready(self):
        # Singleton utility
        # We load them here to avoid multiple instantiation across other
        # modules, that would take too much time.
        cwd = os.getcwd()
        global faceSvm  
        faceSvm = FaceApi((480,640, 3))
        faces = []
        faces.append(faceSvm.processImg(Image.open(cwd+'/snippets/images/liche1.jpg','r'),1,False,False,(1024,1280, 3)))
        faces.append(faceSvm.processImg(Image.open(cwd+'/snippets/images/liche2.png','r'),1,False,False,(1024,1280, 3)))
        faces.append(faceSvm.processImg(Image.open(cwd+'/snippets/images/liche3.jpg','r'),1,False,False,(1024,1280, 3)) )       
        
        faces.append(faceSvm.processImg(Image.open(cwd+'/snippets/images/jackman1.jpg','r'),0,False,False,(1024,1280, 3)))
        faces.append(faceSvm.processImg(Image.open(cwd+'/snippets/images/jackman2.jpg','r'),0,False,False,(1024,1280, 3)))
        faces.append(faceSvm.processImg(Image.open(cwd+'/snippets/images/jackman3.jpg','r'),0,False,False,(1024,1280, 3)))

        faces.append(faceSvm.processImg(Image.open(cwd+'/snippets/images/obama1.jpg','r'),1,False,False,(1024,1280, 3)))
        faces.append(faceSvm.processImg(Image.open(cwd+'/snippets/images/obama2.jpg','r'),0,False,False,(1024,1280, 3)))
        faces.append(faceSvm.processImg(Image.open(cwd+'/snippets/images/obama3.jpg','r'),0,False,False,(1024,1280, 3)))
        faceSvm.trainSVMwithData(faces)