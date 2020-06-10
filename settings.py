from os import environ
import os

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']
GOOGLE_API_KEY = environ.get('GOOGLE_API_KEY')
print('GOOGLE_API', GOOGLE_API_KEY)
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=10.00, participation_fee=150.00, doc=""
)

LANGUAGE_SESSION_KEY = '_language'
import yaml

with open(r'./data/cities.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    CITIES = yaml.load(file, Loader=yaml.FullLoader)
uni_trust = dict(
    name='trust',
    use_browser_bots=False,
    display_name="trust: Intercity Russia",
    num_demo_participants=2,
    app_sequence=[
        # 'sorter',
        'trust',
        # 'questionnaire',
        'last'
    ],



)
SESSION_CONFIGS = [
    {**uni_trust,
     'city_code': '01',
     'name': 'trust_demo_ru',
     'display_name': 'trust: DEMO! Moscow ONLY RUSSIAN',
     'cq': True,
     'debug': True,
     'use_browser_bots': False,
     'language': 'ru'
     },
    {**uni_trust,
     'city_code': '01',
     'name': 'trust_demo_en',
     'display_name': 'trust: DEMO! Moscow ONLY ENGLISH',
     'cq': True,
     'debug': True,
     'use_browser_bots': False,
     'language': 'en'
     },

    {
        'name': 'questionnaire_ru',
        'app_sequence': [
            'questionnaire',
            'last'
        ],
        'display_name': 'Questionnaire only - RUSSIAN',
        'num_demo_participants': 1,
        'use_browser_bots': False,
        'language': 'ru'},
    {
        'name': 'questionnaire_en',
        'app_sequence': [
            'questionnaire',
            'last'
        ],
        'display_name': 'Questionnaire only - ENGLISH',
        'num_demo_participants': 1,
        'use_browser_bots': False,
        'language': 'en'}
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ru'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'RUR'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'токен'

ROOMS = [{'name': 'hse', 'display_name': 'HSE Study'}]
GOOGLE_API_KEY = environ.get('GOOGLE_API_KEY')
ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'm1e8fnwh3#$v6xbng%$!jn_onduh(22hmzx$kt=$ch6+m6*lcg'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',
    'django.contrib.admin',
    'webpack_loader',
    'questionnaire',  # we need this only because we use generic pages from there.
    'mingle', # this one is responsible for mingling.

]
EXTENSION_APPS = ['trust', 'mingle', 'tolokaregister']
MIDDLEWARE_CLASSES = ['django.middleware.locale.LocaleMiddleware', ]
USE_I18N = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VUE_FRONTEND_DIR = os.path.join(BASE_DIR, 'vue_frontend')
WEBPACK_LOADER = {
    'DEFAULT': {
        # 'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'vue/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'vue_frontend', 'webpack-stats.json'),
        'POLL_INTERVAL': 0.3,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}
