from CommonServerPython import *
from CommonServerUserPython import *
from itertools import cycle

# Executes confluera-login command/script
login_data = demisto.executeCommand('confluera-login', {})
token = login_data[0]['Contents']['access_token']


# Executes confluera-fetch-detections command/script
detections_data = demisto.executeCommand('confluera-fetch-detections', {'access_token': token, 'hours': '24'})
detections = detections_data[1]['Contents']

# Generating Chart data
data: List[Dict] = []
colors = cycle([
    '#dc5e50',
    '#64bb18',
    '#8b639a',
    '#d8a747',
    '#528fb2',
    '#9cc5aa',
    '#f1934c',
    '#e25b4c',
    '#5bbe80',
    '#c0363f',
    '#cdb8a8',
    '#3cc861'])
for idx, ioc in enumerate(detections):
    element = [item for item in data if item['name'] == ioc['iocTactic']]

    if element and len(element) != 0:
        element[0]['data'][0] += 1
    else:
        chart_item = {
            "name": ioc['iocTactic'],
            "data": [1],
            "color": next(colors)
        }
        data.append(chart_item)

demisto.results({
    "Type": 17,
    "ContentsFormat": "pie",
    "Contents": {
        "stats": data
    }
})
