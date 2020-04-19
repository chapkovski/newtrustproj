from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

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
        'sorter',
        'trust',
        'questionnaire',
        'results'
    ],

    city1='',
    city2='',
    num_cubicles_city_1=24,
    num_cubicles_city_2=24,

)
SESSION_CONFIGS = [
    {**uni_trust,
     'city1': '01',
     'city2': '02',
     'name': 'trust_demo',
     'display_name': 'trust: DEMO! Moscow-St.Petersburg',
     'cq': True,
     'debug': True,
     'use_browser_bots': False},
    # {**uni_trust,
    #  'name': 'trust_cq',
    #  'display_name': 'trust: LAUNCH THIS FOR REAL STUDY!!!!!!',
    #  'cq': True,
    #  'use_browser_bots': False},
    {
        'name': 'questionnaire',
        'app_sequence': ['questionnaire'],
        'display_name': 'Questionnaire only',
        'num_demo_participants': 1,
        'use_browser_bots': False}
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ru'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'RUR'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'токен'

ROOMS = [{'name': 'hse', 'display_name': 'HSE Study'}]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'm1e8fnwh3#$v6xbng%$!jn_onduh(22hmzx$kt=$ch6+m6*lcg'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',
    'django.contrib.admin',

]
EXTENSION_APPS = ['trust']
MIDDLEWARE_CLASSES = ['django.middleware.locale.LocaleMiddleware', ]
USE_I18N = True
