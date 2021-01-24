import requests


def runRequest(l):
    r = requests.get(l)
    if r.status_code == 200:
        return r.text
    else:
        print('There was an error with accessing %s with error code %s retrieved' % (l, r.status_code))
        return