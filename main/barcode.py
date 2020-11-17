from pyzbar import pyzbar
import argparse
import cv2
import requests
import json

#
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to input image")
# args = vars(ap.parse_args())

#image = cv2.imread(args["image"])

path = "C:\\Users\\Erwin Anoh\\PycharmProjects\\D4\\D4\\media\\images\\produit01.jpg"

def get_string_barcode(img_addreess=None, img_file=None):
    image = img_file if img_file is not None else cv2.imread(img_addreess)
    barcodes = pyzbar.decode(image)
    barcodeData = ""

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode("utf-8")

        text = barcodeData
        cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # cv2.imshow("Image", image)
        # cv2.waitKey(0)

    url = "https://world.openfoodfacts.org/api/v0/product/[" + barcodeData + "].json"
    try:
        response = requests.get(url)
        data = json.loads(response.content)
        marque = data['product']['brands']
        product_name = data['product']['product_name']
        nutriments = data['product']['nutriments']
        ingredients = data['product']['ingredients_text']
        countries = data['product']['countries']
    except:
        print("Please enter a valide code")
    description = ["Product brand", "Product name", "Nutriments", "Ingredients", "Countries"]
    information = [marque, product_name, nutriments, ingredients, countries]
    fichier = dict(zip(description, information))

    if len(barcodeData) < 2 or text == ""  or len(text)< 2:
        barcodeData = "0000000000"
        text = "Product not found"
        fichier = "Product not found"

    return image, barcodeData, text, fichier

# a, b, c = get_string_barcode(path)
#
# print(a, b, c)