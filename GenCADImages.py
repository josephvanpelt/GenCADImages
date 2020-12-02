#!/usr/bin/python3
# -----------------------------------------------------------------------------------------
# GenCADImages.py : a script to create some images from an STL file with multiple rotations
# written: Joseph VanPelt
# license: Public Domain - this is a simple demo script, please use freely
# -----------------------------------------------------------------------------------------
import vtkplotlib  # https://vtkplotlib.readthedocs.io/en/latest
from stl.mesh import Mesh # https://numpy-stl.readthedocs.io/en/latest/stl.html#stl-mesh
import numpy as np 
import math
import pathlib
import os
import sys

class genSTLImages():
    # settings for the number of rotations:
    rotationAngle = 10  # each step to take a shot on
    fullRotation = 350  # should we go all 360 degrees or less?
    # x/y/z axes + an odd one - these will be the rotation axis
    axes = [ np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1]), np.array([0,0.7071,0.7071])]

    # this function looks for a folder and creates it if needed
    def checkForFolderHere(self, path):
        if not os.path.exists(newFolder):
            try:
                os.mkdir(path) # create the folder if it isn't there
                return True
            except:
                print(sys.exc_info()[0])
                return False
        else:
            return True

    def deleteExistingImages(self, path):
        # check for existing images - delete them
        try:
            for f in os.listdir(path):
                if not f.endswith(".png"):
                    continue
                os.remove(os.path.join(newFolder, f))
            return True
        except:
            print(sys.exc_info()[0])
            return False

    def generateImages(self, mesh):
        axisName = 'w'
        for axis in self.axes:
            if axisName == 'w':
                axisName = 'x'
            elif axisName == 'x':
                mesh.rotate(np.array([1,0,0]), math.radians(45), None)
                axisName = 'y'
            elif axisName == 'y':
                mesh.rotate(np.array([0,1,0]), math.radians(45), None)
                axisName = 'z'
            elif axisName == 'z':
                mesh.rotate(np.array([0.5,0.866,0]), math.radians(45), None)
                axisName = 'zy'
            for x in range(math.floor(self.fullRotation/self.rotationAngle)):
                if axisName == 'z':
                    mesh.rotate(np.array([0,1,0]), math.radians(5), None)  # dual rotation for extra variation
                # rotate(axis, theta=0, point=None)
                mesh.rotate(axis, math.radians(self.rotationAngle), None)

                # Plot the mesh
                vtkplotlib.mesh_plot(mesh, color="blue")
                vtkplotlib.save_fig(os.path.normpath(newFolder + '/_' + axisName + str(x) + '.png'))  #saves the figure as an image
                vtkplotlib.figure.close(vtkplotlib.gcf())

# folder to put the images in:
imgFolder = "images"
# source for the STL file:
stlPath = os.path.normpath("/path/to/file.stl")

generator = genSTLImages() # instatiate the class

currentDir = pathlib.Path().absolute()  # get the path where this is executed
newFolder = os.path.join(currentDir, imgFolder)  # add the sub folder name

generator.checkForFolderHere(newFolder) # makes the sub directory if it doesn't exist
generator.deleteExistingImages(newFolder) # gets rid of existing images if they are in that subfolder

mesh = Mesh.from_file(stlPath) # Read the STL using numpy-stl

generator.generateImages(mesh)
