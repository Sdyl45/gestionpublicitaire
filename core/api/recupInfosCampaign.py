from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi

# Remplacez par vos informations
access_token = 'EAAHZAsb1umoIBO7jO2sCO0a7bSYtZCMphKy8YgSpEoKItxivvAYhOKVB2YsIZBdo0rj6U13fuUppvSqWGSVLPwITWLo24gqeLS3yLhc7DAYdaw7WiGx8a79JZCroixu4rlvBzZCMrD7vROokSfIeZBW1WdLzOZADk1sqhHMZBxR369h4TJyskqZAybIYR7zs2FUALHZBc8u1cZB'
app_secret = '12d45bcf60f869424e38f142d3bdec80'
app_id = '520832387291778'
account_id = 'act_1822221194968260'
campaign_id = '120212245216230015'  # Assurez-vous que l'ID de campagne est correct

# Initialiser l'API
FacebookAdsApi.init(access_token=access_token)

try:
    # Créer une instance de AdAccount
    account = AdAccount(account_id)

    # Récupérer des informations sur le compte
    account_info = account.api_get(fields=['id', 'name', 'account_status'])
    print(f"Account ID: {account_info['id']}, Name: {account_info['name']}, Status: {account_info['account_status']}")

    # Créer une instance de Campaign
    campaign = Campaign(campaign_id)

    # Récupérer des informations sur la campagne
    campaign_info = campaign.api_get(fields=['id', 'name', 'objective', 'status'])
    print(f"Campaign ID: {campaign_info['id']}, Name: {campaign_info['name']}, Objective: {campaign_info['objective']}, Status: {campaign_info['status']}")

    # Récupérer les publicités de la campagne
    ads = campaign.get_ads(fields=['id', 'name', 'status', 'creative'])

    # Afficher les publicités récupérées
    print("Ads retrieved:")
    for ad in ads:
        print(f"Ad ID: {ad['id']}, Name: {ad['name']}, Status: {ad['status']}")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")