
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
import facebook
import requests

# access_token = '05ed2f1361ef0824b8c00858c7edd1f6'
access_token = 'EAAHZAsb1umoIBO7OrcsrFvYWSDMaxXayxsyNPMW6MglHgkZAn8cZB4WXPAFKJTf8jtMA8fduIRWXD5ylq6YtbQwt1tsrjbc5sZAmmpNJR6DeTu13AdM48aZBjGXP1OhT34uZAJwK470QBlTRDZAR9gnRwZAZCNntvBNFcuWgXfa4bB3KE5GMQ7X3lJzOKU4odglGsDOY15hVR'
app_secret = '12d45bcf60f869424e38f142d3bdec80'
# app_id = '520832387291778'
id = '61565411843230'
face=FacebookAdsApi.init(access_token=access_token)

# Set up your access token and ad account ID
# ACCESS_TOKEN = '05ed2f1361ef0824b8c00858c7edd1f6'
AD_ACCOUNT_ID = '520832387291778'

# Initialize the Facebook Graph API
graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="12.0")

# Step 1: Create a Campaign



access_token = '05ed2f1361ef0824b8c00858c7edd1f6'
app_secret = '12d45bcf60f869424e38f142d3bdec80'
app_id = '520832387291778'
id = '61565411843230'
graph=FacebookAdsApi.init(access_token=access_token)

# Set up your access token and ad account ID
ACCESS_TOKEN = '05ed2f1361ef0824b8c00858c7edd1f6'
AD_ACCOUNT_ID = '520832387291778'

# Initialize the Facebook Graph API
# graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="12.0")

# Step 1: Create a Campaign
def create_campaign(name, objective):
    params = {
        'name': name,
        'objective': objective,
        'status': 'PAUSED'  # Campaign status can be 'ACTIVE' or 'PAUSED'
    }
    try:
        campaign = graph.put_object(parent_object=f'{AD_ACCOUNT_ID}', connection_name='campaigns', **params)
        print(f"Successfully created campaign: {campaign['id']}")
        return campaign['id']
    except facebook.GraphAPIError as e:
        print("An error occurred:", e)
        return None

# Step 2: Create an Ad Set
def create_ad_set(campaign_id, name, daily_budget, start_time, end_time):
    params = {
        'name': name,
        'daily_budget': daily_budget,
        'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'REACH',
        'campaign_id': campaign_id,
        'targeting': {'geo_locations': {'countries': ['US']}},
        'start_time': start_time,
        'end_time': end_time,
        'status': 'PAUSED'
    }
    try:
        ad_set = graph.put_object(parent_object=f'{AD_ACCOUNT_ID}', connection_name='adsets', **params)
        print(f"Successfully created ad set: {ad_set['id']}")
        return ad_set['id']
    except facebook.GraphAPIError as e:
        print("An error occurred:", e)
        return None

# Step 3: Create an Ad Creative
def create_ad_creative(name, page_id, image_url, message):
    params = {
        'name': name,
        'object_story_spec': {
            'page_id': page_id,
            'link_data': {
                'image_hash': image_url,  # You would typically use a previously uploaded image
                'link': 'https://yourwebsite.com',
                'message': message
            }
        }
    }
    try:
        creative = graph.put_object(parent_object=f'{AD_ACCOUNT_ID}', connection_name='adcreatives', **params)
        print(f"Successfully created ad creative: {creative['id']}")
        return creative['id']
    except facebook.GraphAPIError as e:
        print("An error occurred:", e)
        return None

# Step 4: Create the Ad
def create_ad(name, ad_set_id, creative_id):
    params = {
        'name': name,
        'adset_id': ad_set_id,
        'creative': {'creative_id': creative_id},
        'status': 'PAUSED'
    }
    try:
        ad = graph.put_object(parent_object=f'{AD_ACCOUNT_ID}', connection_name='ads', **params)
        print(f"Successfully created ad: {ad['id']}")
        return ad['id']
    except facebook.GraphAPIError as e:
        print("An error occurred:", e)
        return None




# Main function to create a campaign, ad set, and ad
def main():
    campaign_id = create_campaign('My Campaign', 'REACH')
    if campaign_id:
        ad_set_id = create_ad_set(campaign_id, 'My Ad Set', '1000', '2024-09-01T00:00:00-0700', '2024-09-30T23:59:59-0700')
        if ad_set_id:
            creative_id = create_ad_creative('My Creative', 'your_page_id_here', 'your_image_hash_here', 'Check out our new product!')
            if creative_id:
                create_ad('My Ad', ad_set_id, creative_id)




