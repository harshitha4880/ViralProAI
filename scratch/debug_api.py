import requests
import json
import os

def debug_connection():
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
    
    token = creds['access_token']
    base_url = "https://graph.facebook.com/v20.0/"
    
    print("--- META API DIAGNOSTIC ---")
    
    # 1. Check Token Validity & Scopes
    print("\n1. Testing Token & Permissions...")
    me_resp = requests.get(f"{base_url}me?access_token={token}").json()
    print(f"Token Owner: {me_resp.get('name', 'ERROR: ' + str(me_resp))}")
    
    debug_resp = requests.get(f"{base_url}debug_token?input_token={token}&access_token={creds['app_id']}|{creds['app_secret']}").json()
    scopes = debug_resp.get('data', {}).get('scopes', [])
    print(f"Permissions granted: {', '.join(scopes)}")
    
    # 2. Check Pages
    print("\n2. Searching for Linked Facebook Pages...")
    pages_resp = requests.get(f"{base_url}me/accounts?access_token={token}").json()
    pages = pages_resp.get('data', [])
    print(f"Found {len(pages)} Pages.")
    
    for page in pages:
        p_name = page['name']
        p_id = page['id']
        print(f"   - Page: {p_name} (ID: {p_id})")
        
        # 3. Check for Instagram Business Account
        print(f"   - Checking for Instagram link on '{p_name}'...")
        ig_resp = requests.get(f"{base_url}{p_id}?fields=instagram_business_account&access_token={token}").json()
        
        if 'instagram_business_account' in ig_resp:
            ig_id = ig_resp['instagram_business_account']['id']
            print(f"   SUCCESS! Found Instagram ID: {ig_id}")
            
            # 4. Fetch Profile
            prof_resp = requests.get(f"{base_url}{ig_id}?fields=username,followers_count,name&access_token={token}").json()
            print(f"   Linked Account: @{prof_resp.get('username')} ({prof_resp.get('followers_count')} followers)")
        else:
            print(f"   NO Instagram account linked to this page yet.")

if __name__ == "__main__":
    debug_connection()
