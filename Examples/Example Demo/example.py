# start the api before running the app
# https://console.cloud.google.com/apis/api/vision.googleapis.com/credentials?inv=1&invt=AbxZJA&project=calm-analog-438816-p8

from flask import Flask, redirect, url_for, session, request, render_template # flask is a micro web framework for Python
import os, requests, base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest


# Create a flask instance 
app = Flask(__name__)
# Set a secret key for the session
app.secret_key = 'IHopeItWork8888' 

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Set 1 disables SSL checks (used only for development). In production, HTTPS should be used.

# path to your Google OAuth2 credentials file 
CLIENT_SECRETS_FILE = "client_secret.json" 

# Scope defines the permissions your app will request. In this case, request access to Google Cloud APIs (Vision API).
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# this is for the index route
@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    return render_template('index.html')

# this is for the authorize route
@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    auth_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(auth_url)

# this is for the oauth2callback route
@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('index'))

@app.route('/detect', methods=['POST'])
def detect():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    creds = Credentials(**session['credentials'])
    image = request.files['image']
    content = base64.b64encode(image.read()).decode('utf-8')

    vision_payload = {
        "requests": [{
            "image": {"content": content},
            "features": [{"type": "LOGO_DETECTION"}]
        }]
    }

    headers = {"Authorization": f"Bearer {creds.token}"}
    r = requests.post('https://vision.googleapis.com/v1/images:annotate',
                      json=vision_payload, headers=headers)

    print("Response status:", r.status_code)
    print("Response body:", r.text)  # <--- Add this line

    try:
        logos = r.json()['responses'][0].get('logoAnnotations', [])
    except KeyError:
        return {"error": "Unexpected response from Vision API", "raw_response": r.text}, 500

    return {'logos': logos}

if __name__ == '__main__':
    app.run(debug=True)