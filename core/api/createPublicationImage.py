import requests

# Configuration
page_id = '434662436390612'  # Remplacez par votre Page ID
access_token = 'EAAHZAsb1umoIBOZBmX8tynD4871oFDnhfMS43JXh8eWoO9ff5xYHxtzme1udX55YJf5Vn3iM6AOcn5FZCfTfQlQIbiJlRtKHZANA1RZBu4aLOPIRa3Gc3zzyn1OSLF9odH0d2QRLGemdZCbZCl3X1Jl65omQkK6t7AriD5yZC7kKyfkLFTSWIy00q47R2ZBz0wPtFKNOhakZCpQLCw2z8Gb2gY3ZAx2L7is86kA'  # Assurez-vous qu'il s'agit d'un token de page
message = 'Ma publication!'  # Message que vous souhaitez publier avec la photo
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
