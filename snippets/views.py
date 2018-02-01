# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FileUploadParser
from snippets.models import FaceData
from snippets.serializers import FaceSerializer
from snippets.apps import faceSvm
from PIL import Image


class faceSeek(APIView):
    parser_classes = (JSONParser,)
    def post(self,request,format = None):    
        f = faceSvm.findIdentity(request.data['images'][0],False,True)  
        return JsonResponse({'id':f})

class faceTrain(APIView):
    parser_classes = (JSONParser,)
    def post(self,request,identity,format = None): 
        f=request.data['vector'];
        faceSvm.trainSVMwithData(f)
        return JsonResponse({'trained':True})
class faceProcess(APIView):
    parser_classes = (JSONParser,)
    def post(self,request,identity,format = None): 
        f=[];
        for img in request.data['images']: 
            f.append(faceSvm.processImg(img,identity,False,True,None))
        return JsonResponse(f)

class svmDump(APIView):
    parser_classes = (JSONParser,)
    def post(self,request,format = None):    
        f=request.data['svmPathAndName'];
        faceSvm.saveSvmToFile(f)
        return JsonResponse({'dumped':True})

class svmLoad(APIView):
    parser_classes = (JSONParser,)
    def post(self,request,identity,format = None): 
        f=request.data['svmPathAndName'];
        faceSvm.loadSvmFromFile(f)
        return JsonResponse({'loaded':True})