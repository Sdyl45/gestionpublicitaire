from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi

# Remplacez par vos informations
access_token = 'EAAHZAsb1umoIBO7jO2sCO0a7bSYtZCMphKy8YgSpEoKItxivvAYhOKVB2YsIZBdo0rj6U13fuUppvSqWGSVLPwITWLo24gqeLS3yLhc7DAYdaw7WiGx8a79JZCroixu4rlvBzZCMrD7vROokSfIeZBW1WdLzOZADk1sqhHMZBxR369h4TJyskqZAybIYR7zs2FUALHZBc8u1cZB'
account_id = 'act_1822221194968260'  # ID de compte publicitaire valide

# Initialiser l'API
FacebookAdsApi.init(access_token=access_token)

# Paramètres de l'ensemble de publicités
params = {
    'name': 'Ma publicité',
    'optimization_goal': 'OFFSITE_CONVERSIONS',
    'billing_event': 'IMPRESSIONS',
    'bid_amount': '250',
    'daily_budget': '5000',
    'campaign_id': '120212245216230015',
    'targeting': {
        'facebook_positions': ['feed'],
        'geo_locations': {
            'countries': ['CM']
        }
    },
    'status': 'PAUSED',
    'promoted_object': {
        'application_id': '520832387291778',  # Remplacez par votre application_id
        'custom_event_type': 'PURCHASE'  # Utilisez 'custom_event_type'
    },
}

try:
    # Créer l'objet AdAccount
    ad_account = AdAccount(account_id)

    # Créer l'ensemble de publicités
    ad_set = ad_account.create_ad_set(params=params)
    print(f"Ad Set created successfully: {ad_set}")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")