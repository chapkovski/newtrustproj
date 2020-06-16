
print('inner', type(__name__))
import otree
from otree.session import create_session
cities = [(f"{x:02d}") for x in range(1, 13)]
for x in cities:
    print(x)

    create_session(
        session_config_name='trust_demo_ru',
        num_participants=2,
        label=x,
        modified_session_config_fields=dict(city_code=x)
    )

