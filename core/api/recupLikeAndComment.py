import os
import django
import requests

# Définir la variable d'environnement pour Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialiser Django
django.setup()

from services.models import PostPublication  # Importer après l'initialisation

def get_facebook_post_info_from_db(access_token):
    # Récupérer toutes les publications sauvegardées dans la base de données
    posts = PostPublication.objects.all()
    print(f"Nombre de publications trouvées : {posts.count()}")  # Débogage

    if not posts:
        print("Aucune publication trouvée dans la base de données.")
        return

    for post in posts:
        post_id = post.id_publication  # Assurez-vous que ce champ contient l'ID de publication Facebook
        print(f"Publication ID dans la base de données : {post_id}")  # Débogage

        if not post_id:
            print(f"Aucun ID de publication pour la publication avec l'ID {post.id}.")
            continue

        print(f"Tentative de récupération des informations pour la publication ID: {post_id}")

        # URL pour récupérer les informations de la publication
        url = f"https://graph.facebook.com/v16.0/{post_id}"
        params = {
            'fields': 'created_time,from,likes.summary(true),comments.summary(true){message,from,created_time}',
            'access_token': access_token
        }

        # Faire la requête
        response = requests.get(url, params=params)
        print(f"Réponse brute de l'API : {response.text}")  # Débogage

        if response.status_code == 200:
            data = response.json()
            from_info = data.get('from', {})
            print(f"Publié par: {from_info.get('name', 'Inconnu')}")
            print(f"Date de publication: {data.get('created_time', 'Pas de date')}")

            if 'message' in data:
                print(f"Message: {data['message']}")
            else:
                print("Aucun message disponible.")

            likes_summary = data.get('likes', {}).get('summary', {})
            print(f"Nombre de likes: {likes_summary.get('total_count', 0)}")

            comments_summary = data.get('comments', {}).get('summary', {})
            print(f"Nombre de commentaires: {comments_summary.get('total_count', 0)}")
            comments = data.get('comments', {}).get('data', [])
            if comments:
                print(f"\nCommentaires ({len(comments)}):")
                for comment in comments:
                    commenter = comment['from'].get('name', 'Inconnu')
                    message = comment.get('message', 'Aucun message')
                    created_time = comment.get('created_time', 'Pas de date')
                    print(f"- {commenter} a commenté : {message}")
                    print(f"  Date du commentaire : {created_time}")
            else:
                print("Aucun commentaire à afficher.")
        else:
            error_data = response.json().get('error', {})
            error_message = error_data.get('message', 'Erreur inconnue')
            error_code = error_data.get('code', 'Aucun code')
            print(f"Erreur {response.status_code} pour la publication {post_id}: {error_message} (Code: {error_code})")

# Appel de la fonction avec un token d'accès valide
access_token = "EAAHZAsb1umoIBO1Ht3uYF0fZAvyZCskZAYJX1zseSqG1bzMW7rse0MEsXUhYnIbCLUaY0RpA51rcgKLTg2CQW27yMIxr2Fe86200q8JfdR1g9sq7tocHtRgn2vgYbd7bIGqUdX2cM4PDBXzc8gt0vXnfuG4XhHF7riu9Xq1Lb3cpj8begpfglDiECCpmW0Io9itJ9P8nK9Rw28f7wkqyNfyh8HXZAd0P0"  # Remplacez par votre access token
get_facebook_post_info_from_db(access_token)
