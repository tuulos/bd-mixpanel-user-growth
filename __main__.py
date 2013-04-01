from bitdeli import Profiles, set_theme, Description, Title
from itertools import chain
from collections import Counter
from datetime import datetime, timedelta

WINDOW = 48
text = {}

set_theme('playground')

def date(hour):
    return strftime('%B %d, %Y')

def cumulative(data, cum):
    d = datetime(2013, 1, 1)
    for (year, week), count in data:
        t = d + timedelta(weeks = week)
        cum += count
        yield t.strftime('%Y-%m-%d'), cum

def users(profiles):
    weeks = Counter()
    cum = 0
    for profile in profiles:
        if 'email' in profile['properties']:
            hour, count = min(chain.from_iterable(profile['events'].itervalues()))
            year, week, day = datetime.utcfromtimestamp(hour * 3600).isocalendar()
            if year == 2013:
                weeks[(year, week)] += 1
            else:
                cum +=1
    data = sorted(weeks.items())[:-1]
    yield {'type': 'bar',
           'size': (12, 4),
           'data': data}
    yield {'type': 'line',
           'size': (12, 4),
           'data': list(cumulative(data, cum))}
    
Profiles().map(users).show()
