import cv2
import pytesseract
import unicodedata
#https://www.inspection.gc.ca/exigences-en-matiere-d-etiquetage-des-aliments/etiquetage/industrie/etiquetage-nutritionnel/fra/1386881685057/1386881685870
#img_add = 'D4\\main\\static\\main\\img\\produit01.jpg'
img_add = "C:\\Users\\Erwin Anoh\\PycharmProjects\\D4\\D4\\media\\images\\general\\produit02.jpg"
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


def find_characters(img_address):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    img = cv2.imread(img_address)
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
        cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
    #
    # cv2.imshow('img', img)
    # cv2.waitKey(0)

    return boxes_splitted


def find_words(img_address):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    img_o = cv2.imread(img_address)
    img = cv2.imread(img_address)
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
                    cv2.putText(img,b[11],(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
                    cv2.rectangle(img, (x,y), (x+w, y+h), (50, 50, 255), 2)
                    text_splitted.append(b[11])

    # cv2.imshow('img', img_o)
    # cv2.waitKey(0)

    return (boxes_splitted, text_splitted, l1, l2)

def find_only_digits(img_address):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    img = cv2.imread(img_address)
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
        print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x,hImg- y), (w,hImg- h), (50, 50, 255), 2)
        cv2.putText(img,b[0],(x,hImg- y+25),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)

    cv2.imshow('img', img)
    cv2.waitKey(0)

    return boxes_splitted

def find_nutrition_digits(img_address):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    img = cv2.imread(img_address)
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
    # cv2.imshow('img', img)
    # cv2.waitKey(0)

    return (boxes_splitted, l1, l2)

#process(img_add)
bc_splitted = find_characters(img_add)
bw_splitted = find_words(img_add)
l1 = bw_splitted[2]
#bd_splitted = find_only_digits(img_add)
bd_splitted = find_nutrition_digits(img_add)
l2 = bd_splitted[1]
#########

# for i, val in enumerate(bw_splitted[1]):
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

for i in range(0, len(bw_splitted[1])):
    #print(i)
    index_ingredient = bw_splitted[1][i].lower().find("ingrédient")

    if index_ingredient != -1:
        print("index: ", index_ingredient, " - content: ", bw_splitted[1][i])
        deb = i
        for j in range(i, len(bw_splitted[1])):
            index_fin_ingredient = bw_splitted[1][j].lower().find(".")
            if index_fin_ingredient != -1:
                fin = j
                break
        break

ingredients = bw_splitted[1][deb:fin+1]
print(ingredients)


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

l =l1 + l2
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
def val():
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
    for i in valeurs_nutritives:
        print(i[0])

    return valeurs_nutritives
val()