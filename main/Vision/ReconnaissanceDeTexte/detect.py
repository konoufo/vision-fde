from __future__ import absolute_import, unicode_literals
from celery import shared_task
import cv2
import pytesseract
from pytesseract import Output
import os
import numpy as np
import time
import urllib

#https://www.inspection.gc.ca/exigences-en-matiere-d-etiquetage-des-aliments/etiquetage/industrie/etiquetage-nutritionnel/fra/1386881685057/1386881685870
#img_add = 'D4\\main\\static\\main\\img\\produit01.jpg'

#img_add = "C:\\Users\\Erwin Anoh\\PycharmProjects\\D4\\D4\\media\\images\\ingredients\\images (29).jpg"
#img_add = "C:\\Users\\Erwin Anoh\\PycharmProjects\\D4\\D4\\media\\images\\codesBarre\\téléchargement (5).jpg"
# https://www.murtazahassan.com/courses/opencv-projects/
# control + left click
""""
    https://www.canada.ca/fr/sante-canada/services/comprendre-etiquetage-aliments/tableau-valeur-nutritive.html
    Il vous donne également des renseignements sur les 13 principaux nutriments :

    les lipides
    les lipides saturés
    les lipides trans
    le cholestérol
    le sodium
    les glucides
    les fibres
    les sucres
    les protéines
    la vitamine A
    la vitamine C
    le calcium
    le fer
    Le saviez-vous?
    Il y a 13 principaux nutriments qui doivent figurer sur un tableau de la valeur nutritive. Cependant, voici une liste de certains des nutriments qui sont optionnels :

    le folate
    le magnésium
    la niacine
    le phosphore
    le potassium
    la riboflavine
    le sélénium
    la thiamine
    la vitamine B12
    la vitamine B6
    la vitamine D
    la vitamine E
    le zinc
    """
nutriments_principaux_13 = "lipides, lipides saturés,lipides trans, cholestérol, sodium, glucides, fibres, sucres, protéines, vitamine A,vitamine C, calcium, Fer"
nutriments_principaux_13 = nutriments_principaux_13.split(",")
nutriments_speciaux = "saturés, trans, polyinsaturés, oméga, monoinsaturés, fibres, sucres, B6, B-6, B12, B-12, vitamine"
nutriments_speciaux = nutriments_speciaux.split(",")
nutriments_facultatifs = "folate, magnésium, niacine, phosphore, potassium, riboflavine, sélénium, thiamine, vitamine B12, vitamine B6, vitamine D, vitamine E, zinc" \
                         ",Pantothénate"
nutriments_facultatifs = nutriments_facultatifs.split(",")
unites = "g,mh,%,yg"
all = nutriments_principaux_13 + nutriments_facultatifs + nutriments_speciaux
#print(all)
img_add = "../media/images/produit02.jpg"

'''
    CONFIGURATION DE LA COMMAND LINE DE PYTESSERACT
    VERIFIE SI ON UTILISE HEROKU OU PAS

'''

if os.environ.get("ENVIRONMENT", None) == "heroku":
    pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"
else:
    #le chemin de l'installation de tesseract
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

@shared_task
def detect_VN_ING(img_address=None, img_file=None, fast=1):
    # img_file = np.array(img_file)
    img = img_file if img_file is not None else cv2.imread(img_address)
    # pytesseract only accept rgb, so we convert bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ##############################################
    ##### Detecting Words  ######
    ##############################################
    #[   0          1           2           3           4          5         6       7       8        9        10       11 ]
    #['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text']
    boxes = pytesseract.image_to_data(img)
    # boxes_dict = pytesseract.image_to_data(img, output_type=Output.DICT)
    Text = pytesseract.image_to_string(img)
    #print(Text) # to see

    #######################################################################################################
    if fast == 0:
        hImg, wImg, _ = img.shape
        conf = r'--oem 3 --psm 6 outputbase digits'
        boxes = pytesseract.image_to_boxes(img, config=conf)
        boxes_splitted = boxes.splitlines()
        l1 = []
        l2 = []
        for b in boxes_splitted:
            b = b.split(' ')
            l1.append(tuple(b))
            l2.append(b[1:])
            # print(b)
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
            cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
    #######################################################################################################
    # boxes_splitted = boxes.splitlines()
    # text_splitted = []
    # l1 = []
    # l2 = []
    # for a,b in enumerate(boxes_splitted):
    #         #print(b)
    #         if a!=0:
    #             b = b.split()
    #             if len(b)==12:
    #                 x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
    #                 l1.append((b[11], x, y, w, h))
    #                 l2.append([x, y, w, h])
    #                 # cv2.putText(img,b[11],(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(255,50, 50),2)
    #                 cv2.rectangle(img, (x,y), (x+w, y+h), (255, 50, 50), 2)
    #                 text_splitted.append(b[11])

    ###################################################################################################
    n =0
    Text_splitted = Text.split('\n')
    for i in Text_splitted:
        # print(n,": " , i)
        n = n + 1

    # with open("p_valnutritive.txt", "w", encoding="utf-8") as file:
    #     for line in valeurs_nutritives:
    #         file.write(str(line[0]) + "\n")

    valeurs_nutritives = {}
    for j in all:
        valeurs_nutritives[j] = []
        for i in Text_splitted:
            if (i.replace(" ","")).lower().find(j.replace(" ","").lower()) != -1:
                # print(j, ": ", i)
                valeurs_nutritives[j].append(i)

    # print("-------------------------------------")
    for k in list(valeurs_nutritives):
        if valeurs_nutritives[k] == []:
            valeurs_nutritives.pop(k)
    ingredients = []
    l = 0
    for m in Text_splitted:
       l = l+1
       if m.lower().replace(" ", "").find("ingrédients".lower()) != -1:
           break

    for i in range(l, len(Text_splitted)-1):
        ingredients.append(Text_splitted[i])
        if Text_splitted[i] == '':
            break

    #print("ingredients: ", ingredients)


    return img, Text, valeurs_nutritives, {"Ingrédients":ingredients}
