import requests
import json

file_path = "../media/images/produit02.jpg"
#url = "https://{domain_prefix}.vendhq.com/api/2.0/products/{product_id}/actions/image_upload"

def requete_post(file_path=None, url=None):
    files = {}
    headers = {}
    if file_path is not None:
        files = {'image': open(file_path, 'rb')}
        headers = {
            'authorization': "Bearer {token}"
        }
    response = requests.request("POST", url, files=files, headers=headers)
    return response.text

#####
url = "https://alivisiond4.herokuapp.com/api/images/"
r_post = requete_post(file_path=file_path, url=url)
print(r_post)

#primary key du produit
image_pk = json.loads(r_post)["pk"]

#####
url_ri = "https://alivisiond4.herokuapp.com/api/images/"+str(image_pk)+"/reconImage/"
r_post_reconImage = requete_post(url=url_ri)
#utiliser json.loads(r_post_reconImage) pour convertir la reponse en dictionnaire json
print(r_post_reconImage)

#####
url_rb = "https://alivisiond4.herokuapp.com/api/images/"+str(image_pk)+"/reconBarcode/"
r_post_reconBarcode = requete_post(url=url_rb)
#utiliser json.loads(r_post_reconBarcode) pour convertir la reponse en dictionnaire json
print(r_post_reconBarcode)