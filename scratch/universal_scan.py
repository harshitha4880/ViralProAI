import requests
import json

def universal_scan():
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
    
    token = creds['access_token']
    base_url = "https://graph.facebook.com/v20.0/"
    
    print("--- UNIVERSAL META SCAN ---")
    
    # 1. Check Me
    me = requests.get(f"{base_url}me?fields=id,name&access_token={token}").json()
    print(f"User: {me.get('name')} ({me.get('id')})")
    
    # 2. Check Accounts (Pages)
    accounts = requests.get(f"{base_url}me/accounts?access_token={token}").json()
    pages = accounts.get('data', [])
    print(f"Found {len(pages)} Pages via 'me/accounts'")
    
    for p in pages:
        print(f" - Page: {p['name']} (ID: {p['id']})")
        ig = requests.get(f"{base_url}{p['id']}?fields=instagram_business_account&access_token={token}").json()
        print(f"   Link: {ig}")

    # 3. Check Instagram Accounts directly
    ig_accounts = requests.get(f"{base_url}me?fields=instagram_accounts&access_token={token}").json()
    print(f"Direct Instagram check: {ig_accounts}")

    # 4. Check Business Accounts
    biz = requests.get(f"{base_url}me/business_users?access_token={token}").json()
    print(f"Business Users: {biz}")

if __name__ == "__main__":
    universal_scan()
