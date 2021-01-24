import requests


def retry(l):
    if str(input("Try again? [Y/N]")).lower() == "y":
        return runRequest(l)
    elif str(input("Try again? [Y/N]")).lower() == "n":
        return
    else:
        return retry(l)


def runRequest(l):
    try:
        r = requests.get(l, timeout=5)
        if r.status_code == 200:
            return r.text
        else:
            print('There was an error with accessing %s with error code %s retrieved' % (l, r.status_code))
    except:
        print('There was a timeout')
    finally:
        return retry(l)
