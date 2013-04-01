from bitdeli import Profiles, set_theme, Description, Title
from itertools import chain, groupby
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
        if year > 2012 and week > 1:
            p = 100. * float(count) / cum
            yield (year, week), p
        cum += count
    
def cumulative(data):
    cum = 0
    for (year, week), count in data:
        if True:
            t = datetime(year, 1, 1) + timedelta(weeks = week)     
            yield t.strftime('%Y-%m-%d'), cum
        cum += count

def new_users(data):
    def monthly():
        for (year, week), count in data:
            if year > 2012:
                yield datetime(year, 1, 1) + timedelta(weeks = week), count
    for month, counts in groupby(monthly(), lambda x: x[0]):
        counts = list(counts)
        print counts
        yield month.strftime('%B'), sum(count for month, count in counts)
            
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
           'size': (5, 4),
           'data': list(new_users(data))}
    yield {'type': 'bar',
           'label': 'Week-to-week growth',
           'size': (10, 4),
           'data': gdata}
    yield {'type': 'text',
           'size': (2, 2),
           'label': 'Average weekly growth',
           'data': {'head': '%.2f%%' % (sum(gdata.values()) / len(gdata))}}
    yield {'type': 'line',
           'size': (6, 4),
           'label': 'Total number of users',
           'data': list(cumulative(data))}
    
Profiles().map(users).show()
