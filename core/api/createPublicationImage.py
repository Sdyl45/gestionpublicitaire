import requests

# Configuration
page_id = '434662436390612'  # Remplacez par votre Page ID
access_token = 'EAAHZAsb1umoIBO4aSGxHV1ZCBtZCIop28F8oEt4B94f12Kai4HuPC97JdaeszSuxpsPoWG0ZBZAEI1m0t3kpsvygbUQk612xCGWZAGOrA345dZCWVPg7VCuMngGVZASiAbSOn6otoVaaX1IapMaAKB0ULr36Ady1YmPdM3TCrZCBS0KdU6sVKvP0DribA4EJP5qxwfCe4ZCVCfQTi59xOEpnzRapvmLfwAhl44'  # Assurez-vous qu'il s'agit d'un token de page
message = 'Voici une photo !'  # Message que vous souhaitez publier avec la photo
photo_path = 'C:/Users/LYAN/PycharmProjects/montest/static/images/mage2.jpg'  # Chemin vers votre image locale

# Publier une photo avec un message sur la page
url = f'https://graph.facebook.com/{page_id}/photos'

try:
    with open(photo_path, 'rb') as photo:
        files = {
            'source': photo  # L'image est envoyée en binaire
        }
        data = {
            'message': message,  # Le message est placé dans les paramètres de requête
            'access_token': access_token  # Token d'accès pour authentification
        }
        response = requests.post(url, files=files, data=data)

    # Vérification du succès de la requête
    if response.status_code == 200:
        print("Photo publiée avec succès !", response.json())
    else:
        print(f"Échec de la publication. Code: {response.status_code}, Erreur: {response.text}")

except FileNotFoundError:
    print(f"Erreur : Le fichier {photo_path} est introuvable.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")