#
# img, Text, valeurs_nutritives, ingredients = detect_VN_ING(img_add)
# cv2.imshow("img", img)
# cv2.waitKey(0)

#
# for k, v in valeurs_nutritives.items():
#         if v!= []:
#             print(k, ": ", v)
# print(ingredients["Ingrédients"])
#

@shared_task
def process(img_adress=None, img_file=None):

    img = img_file if img_file is not None else cv2.imread(img_adress)
    # print(img)
    #pytesseract only accept rgb, so we convert bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    ##Detecting characters and their position
    #print(pytesseract.image_to_string(img))
    ##character xpoint ypoint width heigth
    #print(pytesseract.image_to_boxes(img))

    #taille
    hImg, wImg,_ = img.shape
    ##character xpoint ypoint width heigth
    boxes = pytesseract.image_to_boxes(img)
    boxes_splitted = boxes.splitlines()
    boxes_stringed = pytesseract.image_to_string(img).splitlines()
    for b in boxes_splitted:
        #print(b)
        b = b.split(' ')
        x,y,w,h = int( b[1]), int(b[2]), int(b[3]),int(b[4])

        # cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 1)
        cv2.rectangle(img, (x,hImg - y), (w, hImg - h), (50, 50, 255), 2)

        #ecrire le caracteres dessus
        cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 255, 50), 2)

    cv2.imshow('result', img)
    cv2.waitKey(0)

    return (img, boxes_splitted, boxes_stringed)
# process(img_add)

@shared_task
def find_characters(img_adress=None, img_file=None):

    img = img_file if img_file is not None else cv2.imread(img_adress)
    # pytesseract only accept rgb, so we convert bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #############################################
    #### Detecting Characters  ######
    #############################################
    hImg, wImg, _ = img.shape
    boxes = pytesseract.image_to_boxes(img)
    boxes_splitted = boxes.splitlines()
    for b in boxes_splitted:
        #print(b)
        b = b.split(' ')
        #print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
        # cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)

    return img, boxes_splitted

@shared_task
def find_only_digits(img_adress=None, img_file=None):

    img = img_file if img_file is not None else cv2.imread(img_adress)
    # pytesseract only accept rgb, so we convert bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #############################################
    #### Detecting ONLY Digits  ######
    #############################################
    hImg, wImg,_ = img.shape
    conf = r'--oem 3 --psm 6 outputbase digits'
    boxes = pytesseract.image_to_boxes(img, config=conf)

    boxes_splitted = boxes.splitlines()
    for b in boxes_splitted:
        #print(b)
        b = b.split(' ')
        #print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x,hImg- y), (w,hImg- h), (50, 255, 255), 2)
        cv2.putText(img,b[0],(x,hImg- y+25),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)

    return img, boxes_splitted

@shared_task
def find_nutrition_digits(img_adress=None, img_file=None):

    img = img_file if img_file is not None else cv2.imread(img_adress)
    # pytesseract only accept rgb, so we convert bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hImg, wImg,_ = img.shape
    conf = r'--oem 3 --psm 6 outputbase digits'
    boxes = pytesseract.image_to_boxes(img, config=conf)
    boxes_splitted = boxes.splitlines()
    l1 = []
    l2 = []
    for b in boxes_splitted:
        b = b.split(' ')
        l1.append(tuple(b))
        l2.append(b[1:])
        #print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x,hImg- y), (w,hImg- h), (50, 50, 255), 2)
        cv2.putText(img,b[0],(x,hImg- y+25),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)

    return img, boxes_splitted, l1, l2

###################################################################################
@shared_task
def detect_contours(img_adress=None, img_file=None):
    img = img_file if img_file is not None else cv2.imread(img_adress)
    # conversion en niveaux de gris(127,255,0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV)

    contours,h = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #key: figX, val = [contours, pointminHAUTGAUCHE, pointmaxBASDROITE)]
    sub_figures = {}
    key = "fig"
    n = 0
    xs = []
    ys = []
    point0 = 0
    point3 = 0
    points_plus_clairs = []
    fig_width = 0
    fig_heigth = 0
    for i in contours:
        if len(i)>2:
            for j in i:
                xs.append(j[0][0])
                ys.append(j[0][1])
                points_plus_clairs.append((j[0][0], j[0][1]))
                point0 = (min(xs), min(ys))
                point3 = (max(xs), max(ys))
                fig_width = abs(max(xs)-min(xs))
                fig_heigth = abs(max(ys)-min(ys))
            xs = []
            ys = []
            sub_figures[key+str(n)] = [i, point0, point3, fig_width, fig_heigth]
            n = n + 1
    return img, sub_figures

@shared_task
def mainproc(img_adress=None, img_file=None):
    img, sub_fig = detect_contours(img_adress=img_add, img_file=img_file)
    img1, bc_splitted = find_characters(img_file=img)
    img2, Text, valeurs_nutritives, ingredients = detect_VN_ING(img_file=img)
    img4, bnd_splitted, bnd_l1, bnd_l2 = find_nutrition_digits(img_file=img2)

    return ingredients, img, img1, img2, img4
