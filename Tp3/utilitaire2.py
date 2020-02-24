#!/usr/bin/python
# -*- coding: utf-8 -*-

# Quelques fonctions de traitements d'images
# Question1: tester quelques fonctions de filtrage

from PIL import Image

# ouvre une image
def ouvrir(nomimg):
    return Image.open(nomimg)

# enregistre une image
def enregistrer(ims, nomimg):
    return ims.convert('L').save(nomimg)

# affiche une image
def affiche(img):
    img.show()

# recupère un cannal d'une image multicannaux
def imc2img(imc, n):
    img = Image.new('F', imc.size)
    pixc = imc.load()
    pixg = img.load()
    (width, height) = imc.size
    for j in range(height):
        for i in range(width):
            pixg[i,j] = pixc[i,j][n]
    return img

# moyenne d'une image
def moyenne(ims):
    pixs = ims.load()
    imd = ims.copy()
    pixd = imd.load()
    (width, height) = ims.size
    for j in range(1,height-1):
        for i in range(1,width-1):
            p  = pixs[i,j]
            p += pixs[i-1,j-1]
            p += pixs[i,j-1]
            p += pixs[i+1,j-1]
            p += pixs[i-1,j]
            p += pixs[i+1,j]
            p += pixs[i-1,j+1]
            p += pixs[i,j+1]
            p += pixs[i+1,j+1]
            pixd[i,j] = (int)(p / 9.0)
    return imd

# moyenne itérative d'une image
def moyenneIterative(ims, n):
    imd = ims
    for i in range(n):
        imd = moyenne(imd)
    return imd



#Exercice 2 filtre médian
#2.1. médiane d'une liste
def mediane(liste):
    liste.sort()
    return liste[len(liste)/2]

#2.2. filtre médian
def MedianeImage(ims):
    imd0 = ims.copy()
    pixs = ims.load()
    pixd0 = imd0.load()
    (width, height) = ims.size
    for j in range(1,height-1):
        for i in range(1,width-1):
            liste=[pixs[i+1,j],pixs[i-1,j],pixs[i,j],pixs[i,j-1],pixs[i,j+1]]
            med=mediane(liste)
            pixd0[i,j] = med
    return imd0

#2.2. filtre médian itératif
def MedianeIteratif(ims,n):
    imd0 = ims.copy()
    imd1 = ims.copy()
    pixs = ims.load()
    (width, height) = ims.size
    for n_i in range(n):
        pixd0 = imd0.load()
        pixd1 = imd1.load()
        for j in range(1,height-1):
            for i in range(1,width-1):
                liste=[pixd0[i+1,j],pixd0[i-1,j],pixd0[i,j],pixd0[i,j-1],pixd0[i,j+1]]
                med=mediane(liste)
                pixd1[i,j] = med
        (imd0, imd1) = (imd1, imd0)
    return imd0


# dilatation d'une image
def dilatation(ims):
    pixs = ims.load()
    imd = ims.copy()
    pixd = imd.load()
    (width, height) = ims.size
    for j in range(1,height-1):
        for i in range(1,width-1):
            p = pixs[i,j]
            p = max(p, pixs[i-1,j-1])
            p = max(p, pixs[i,j-1])
            p = max(p, pixs[i+1,j-1])
            p = max(p, pixs[i-1,j])
            p = max(p, pixs[i+1,j])
            p = max(p, pixs[i-1,j+1])
            p = max(p, pixs[i,j+1])
            p = max(p, pixs[i+1,j+1])
            pixd[i,j] = p
    return imd


# dilatation itérative d'une image
def dilatationIterative(ims, n):
    imd = ims
    for i in range(n):
        imd = dilatation(imd)
    return imd


