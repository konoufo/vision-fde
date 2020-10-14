import cv2
import pytesseract
import unicodedata
import numpy as np
import timeit
import time

#https://www.inspection.gc.ca/exigences-en-matiere-d-etiquetage-des-aliments/etiquetage/industrie/etiquetage-nutritionnel/fra/1386881685057/1386881685870
#img_add = 'D4\\main\\static\\main\\img\\produit01.jpg'
img_add = "C:/Users/Erwin Anoh/PycharmProjects/D4/D4/media/images/general/produit02.jpg"
#img_add = "C:\\Users\\Erwin Anoh\\PycharmProjects\\D4\\D4\\media\\images\\ingredients\\images (29).jpg"
#img_add = "C:\\Users\\Erwin Anoh\\PycharmProjects\\D4\\D4\\media\\images\\codesBarre\\téléchargement (5).jpg"
def process(img_adress):
    #https://www.murtazahassan.com/courses/opencv-projects/
    #control + left click
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    img = cv2.imread(img_adress)
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

    # cv2.imshow('result', img)
    # cv2.waitKey(0)

    return (img, boxes_splitted, boxes_stringed)


def find_characters(img):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    # img = cv2.imread(img_address)
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
    #
    # cv2.imshow('characters', img)
    # cv2.waitKey(0)

    return img, boxes_splitted


def find_words(img):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    # img = cv2.imread(img_address)
    # pytesseract only accept rgb, so we convert bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ##############################################
    ##### Detecting Words  ######
    ##############################################
    #[   0          1           2           3           4          5         6       7       8        9        10       11 ]
    #['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text']
    boxes = pytesseract.image_to_data(img)
    #print(boxes) # to see

    boxes_splitted = boxes.splitlines()
    text_splitted = []
    l1 = []
    l2 = []
    for a,b in enumerate(boxes_splitted):
            #print(b)
            if a!=0:
                b = b.split()
                if len(b)==12:
                    x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                    l1.append((b[11], x, y, w, h))
                    l2.append([x, y, w, h])
                    # cv2.putText(img,b[11],(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(255,50, 50),2)
                    cv2.rectangle(img, (x,y), (x+w, y+h), (255, 50, 50), 2)
                    text_splitted.append(b[11])

    # cv2.imshow('words', img)
    # cv2.waitKey(0)

    return img, boxes_splitted, text_splitted, l1, l2

def find_only_digits(img):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    #img = cv2.imread(img_address)
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

    # cv2.imshow('only digits', img)
    # cv2.waitKey(0)

    return img, boxes_splitted

def find_nutrition_digits(img):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    #img = cv2.imread(img_address)
    # pytesseract only accept rgb, so we convert bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #############################################
    #### Detecting ONLY Digits  ######
    #############################################
    hImg, wImg,_ = img.shape
    conf = r'--oem 3 --psm 6 outputbase digits'
    boxes = pytesseract.image_to_boxes(img, config=conf)
    boxes_splitted = boxes.splitlines()
    # nutri_boxes = pytesseract.image_to_data(img).splitlines()
    # for b, c in zip(boxes_splitted, nutri_boxes):
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
    #
    # cv2.imshow('nutrition digits', img)
    # cv2.waitKey(0)

    return img, boxes_splitted, l1, l2

###################################################################################
def detect_contours(img_address):
    img = cv2.imread(img_address)
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


start_time = time.time()

