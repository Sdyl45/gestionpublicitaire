import os
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.api import FacebookAdsApi

# Votre access token, account id et app id
ACCESS_TOKEN = 'EAAHZAsb1umoIBO0CRIHdIVbCD86kffLRC9i9trg1ZCIOceOg3rmokxjfvZCZBkXNyYSl8AObIDL1PqQK18IW2hpl3Qw9jb4Ud02vgvXu58k8gT6Qqz16RJOL4cVFZCK3NyxIMZBYvIKBPgo064qtahbHuLjkdZB8ttAzWvEK9WxtprEG56KOthWYFrZBZBCaJl4ZBSXHwABCI2CgNqlHjQjAfemIzCowZDZD'
ACCOUNT_ID = 'act_1822221194968260'  # Remplacez par votre ID de compte publicitaire
PAGE_ID = '434662436390612'  # ID de la page où se trouve la publication
POST_ID = '495804786652947'  # ID de la publication à booster

# Initialisation de l'API Facebook
FacebookAdsApi.init(access_token=ACCESS_TOKEN)


# Fonction pour créer une campagne
def create_campaign(account_id):
    account = AdAccount(account_id)
    campaign = account.create_campaign(
        params={
            'name': 'Boost de publication',
            'objective': 'OUTCOME_ENGAGEMENT',
            'status': 'PAUSED',  # Peut être 'ACTIVE' ou 'PAUSED'
            'buying_type': 'AUCTION',
            'special_ad_categories': ['EMPLOYMENT'],
        }
    )
    print(f"Campagne créée avec succès : {campaign['id']}")
    return campaign['id']


# Fonction pour créer un Ad Set (ensemble de publicités)
def create_ad_set(campaign_id, daily_budget, target_country):
    ad_account = AdAccount(ACCOUNT_ID)
    ad_set = ad_account.create_ad_set(
        params={
            'name': 'Ensemble de publicités pour booster la publication',
            'campaign_id': campaign_id,
            'daily_budget': daily_budget,  # Montant en centimes (ex: 10000 pour 100€)
            'billing_event': 'IMPRESSIONS',
            'optimization_goal': 'POST_ENGAGEMENT',
            'bid_amount': '200',  # Montant de l'enchère en centimes
            'targeting': {
                'geo_locations': {'countries': [target_country]},
                'facebook_positions': ['feed'],
                'age_min': 18,
                'age_max': 65,
                'genders': [1],  # 1 pour hommes, 2 pour femmes, ou [1, 2] pour tous
            },
            'status': 'PAUSED',  # Peut être 'ACTIVE' ou 'PAUSED'
        }
    )
    print(f"Ad Set créé avec succès : {ad_set['id']}")
    return ad_set['id']


# Fonction pour booster la publication
def create_ad(ad_set_id, page_id, post_id):
    ad_account = AdAccount(ACCOUNT_ID)
    ad = ad_account.create_ad(
        params={
            'name': 'Boost Publication Ad',
            'adset_id': ad_set_id,
            'creative': '{"object_story_id":"434662436390612_122112020678513728"}',
            'status': 'PAUSED',  # Peut être 'ACTIVE' ou 'PAUSED'
        }
    )
    print(f"Publicité créée avec succès : {ad['id']}")
    return ad['id']


# Appel des fonctions pour exécuter le processus
if __name__ == "__main__":
    try:
        # Étape 1: Créer une campagne
        campaign_id = create_campaign(ACCOUNT_ID)

        # Étape 2: Créer un Ad Set pour la campagne
        daily_budget = 1000  # Exemple: 10€ par jour (1000 centimes)
        target_country = 'CM'  # Cible géographique (Cameroun)
        ad_set_id = create_ad_set(campaign_id, daily_budget, target_country)

        # Étape 3: Créer une publicité autour de la publication existante
        ad_id = create_ad(ad_set_id, PAGE_ID, POST_ID)

        print(f"Le boost de la publication {POST_ID} a été créé avec succès. ID de la publicité : {ad_id}")

    except Exception as e:
        print(f"Erreur lors de la création du boost de la publication : {str(e)}")
