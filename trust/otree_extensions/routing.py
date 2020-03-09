from django.urls import re_path
from . import consumers
v4 = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}';

websocket_routes = [
    re_path(rf'export/decisions/(?P<user_id>{v4})', consumers.ExportConsumer),
]
