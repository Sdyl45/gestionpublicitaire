import requests
import os

class FacebookService:
    def __init__(self, page_id, access_token):
        self.page_id = page_id
        self.access_token = access_token
        self.base_url = f'https://graph.facebook.com/{self.page_id}'

    def publish_message(self, message):
        """Publier un simple message texte."""
        url = f'{self.base_url}/feed'
        params = {
            'message': message,
            'access_token': self.access_token
        }
        response = requests.post(url, data=params)
        return self._handle_response(response)

    def publish_image(self, message, image_path):
        """Publier une image avec un message."""
        url = f'{self.base_url}/photos'
        try:
            with open(image_path, 'rb') as image:
                files = {'source': image}
                data = {
                    'message': message,
                    'access_token': self.access_token
                }
                response = requests.post(url, files=files, data=data)
            return self._handle_response(response)
        except FileNotFoundError:
            return {"error": f"Image not found: {image_path}"}

    def publish_video(self, description, video_path):
        """Publier une vidéo avec une description."""
        url = f'{self.base_url}/videos'
        try:
            with open(video_path, 'rb') as video:
                files = {'source': video}
                data = {
                    'description': description,
                    'access_token': self.access_token
                }
                response = requests.post(url, files=files, data=data)
            return self._handle_response(response)
        except FileNotFoundError:
            return {"error": f"Video not found: {video_path}"}

    def _handle_response(self, response):
        """Gérer les réponses de l'API."""
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Échec de la publication. Code: {response.status_code}, "
                         f"Erreur: {response.text}"
            }
