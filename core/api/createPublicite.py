from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign

ACCESS_TOKEN='EAAHZAsb1umoIBO2m9xqoubTNrPX6q1jApd1i5vJj8OoneQdJOajJpEQzxCLtcROQf8fjzkYqdkcQbyrY9Bm5r20vKaOGTdsHIuNNFp8XZBVnV7ZC8qpFS8uyFUi0EMZCWOIFiGZChdKpmwHI5WXL8tsj16o6KQG91fsYmSHBJkqjEq8nlIdbZCVNwS732YLL4FDUkWpzn8'
ACCOUNT_ID='act_1822221194968260'

def create_ad_set(campaign_id, nom, budget):
    # Initialiser l'API
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)

    # Vérifier l'état de la campagne
    campaign = Campaign(campaign_id)
    campaign_data = campaign.api_get(fields=['id', 'name', 'status'])

    if campaign_data['status'] == 'ARCHIVED':
        print("La campagne est archivée. Veuillez l'activer avant de créer des ensembles de publicités.")
        return None

    # Paramètres de l'ensemble de publicités
    params = {
        'name': nom,
        'optimization_goal': 'OFFSITE_CONVERSIONS',
        'billing_event': 'IMPRESSIONS',
        'bid_amount': 250,  # Montant d'enchère (entier, en centimes)
        'daily_budget': int(budget) * 100,  # Budget quotidien en centimes
        'campaign_id': campaign_id,
        'targeting': {
            'facebook_positions': ['feed'],
            'geo_locations': {
                'countries': ['CM']  # Ciblage géographique (Cameroun)
            }
        },
        'status': 'PAUSED',  # Statut de l'ensemble de publicités
        'promoted_object': {
            'application_id': '520832387291778',
            'custom_event_type': 'PURCHASE'
        },
    }

    # Créer l'objet AdAccount
    ad_account = AdAccount(ACCOUNT_ID)

    # Tentez de créer l'ensemble de publicités
    ad_set = ad_account.create_ad_set(params=params)

    # Retourner l'ID de l'ensemble de publicités ou None
    return ad_set.get('id') if ad_set else None
