from bitdeli import Profiles, set_theme, Description, Title
from itertools import chain
from collections import Counter
from datetime import datetime, timedelta

WINDOW = 48
text = {}

set_theme('playground')

def date(hour):
    return strftime('%B %d, %Y')

def growth(data):
    avg = []
    cum = 0
    for (year, week), count in data:
        if year > 2012:
            p = 100. * float(count) / cum
            yield (year, week), p
        cum += count
    
def cumulative(data):
    cum = 0
    for (year, week), count in data:
        if (year, week) > (2012, 50):
            t = datetime(year, 1, 1) + timedelta(weeks = week)     
            yield t.strftime('%Y-%m-%d'), cum
            cum += count
        
def users(profiles):
    weeks = Counter()
    for profile in profiles:
        if 'email' in profile['properties']:
            hour, count = min(chain.from_iterable(profile['events'].itervalues()))
            year, week, day = datetime.utcfromtimestamp(hour * 3600).isocalendar()
            weeks[(year, week)] += 1
    data = sorted(weeks.items())[:-1]
    gdata = dict(growth(data))
    yield {'type': 'bar',
           'label': 'New Users',
           'size': (12, 4),
           'data': filter(lambda x: x[0][0] > 2012, data)}
    yield {'type': 'bar',
           'label': 'Week-to-week growth',
           'size': (10, 4),
           'data': gdata}
    yield {'type': 'text',
           'size': (2, 2),
           'label': 'Average weekly growth',
           'data': {'head': '%.2f%%' % (sum(gdata.values()) / len(gdata))}}
    yield {'type': 'line',
           'size': (12, 4),
           'label': 'Total number of users',
           'data': list(cumulative(data))}
    
Profiles().map(users).show()
