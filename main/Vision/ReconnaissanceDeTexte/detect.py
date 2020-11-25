from __future__ import absolute_import, unicode_literals
from celery import shared_task
import cv2
import pytesseract
import os
import re
""""
Quelques liens utiles
    1 - https://www.murtazahassan.com/courses/opencv-projects/
    2 - https://www.inspection.gc.ca/exigences-en-matiere-d-etiquetage-des-aliments/etiquetage/industrie/etiquetage-nutritionnel/fra/1386881685057/1386881685870
    3 - https://www.canada.ca/fr/sante-canada/services/comprendre-etiquetage-aliments/tableau-valeur-nutritive.html
    
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
nutriments_principaux_13 = "lipides, lipides saturés,lipides trans, cholestérol, sodium, glucides, fibres, sucres, protéines, protein,carboxhydrate,sugar,sugars,calories,calorie,cholesterol, vitamine A,vitamine C, calcium, Fer"
nutriments_principaux_13 = nutriments_principaux_13.split(",")
nutriments_speciaux = "saturés, saturated, trans, polyinsaturés, oméga, monoinsaturés, fibres, sucres, B6, B-6, B12, B-12, vitamine,iron"
nutriments_speciaux = nutriments_speciaux.split(",")
nutriments_facultatifs = "folate, magnésium, niacine, phosphore, potassium, riboflavine, sélénium, thiamine, vitamine B12, vitamine B6, vitamine D, vitamine E, zinc" \
                         ",Pantothénate,Valeur,Valeur é, Valeur énergétique"
nutriments_facultatifs = nutriments_facultatifs.split(",")
unites = "g,mh,%,yg"
all = nutriments_principaux_13 + nutriments_facultatifs + nutriments_speciaux
ingr = "ingrédients,Ingredients,INGREDIENTS,INGRÉDIENTS,ingredients," \
           "Ingrédients,INGREDIENT,INGRÉDIENT,Ingredient," \
           "Ingrédient,Ingredient,Ingrédient"
ingr = ingr.split(",")

arret_val = "val,Val,VAL"
arret_ingr = "ING,ing,Ing"
arret_val = arret_val.split(",")
arret_ingr = arret_ingr.split(",")

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
    img = img_file if img_file is not None else cv2.imread(img_address)
    # pytesseract only accept rgb, so we convert bgr to rgb

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img)
    Text = pytesseract.image_to_string(img)
    # print(Text) # to see

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

    valeurs_nutritives = {}
    for j in all:
        valeurs_nutritives[j] = []
        for i in Text_splitted:
            if (i.replace(" ","")).lower().find(j.replace(" ","").lower()) != -1:
                # print(j, ": ", i)
                valeurs_nutritives[j].append(i.replace(j, "").lower())

    # print(valeurs_nutritives)
    # print("-------------------------------------")

    for k in list(valeurs_nutritives):
        if valeurs_nutritives[k] == []:
            valeurs_nutritives.pop(k)
    for k, v in valeurs_nutritives.items():
        for i in range(len(v)):
            # print(v[i], "===", k)
            v[i] = v[i].replace(k, "")
            v[i] = v[i].replace("9 ", "g ")

    ingredients = []
    debut = []
    n=0
    for m in Text_splitted:
       n = n+1
       for i in ingr:
           if m.lower().replace(" ", "").find(i) != -1:
               debut.append(n)

    fin = []
    n=0
    for i in range(len(Text_splitted)):
        n = n + 1
        try:
            if Text_splitted[i] == '' != -1 and n > min(debut):
                fin.append(n)
        except ValueError:
            pass
    f = 0
    a = 0
    try:
        f = min(fin)
        for i in arret_ingr:
            if Text_splitted[f].find(j) == -1:
                f += 1
    except (ValueError, IndexError):
        pass
 # print("debut: ", debut, "fin", fin)

    if len(debut) > 0 and len(fin)>0:
        a = min(debut) - 2
        while Text_splitted[a] == '':
            a += 1
        if len(fin) > 1:
            for i in range(a, fin[1]-2):
                ingredients.append(Text_splitted[i])
        else:
            for i in range(a, fin[0]-2):
                ingredients.append(Text_splitted[i])

    ingredients = "".join(ingredients)
    ingredients = cleaner(ingredients)

    # print("valeurs nutritives: ", valeurs_nutritives)
    # print("ingredients: ", ingredients)

    return img, Text, valeurs_nutritives, ingredients

def cleaner(ingredients):
    list_ingredients = ingredients
    for i in list_ingredients:
        if i.isalpha() == False and i.isdigit() == False \
                and i != "%" and i != "," and i != "." and i != " " and i != "(" and i != ")":
            list_ingredients = list_ingredients.replace(i, ",")

    for i in ingr:
        list_ingredients = list_ingredients.replace(i,"")
    return list_ingredients

# img_add = "../../../media/images/produit03.jpg"
# img_add = "../../../media/images/produit04 (5).jpeg"
# # img_add = "../../../media/images/produit04.png"
# img, Text, valeurs_nutritives, ingredients = detect_VN_ING(img_add)
# cv2.imshow("img", img)
# cv2.waitKey(0)


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
