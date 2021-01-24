import requests


def runRequest(l):
    r = requests.get(l)
    if r.status_code == 200:
        return r.text
    else:
        print('There was an error with accessing %s with error code %s retrieved' % (l, r.status_code))
        return


# def handleLink(d):
#     """
#     d - list of keys and keyvalues (dict)
#     returns a list of data, formatted in a list
#     """
#     r_list = {}
#     for school in d:
#         r = requests.get(d[school])
#         if r.status_code == 200:
#             r_list[school] = r.text
#         else:
#             print('There is an error with %s listing code: %s' % (d[school], r.status_code))
#             return 
#     return r_list