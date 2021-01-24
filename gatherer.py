import json
import requester
import urllib.parse
from html.parser import HTMLParser


BASE_URL = 'https://govsalaries.com'
STATE = 'KS'
EMPLOYER = 'olathe'
# Fields to check
FIELDS = ('location', 'position', 'employer')
#https://govsalaries.com/search?employer=%s&year=%s&employee=%s&state=%s


class htmlParserSearch(HTMLParser):
    allPageLinks = None #formatted {pos: 'link', }
    returnMoney = None #formatted [($, link),($, link),...]
    employee = None

    def __init__(self, person):
        HTMLParser.__init__(self)
        self.allPageLinks = {}
        self.employee = person
        self.returnMoney = []

    def handle_starttag(self, tag, attrs):
        links = self.allPageLinks
        if str(tag) == 'a':
            # and not str(attrs[0][1] in ('/', '/jobs'))
            if str(attrs[0][0]) == 'href' and str(attrs[0][1]) not in ('/salaries/%s/%s' % (STATE, EMPLOYER), '/jobs', '/') :
                #print(attrs[0], self.getpos()[0])
                links[(self.getpos()[0])] = (str(attrs[0][1]))
        self.allPageLinks = links

    def handle_data(self, data):
        if str(data)[0] == '$':
            posLine = self.getpos()[0]
            lTC = self.allPageLinks
            if posLine in lTC:
                moneyInt = int(str(data).strip('$').replace(',',''))
                url = (BASE_URL + lTC[posLine])
                self.returnMoney.append((moneyInt, url))
                print('%s appended (%i, %s)' % (self.employee, moneyInt, lTC[posLine]))
                #print(self.allPageLinks, self.returnMoney)


def gatherFromJSON(j):
    """
    Takes JSON and runs the check through govsalaries.com
    """
    decoded = json.loads(j)
    employeeMoney = {}
    for person in decoded['employees']:
        #url = '%s/search?employer=%s&year=%i&employee=%s&state=%s' % (BASE_URL, 'olathe', 2018, urllib.parse.quote(person), 'KS')
        url = '%s/search?employer=%s&employee=%s&state=%s' % (BASE_URL, 'olathe', urllib.parse.quote(person), 'KS')
        #print(url)
        parser = htmlParserSearch(str(person))
        parser.feed(requester.runRequest(url))
        employeeMoney[str(person)] = parser.returnMoney
        
