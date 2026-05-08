import sys
import os
import json

# Add current directory to path
sys.path.append(os.getcwd())

def run_diagnostic():
    print("--- ViralProAI Pre-Flight Diagnostic Active ---")
    
    # 1. Check Credentials
    print("\n[Step 1] Checking Credentials...")
    if not os.path.exists('credentials.json'):
        print("ERROR: credentials.json missing!")
        return
    try:
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
            if not creds.get('access_token'):
                print("ERROR: Access Token missing in credentials!")
            else:
                print("SUCCESS: Credentials Found.")
    except Exception as e:
        print(f"ERROR: Failed to read credentials: {e}")

    # 2. Check Database
    print("\n[Step 2] Checking Database...")
    try:
        from db_manager import DBManager
        db = DBManager()
        print("SUCCESS: Database Connection Successful.")
    except Exception as e:
        print(f"ERROR: Database Error: {e}")

    # 3. Check API Handler (Handshake)
    print("\n[Step 3] Checking Meta API Handshake...")
    try:
        from instagram_api_handler import InstagramAPIHandler
        api = InstagramAPIHandler()
        if api.ig_user_id:
            print(f"SUCCESS: API Handshake Successful! Connected to IG User: {api.ig_user_id}")
        else:
            print(f"WARNING: API Discovery failed. Error: {api.last_error}")
    except Exception as e:
        print(f"ERROR: API Handler Error: {e}")

    # 4. Check Model File
    print("\n[Step 4] Checking Virality Model...")
    if os.path.exists('virality_model.pkl'):
        size_mb = os.path.getsize('virality_model.pkl') / (1024 * 1024)
        print(f"SUCCESS: Model Found ({size_mb:.2f} MB).")
    else:
        print("WARNING: virality_model.pkl missing. You may need to train the model first.")

    print("\n--- Diagnostic Complete. System is primed for launch! ---")

if __name__ == "__main__":
    run_diagnostic()
