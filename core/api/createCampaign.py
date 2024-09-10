from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi

# Remplacez par vos informations
access_token = 'EAAHZAsb1umoIBO7jO2sCO0a7bSYtZCMphKy8YgSpEoKItxivvAYhOKVB2YsIZBdo0rj6U13fuUppvSqWGSVLPwITWLo24gqeLS3yLhc7DAYdaw7WiGx8a79JZCroixu4rlvBzZCMrD7vROokSfIeZBW1WdLzOZADk1sqhHMZBxR369h4TJyskqZAybIYR7zs2FUALHZBc8u1cZB'
app_secret = '12d45bcf60f869424e38f142d3bdec80'
app_id = '520832387291778'
account_id = 'act_1822221194968260'

# Initialiser l'API
FacebookAdsApi.init(access_token=access_token)

try:
    # Créer une instance de AdAccount
    account = AdAccount(account_id)

    # Récupérer des informations sur le compte
    account_info = account.api_get(fields=['id', 'name', 'account_status'])

    print(f"Account ID: {account_info['id']}, Name: {account_info['name']}, Status: {account_info['account_status']}")

    # Définir les paramètres de la campagne
    params = {
        'name': 'My campaign',
        'objective': 'OUTCOME_TRAFFIC',
        'status': 'PAUSED',
        'special_ad_categories': [],
    }

    # Créer la campagne
    campaign = account.create_campaign(fields=[], params=params)
    print(f"Campaign created with ID: {campaign['id']}")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")

