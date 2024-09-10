from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adset import AdSet

# Remplacez par vos informations
access_token = 'EAAHZAsb1umoIBO7jO2sCO0a7bSYtZCMphKy8YgSpEoKItxivvAYhOKVB2YsIZBdo0rj6U13fuUppvSqWGSVLPwITWLo24gqeLS3yLhc7DAYdaw7WiGx8a79JZCroixu4rlvBzZCMrD7vROokSfIeZBW1WdLzOZADk1sqhHMZBxR369h4TJyskqZAybIYR7zs2FUALHZBc8u1cZB'
account_id = 'act_1822221194968260'  # ID de compte publicitaire valide
ad_set_id = '120212331605370015'  # Remplacez par l'ID de votre ensemble de publicités

# Initialiser l'API
FacebookAdsApi.init(access_token=access_token)

try:
    # Créer l'objet AdAccount
    ad_account = AdAccount(account_id)

    # Récupérer les informations de l'ensemble de publicités
    ad_set = AdSet(ad_set_id)
    ad_set_data = ad_set.api_get(fields=[
        AdSet.Field.id,
        AdSet.Field.name,
        AdSet.Field.status,
        AdSet.Field.daily_budget,
        AdSet.Field.targeting,
        AdSet.Field.optimization_goal,
        AdSet.Field.billing_event,
    ])

    print(f"Ad Set Information: {ad_set_data}")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")