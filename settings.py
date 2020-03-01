from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

import yaml

with open(r'./data/cities.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    CITIES = yaml.load(file, Loader=yaml.FullLoader)

SESSION_CONFIGS = [
    dict(
        name='trust',
        use_browser_bots=False,
        display_name="trust: Moscow-SPB",
        num_demo_participants=2,
        app_sequence=[
            'sorter',
            'trust',
            'questionnaire',
            'results'],
        city1='MSK',
        city2='SPB',

    ),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'm1e8fnwh3#$v6xbng%$!jn_onduh(22hmzx$kt=$ch6+m6*lcg'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
EXTENSION_APPS=['trust']