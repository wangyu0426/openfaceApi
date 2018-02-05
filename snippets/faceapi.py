import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fileDir, "..", ".."))


import argparse
import cv2
import imagehash
import json
from PIL import Image
from PIL import ImageFilter
import numpy as np
import StringIO
import urllib
import base64

from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV
from sklearn.manifold import TSNE
from sklearn.svm import SVC
from sklearn.externals import joblib

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import openface


class Face:

    def __init__(self, rep, identity, phash):
        self.rep = rep
        self.identity = identity
        self.phash = phash

    def __repr__(self):
        return "{{id: {}, rep[0:5]: {}, phash: {}}}".format(
            str(self.identity),
            self.rep[0:5],
            self.phash
        )


class FaceApi:
    def __init__(self,res):
        self.res = res
        self.images = {}
        self.people = []
        self.svm = None
        self.modelDir = os.path.join(fileDir, 'models')
        self.dlibModelDir = os.path.join(self.modelDir, 'dlib')
        self.openfaceModelDir = os.path.join(self.modelDir, 'openface')
        self.align = openface.AlignDlib(os.path.join(self.dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
        self.net = openface.TorchNeuralNet(os.path.join(self.openfaceModelDir, 'nn4.small2.v1.t7'), imgDim=96, cuda='')
        self.count = 1
        self.imgDim = 96
    def increace(self):
        self.count += 1
    def processImg(self,imgData,identity,isStram,isBase64,res):
        #train
        res = res if res is not None else self.res
        if isStram:
            imgF = StringIO.StringIO()
            imgF.write(imgData)
            imgF.seek(0)
            img = Image.open(imgF)
        elif isBase64:
            imgF = StringIO.StringIO()
            imgF.write(base64.b64decode(imgData))
            imgF.seek(0)
            img = Image.open(imgF)
        else:
            img = imgData
        buf = np.fliplr(np.asarray(img))
        #rgbFrame is bit map for every single px
        rgbFrame = np.zeros(res, dtype=np.uint8)
        rgbFrame[:, :, 0] = buf[:, :, 2]
        rgbFrame[:, :, 1] = buf[:, :, 1]
        rgbFrame[:, :, 2] = buf[:, :, 0]
        # bbs = align.getAllFaceBoundingBoxes(rgbFrame)
        bb = self.align.getLargestFaceBoundingBox(rgbFrame)
        bbs = [bb] if bb is not None else []
        for bb in bbs:
            # print(len(bbs))
            landmarks = self.align.findLandmarks(rgbFrame, bb)
            #alignedFace aligned picture (still bit map)
            alignedFace = self.align.align(self.imgDim, rgbFrame, bb,
                                      landmarks=landmarks,
                                      landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if alignedFace is None:
                continue
            phash = str(imagehash.phash(Image.fromarray(alignedFace)))
            #tasete face
            rep = self.net.forward(alignedFace)
        self.images[phash] = Face(rep, identity,phash)
        return Face(rep,identity,phash)
            #
            #save
            #self.images[phash] = Face(rep, identity)
            #self.people.append(name)
    def trainSVMwithData(self,images):
        # Face.rep -> rep
        # Face.identity -> identity
        # Face.phash -> id
        X = []
        y = []
        for img in images:
            X.append(img.rep)
            y.append(img.identity)
        X = np.vstack(X)
        y = np.array(y)
        param_grid = [
            {'C': [1, 10, 100, 1000],
                'kernel': ['linear']},
            {'C': [1, 10, 100, 1000],
                'gamma': [0.001, 0.0001],
                'kernel': ['rbf']}
        ]
        # svm = self.svm if self.svm is not None else GridSearchCV(SVC(C=1), param_grid, cv=5)
        self.svm = GridSearchCV(SVC(C=1), param_grid, cv=5).fit(X, y)

    def findIdentity(self, imgData,isStram,isBase64,res):
        res = res if res is not None else self.res
        if isStram:
            imgF = StringIO.StringIO()
            imgF.write(imgData)
            imgF.seek(0)
            img = Image.open(imgF)
        elif isBase64:
            imgF = StringIO.StringIO()
            imgF.write(base64.b64decode(imgData))
            imgF.seek(0)
            img = Image.open(imgF)
        else:
            img = imgData
        buf = np.fliplr(np.asarray(img))
        rgbFrame = np.zeros(res, dtype=np.uint8)
        rgbFrame[:, :, 0] = buf[:, :, 2]
        rgbFrame[:, :, 1] = buf[:, :, 1]
        rgbFrame[:, :, 2] = buf[:, :, 0]
        annotatedFrame = np.copy(buf)
        identities = []
        # bbs = align.getAllFaceBoundingBoxes(rgbFrame)
        bb = self.align.getLargestFaceBoundingBox(rgbFrame)
        bbs = [bb] if bb is not None else []
        for bb in bbs:
            # print(len(bbs))
            landmarks = self.align.findLandmarks(rgbFrame, bb)
            alignedFace = self.align.align(self.imgDim, rgbFrame, bb,
                                      landmarks=landmarks,
                                      landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if alignedFace is None:
                continue

            phash = str(imagehash.phash(Image.fromarray(alignedFace)))
            # search db to get id
            if phash in self.images:
                identity = self.images[phash].identity
            else:
                rep = self.net.forward(alignedFace)
                if self.svm:
                    #pridict id
                    identity = self.svm.predict(rep)[0]
                else:
                    identity = -1
                if identity not in identities:
                    identities.append(identity)
        return identities

    def saveSvmToFile(self,filePathAndName):
        joblib.dump(self.svm, filePathAndName)

    def loadSvmFromFile(self,filePathAndName):
        self.svm = joblib.load(filePathAndName)