# Erosion d'une image
def erosion(ims):
    pixs = ims.load()
    imd = ims.copy()
    pixd = imd.load()
    (width, height) = ims.size
    for j in range(1,height-1):
        for i in range(1,width-1):
            p = pixs[i,j]
            p = min(p, pixs[i-1,j-1])
            p = min(p, pixs[i,j-1])
            p = min(p, pixs[i+1,j-1])
            p = min(p, pixs[i-1,j])
            p = min(p, pixs[i+1,j])
            p = min(p, pixs[i-1,j+1])
            p = min(p, pixs[i,j+1])
            p = min(p, pixs[i+1,j+1])
            pixd[i,j] = p
    return imd

# Erosion itérative d'une image
def erosionIterative(ims, n):
    imd = ims
    for i in range(n):
        imd = erosion(imd)
    return imd

# difference entre 2 images
def difference(ims0, ims1):
    pixs0 = ims0.load()
    pixs1 = ims1.load()
    imd = Image.new('F', ims0.size)
    pixd = imd.load()
    (width, height) = ims0.size
    for j in range(1,height-1):
        for i in range(1,width-1):
            pixd[i,j] = pixs0[i,j] - pixs1[i,j]
    return imd

# somme de 2 images
def somme(ims0, ims1):
    pixs0 = ims0.load()
    pixs1 = ims1.load()
    imd = Image.new('F', ims0.size)
    pixd = imd.load()
    (width, height) = ims0.size
    for j in range(height):
        for i in range(width):
            pixd[i,j] = pixs0[i,j] + pixs1[i,j]
    return imd

def binarization(ims, seuil):
    imd = ims.copy()
    pixs = ims.load()
    pixd = imd.load()
    (width, height) = ims.size
    for j in range(height):
        for i in range(width):
            pixd[i,j] = 255 if pixs[i,j] >= seuil else 0
    return imd



#############################################################

def fexponentiellex(ims, alpha): # Filtrage sur les colonnes
    imd = Image.new('F', ims.size)
    pixs = ims.load()
    pixd = imd.load()
    (width, height) = ims.size
    for j in range(height):
        pixd[0,j] = pixs[0,j]
        for i in range(1,width):
            pixd[i,j] = alpha * (pixd[i-1,j] - pixs[i,j]) + pixs[i,j]
        for i in range(width-2, -1, -1):
            pixd[i,j] = alpha * (pixd[i+1,j] - pixd[i,j]) + pixd[i,j]
    return imd

def fexponentielley(ims, alpha): #Filtrage sur les lignes
    imd = Image.new('F', ims.size)
    pixs = ims.load()
    pixd = imd.load()
    (width, height) = ims.size
    for i in range(height):
        pixd[i,0] = pixs[i,0]
        for j in range(1,height):
            pixd[i,j] = alpha * (pixd[i,j-1] - pixs[i,j]) + pixs[i,j]
        for j in range(height-2, -1, -1):
            pixd[i,j] = alpha * (pixd[i,j+1] - pixd[i,j]) + pixd[i,j]
    return imd

def fexponentielle(ims, alpha): #Filtrage lignes et colonnes
    im = fexponentiellex(ims, alpha)
    return fexponentielley(im, alpha)

def frontiere(ims):
    imd = Image.new('F', ims.size)
    pixs = ims.load()
    pixd = imd.load()
    (width, height) = ims.size
    for i in range(height-1):
        for j in range(width-1):
            if pixs[i,j] != pixs[i+1,j+0] or pixs[i,j] != pixs[i+0,j+1]:
               pixd[i,j] = 255
    return imd

def maximage(im1, im2):
    imd = Image.new('F', im1.size)
    pixs1 = im1.load()
    pixs2 = im2.load()
    pixd = imd.load()
    (width, height) = im1.size
    for i in range(height):
        for j in range(width):
            pixd[i,j] = max(pixs1[i,j], pixs2[i,j])
    return imd

#############################################################


def multcst(ims, s):
    imd = ims.copy()
    pixs = ims.load()
    pixd = imd.load()
    (width, height) = ims.size
    for j in range(height):
        for i in range(width):
            pixd[i,j] = s * pixs[i,j]
    return imd
#################################################################
def main():
    img = ouvrir("tangram.png")
    img.show()
main()