def mainproc(img_add):
    img, sub_fig = detect_contours(img_add)
    # cv2.imshow('contours', img)
    # cv2.imwrite('p_contours.jpg', img)
    # cv2.waitKey(0)
    #
    #process(img_add)
    img1, bc_splitted = find_characters(img)
    # cv2.imshow('only characters', img1)
    # cv2.imwrite('p_characters.jpg', img1)
    # cv2.waitKey(0)

    img2, bw_splitted, text_splitted, bw_l1, bw_l2 = find_words(img)
    # cv2.imshow('words', img2)
    # cv2.imwrite('p_mots.jpg', img2)
    # cv2.waitKey(0)


    cv2.drawContours(img, [sub_fig["fig3"][0]], -1, (0,255,0), 2)
    cv2.drawContours(img, [sub_fig["fig1"][0]], -1, (0,255,0), 2)
    cv2.drawContours(img2, [sub_fig["fig3"][0]], -1, (0,255,0), 2)
    cv2.drawContours(img2, [sub_fig["fig1"][0]], -1, (0,255,0), 2)
    # cv2.imshow('words+contours', img2)
    # cv2.imwrite('p_mots_contours_tableaux.jpg', img2)
    # cv2.waitKey(0)

    img3, bod_splitted = find_only_digits(img)
    # cv2.imshow('only digits', img3)
    # cv2.waitKey(0)

    img4, bnd_splitted, bnd_l1, bnd_l2 = find_nutrition_digits(img)
    # cv2.imshow('nutrition digits', img4)
    # cv2.imwrite('p_nutritiondigit.jpg', img4)
    # cv2.waitKey(0)
    #########

    # for i, val in enumerate(text_splitted):
    #     #print(i)
    #     index_ingredient = val.lower().find("ingrédient")
    #     index_fin_ingredient = val.lower().find(".")
    #     if index_ingredient != -1:
    #         print("index: ", index_ingredient, " - content: ", val)
    #         deb = i
    #     if index_fin_ingredient != -1 :
    #         fin = i
    #         break

    # uncomment


    deb =0
    fin =0

    for i in range(0, len(text_splitted)):
        #print(i)
        index_ingredient = text_splitted[i].lower().find("ingrédient")

        if index_ingredient != -1:
            #print("index: ", index_ingredient, " - content: ", text_splitted[i])
            deb = i
            for j in range(i, len(text_splitted)):
                index_fin_ingredient = text_splitted[j].lower().find(".")
                if index_fin_ingredient != -1:
                    fin = j
                    break
            break

    ingredients = text_splitted[deb:fin+1]
    # print(ingredients)
    with open("p_ingredients.txt", "w", encoding="utf-8") as file:
        for line in ingredients:
            file.write(line + "\n")

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

    l = bw_l1 + bnd_l2
    l_int = []
    for i in l:
         l_int.append((i[0], int(i[1]),int(i[2]), int(i[3]), int(i[4])))

    l_int = sorted(l_int, key= lambda elem : elem[2])
    # for i in l_int:
    #     print(i)

    tableau = []
    for i in l_int:
        tableau.append({i[2]: i})
    # print(tableau)
    # student_tuples = [
    #     ('john', 'A', 15),
    #     ('jane', 'B', 12),
    #     ('dave', 'B', 10),
    # ]
    #sorted(student_tuples, key=lambda student: student[2])

    nutriments_principaux_13 ="lipides, lipides saturés,lipides trans, cholestérol, sodium,glucides, fibres, sucres, protéines, vitamine A,vitamine C, calcium, fer"
    nutriments_principaux_13 = nutriments_principaux_13.split(",")
    nutriments_facultatifs =" folate, magnésium, niacine, phosphore, potassium, riboflavine, sélénium, thiamine, vitamine B12, vitamine B6, vitamine D, vitamine E, zinc" \
                            ",Pantothénate, Sodium"
    nutriments_facultatifs.split(",")
# def val():
    valeurs_nutritives = []
    n = 0
    deb= 0
    fin = 0
    for i in l_int:
        index_ingredient = i[0].lower().find("valeur")
        index_fin_ingredient = i[0].lower().find(".")
        if index_ingredient != -1:
            deb = n
            #print("ok deb", deb)
        if index_fin_ingredient != -1:
            fin = n
            #print("ok fin", fin)
        n+=1

    valeurs_nutritives = l_int[deb:fin]
    # for i in valeurs_nutritives:
    #     print(i[0])

    with open("p_valnutritive.txt", "w", encoding="utf-8") as file:
        for line in valeurs_nutritives:
            file.write(str(line[0]) + "\n")

    interval = time.time() - start_time
    print( 'Total time in seconds:', interval )

    return ingredients, valeurs_nutritives
mainproc(img_add)