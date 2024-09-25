from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign

# Remplacez par vos informations
access_token = 'EAAHZAsb1umoIBO2m9xqoubTNrPX6q1jApd1i5vJj8OoneQdJOajJpEQzxCLtcROQf8fjzkYqdkcQbyrY9Bm5r20vKaOGTdsHIuNNFp8XZBVnV7ZC8qpFS8uyFUi0EMZCWOIFiGZChdKpmwHI5WXL8tsj16o6KQG91fsYmSHBJkqjEq8nlIdbZCVNwS732YLL4FDUkWpzn8'
account_id = 'act_1822221194968260'  # ID de compte publicitaire valide
campaign_id = '120212722750770015'  # ID de campagne valide

# Initialiser l'API
FacebookAdsApi.init(access_token=access_token)

# Vérifier l'état de la campagne
campaign = Campaign(campaign_id)
campaign_data = campaign.api_get(fields=['id', 'name', 'status'])

if campaign_data['status'] == 'ARCHIVED':
    print("La campagne est archivée. Veuillez l'activer avant de créer des ensembles de publicités.")
else:
    # Paramètres de l'ensemble de publicités
    params = {
        'name': 'Ma publicité',
        'optimization_goal': 'OFFSITE_CONVERSIONS',
        'billing_event': 'IMPRESSIONS',
        'bid_amount': '250',
        'daily_budget': '5000',
        'campaign_id': campaign_id,  # Utilisez la variable ici
        'targeting': {
            'facebook_positions': ['feed'],
            'geo_locations': {
                'countries': ['CM']
            }
        },
        'status': 'PAUSED',
        'promoted_object': {
            'application_id': '520832387291778',
            'custom_event_type': 'PURCHASE'
        },
    }

    try:
        # Créer l'objet AdAccount
        ad_account = AdAccount(account_id)

        # Créer l'ensemble de publicités
        ad_set = ad_account.create_ad_set(params=params)
        print(f"Ensemble de publicités créé avec succès : {ad_set}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
