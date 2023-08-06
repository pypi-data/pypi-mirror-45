from kuveytturk.api import API
from kuveytturk.auth import OAuthHandler

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = ''
PRIVATE_KEY = ''

# Create an authentication handler with your credentials
auth = OAuthHandler(CLIENT_ID, CLIENT_SECRET, PRIVATE_KEY, REDIRECT_URI)

# Then create an API instance using this authentication handler
api = API(auth)

r = api.fx_currency_rates()