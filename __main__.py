from bitdeli import Profiles, set_theme, Description, Title
from itertools import chain
from collections import Counter
from datetime import datetime

WINDOW = 48
text = {}

set_theme('playground')

def date(hour):
    return strftime('%B %d, %Y')

def users(profiles):
    weeks = Counter()
    for profile in profiles:
        if 'email' in profile['properties']:
            hour, count = min(chain.from_iterable(profile['events'].itervalues()))
            year, week, day = datetime.utcfromtimestamp(hour * 3600).isocalendar()
            if year == 2013:
                weeks[(year, week)] += 1
    data = sorted(weeks.items())
    yield {'type': 'bar',
           'size': (12, 4),
           'data': data}
    
Profiles().map(users).show()
