
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi

ACCESS_TOKEN = 'EAAHZAsb1umoIBO7jO2sCO0a7bSYtZCMphKy8YgSpEoKItxivvAYhOKVB2YsIZBdo0rj6U13fuUppvSqWGSVLPwITWLo24gqeLS3yLhc7DAYdaw7WiGx8a79JZCroixu4rlvBzZCMrD7vROokSfIeZBW1WdLzOZADk1sqhHMZBxR369h4TJyskqZAybIYR7zs2FUALHZBc8u1cZB'
ACCOUNT_ID = 'act_1822221194968260'


def create_campaign(nom):
    """
    Fonction pour créer une campagne publicitaire via l'API Facebook.

    Parameters:
    nom (str): Le nom de la campagne publicitaire.
    """
    if not nom:
        print("Le nom de la campagne est requis.")
        return None

    # Initialiser l'API
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)

    # Créer une instance de AdAccount
    account = AdAccount(ACCOUNT_ID)

    # Récupérer des informations sur le compte publicitaire
    account_info = account.api_get(fields=['id', 'name', 'account_status'])
    print(f"Account ID: {account_info['id']}, Name: {account_info['name']}, Status: {account_info['account_status']}")

    # Définir les paramètres de la campagne
    params = {
        'name': nom,  # Assurez-vous que le nom est fourni
        'objective': 'OUTCOME_TRAFFIC',  # Objectif de la campagne
        'status': 'PAUSED',  # Statut initial de la campagne
        'special_ad_categories': ['EMPLOYMENT'],  # Si aucune catégorie spéciale, mettez une liste vide
    }

    # Créer la campagne
    campaign = account.create_campaign(fields=[], params=params)
    print(f"Campaign created with ID: {campaign['id']}")

    return campaign['id']



