import os
import django
import requests

from services.models import PostPublication, FacebookPostInfo

# Définir la variable d'environnement pour Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialiser Django
django.setup()

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
            'fields': 'created_time,from,message,likes.summary(true),comments.summary(true){message,from,created_time}',
            'access_token': access_token
        }

        # Faire la requête
        response = requests.get(url, params=params)
        print(f"Réponse brute de l'API : {response.text}")  # Débogage

        if response.status_code == 200:
            data = response.json()
            from_info = data.get('from', {})
            posted_by = from_info.get('name', 'Inconnu')
            likes_summary = data.get('likes', {}).get('summary', {})
            comments_summary = data.get('comments', {}).get('summary', {})
            comments = data.get('comments', {}).get('data', [])

            # Enregistrer les informations de la publication
            facebook_post_info = FacebookPostInfo(
                post_id=post_id,
                posted_by=posted_by,
                likes_count=likes_summary.get('total_count', 0),
                comments_count=comments_summary.get('total_count', 0)
            )
            facebook_post_info.save()

            # Enregistrer les commentaires
            if comments:
                for comment in comments:
                    comment_id = comment['id']  # Récupérer l'ID du commentaire
                    commenter_name = comment['from'].get('name', 'Inconnu')
                    comment_message = comment.get('message', 'Aucun message')

                    # Créer une nouvelle instance de FacebookPostInfo pour chaque commentaire
                    comment_info = FacebookPostInfo(
                        post_id=post_id,  # Associé à la publication
                        comment_id=comment_id,
                        commenter_name=commenter_name,
                        comment_message=comment_message
                    )
                    comment_info.save()

            print(f"Informations enregistrées pour la publication ID: {post_id}")
        else:
            error_data = response.json().get('error', {})
            error_message = error_data.get('message', 'Erreur inconnue')
            error_code = error_data.get('code', 'Aucun code')
            print(f"Erreur {response.status_code} pour la publication {post_id}: {error_message} (Code: {error_code})")