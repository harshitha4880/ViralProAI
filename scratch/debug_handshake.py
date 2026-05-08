import requests
import json

def debug_meta_link():
    print("--- ViralProAI Deep Handshake Probe Active ---")
    
    try:
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
        
        token = creds['access_token']
        base_url = "https://graph.facebook.com/v20.0/"
        
        # 1. Test Token Validity & Permissions
        print("\n[Phase 1] Testing Token Permissions...")
        me_url = f"{base_url}me?fields=id,name&access_token={token}"
        me_res = requests.get(me_url).json()
        
        if 'error' in me_res:
            print(f"ERROR: {me_res['error'].get('message')}")
            return
        else:
            print(f"SUCCESS: Token Healthy: Connected as {me_res.get('name')} (ID: {me_res.get('id')})")

        # 2. Check Linked Facebook Pages
        print("\n[Phase 2] Checking Linked Facebook Pages...")
        pages_url = f"{base_url}me/accounts?access_token={token}"
        pages_res = requests.get(pages_url).json()
        
        pages = pages_res.get('data', [])
        if not pages:
            print("WARNING: No Facebook Pages found linked to this token.")
        else:
            print(f"SUCCESS: Found {len(pages)} Facebook Page(s).")
            for p in pages:
                print(f"   - Page: {p.get('name')} (ID: {p.get('id')})")

        # 3. Check Instagram Business Discovery
        print("\n[Phase 3] Probing for Instagram Business Accounts...")
        found_ig = False
        for p in pages:
            p_id = p.get('id')
            ig_url = f"{base_url}{p_id}?fields=instagram_business_account&access_token={token}"
            ig_res = requests.get(ig_url).json()
            
            if 'instagram_business_account' in ig_res:
                ig_id = ig_res['instagram_business_account']['id']
                print(f"SUCCESS: Linked IG Business Account Found: {ig_id} (on Page: {p.get('name')})")
                found_ig = True
                
                # 4. Test Profile Fetch
                print("\n[Phase 4] Testing Profile Data Fetch...")
                prof_url = f"{base_url}{ig_id}?fields=username,followers_count&access_token={token}"
                prof_res = requests.get(prof_url).json()
                if 'username' in prof_res:
                    print(f"FINAL VERIFICATION: Successfully fetched @{prof_res['username']} with {prof_res['followers_count']} followers.")
                else:
                    print(f"FETCH ERROR: {prof_res.get('error', {}).get('message', 'Unknown Error')}")
                break
        
        if not found_ig:
            print("FAILURE: No Instagram Business Account is linked to ANY of your Facebook Pages.")

    except Exception as e:
        print(f"CRITICAL PROBE FAILURE: {e}")

    print("\n--- Diagnostic Probe Complete ---")

if __name__ == "__main__":
    debug_meta_link()
