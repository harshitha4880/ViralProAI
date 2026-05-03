# 🔌 Instagram Graph API Setup Guide

This guide explains how to get your production keys for the InstaViral AI platform.

## 1. Prerequisites
- An **Instagram Business** or **Creator** account.
- A **Facebook Page** linked to that Instagram account.
- A **Meta Developer Account**.

## 2. Step-by-Step Setup
### Phase A: The Developer Portal
1. Go to [Meta for Developers](https://developers.facebook.com/).
2. Create a new App (Select **Business** as the type).
3. In the "Add Products" section, add **Instagram Graph API**.

### Phase B: Permissions
You will need to request the following permissions during the token generation:
- `instagram_basic`
- `instagram_manage_insights`
- `pages_show_list`
- `pages_read_engagement`

### Phase C: Generating the Token
1. Use the [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. Select your App.
3. Click "Generate Token".
4. To get a **Long-Lived Token** (that lasts 60 days), click the info icon next to the token and select "Open in Access Token Tool".

## 3. Integrating with the App
Once you have your **Access Token** and **App ID**:
1. Open the **InstaViral AI** Dashboard.
2. Go to the **🔌 API Connections** page.
3. Paste your credentials and click **Connect**.

---
*Note: For official production use, you will eventually need to go through "App Review" by Meta to verify your business.*
