from django.utils.translation import ugettext as _

USER_TYPE_CHOICES = ()

GOOGLE_ACCESS_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_PEOPLE_API_URL = 'https://www.googleapis.com/plus/v1/people/me'

TWITTER_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
TWITTER_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
TWITTER_PEOPLE_API_URL = 'https://api.twitter.com/1.1/account/verify_credentials.json'

GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_PEOPLE_API_URL = 'https://api.github.com/user'

STRIPE_ACCESS_TOKEN_URL = 'https://connect.stripe.com/oauth/token'
STRIPE_PEOPLE_API_URL = ''
