from pyzbar import pyzbar
import argparse
import cv2

#
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to input image")
# args = vars(ap.parse_args())

#image = cv2.imread(args["image"])

path = "C:\\Users\\Erwin Anoh\\PycharmProjects\\D4\\D4\\media\\images\\produit01.jpg"

def get_string_barcode(img_addreess):
    image = cv2.imread(img_addreess)
    barcodes = pyzbar.decode(image)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode("utf-8")

        text = barcodeData[7:12]
        cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # cv2.imshow("Image", image)
        # cv2.waitKey(0)

    return image, barcodeData, text

# a, b, c = get_string_barcode(path)
#
# print(a, b, c)