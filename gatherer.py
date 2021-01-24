import json
import requester
import urllib.parse
import time
from html.parser import HTMLParser


BASE_URL = 'https://govsalaries.com'
STATE = 'KS'
EMPLOYER = 'olathe'
# Fields to check
FIELDS = ('location', 'position', 'employer')
#https://govsalaries.com/search?employer=%s&year=%s&employee=%s&state=%s


class htmlParserSearch(HTMLParser):
    allPageLinks = None #formatted {pos: 'link', }
    finalList = {} #formatted {'employee': [($, link),($, link),...]}
    employee = None

    def __init__(self, person):
        HTMLParser.__init__(self)
        self.allPageLinks = {}
        self.employee = person
        self.returnMoney = []

    def resetParser(self):
        self.allPageLinks = {}
        self.employee = None
        self.returnMoney = []

    def setEmployee(self, s):
        self.employee = s

    def handle_starttag(self, tag, attrs):
        links = self.allPageLinks
        if str(tag) == 'a':
            # and not str(attrs[0][1] in ('/', '/jobs'))
            if str(attrs[0][0]) == 'href' and str(attrs[0][1]) not in ('/salaries/%s/%s' % (STATE, EMPLOYER), '/jobs', '/'):
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
                try:
                    if self.finalList[self.employee]:
                        print('%s appended (%i, %s)' %
                              (self.employee, moneyInt, lTC[posLine]))
                        #print(self.finalList[self.employee])
                        self.finalList[self.employee].append((moneyInt, url))
                except:
                    print('%s first link (%i, %s)' % (self.employee, moneyInt, lTC[posLine]))
                    self.finalList[self.employee] = [(moneyInt, url)]
                finally:
                    self.allPageLinks.pop(posLine)
                    #print(data, self.getpos()[0])


#new and improved, I can't believe it's not butter
#this function is a WIP, but parses more info, which means we won't be doing unnecessary searches of unavailable data points
class htmlParserFast(HTMLParser):
    allPageLinks = None #formatted {pos: 'link',...}
    allMoney = None #formatted {pos: 'link',...}
    finalList = {} #formatted {'employee': [($, link),($, link),...]}
    employeeList = None

    def __init__(self, List):
        HTMLParser.__init__(self)
        self.allPageLinks = {}
        self.allMoney = {}
        self.employeeList = List
        self.returnMoney = []

    def resetParser(self):
        self.allPageLinks = {}
        self.allMoney = {}
        self.returnMoney = []

    def handle_starttag(self, tag, attrs):
        links = self.allPageLinks
        if str(tag) == 'a':
            if str(attrs[0][0]) == 'href' and str(attrs[0][1]) not in ('/salaries/%s/%s' % (STATE, EMPLOYER), '/jobs', '/') :
                links[(self.getpos()[0])] = (str(attrs[0][1]))
        self.allPageLinks = links

    def handle_data(self, data):
        if str(data)[0] == '$':
            pass
        try:
            if self.employeeList[str(data).lower()]:
                pass
        except:
            pass


def gatherFromJSON(j):
    """
    Takes JSON and runs the check through govsalaries.com
    """
    decoded = json.loads(j)
    parser = htmlParserSearch(None)
    times = [0, 0] #formatted [timeTotal, iterations]

    # Highly inefficient that makes over 2000 requests to govsalaries
    # Currently still in use because the other method requires more coding... and idk if i want to do it.
    for person in decoded['employees']:
        #url = '%s/search?employer=%s&year=%i&employee=%s&state=%s' % (BASE_URL, EMPLOYER, 2018, urllib.parse.quote(person), STATE)
        url = '%s/search?employer=%s&employee=%s&state=%s' % (BASE_URL, EMPLOYER, urllib.parse.quote(person), STATE)
        #print(url)
        s = time.time()
        parser.setEmployee(str(person))
        parser.feed(requester.runRequest(url))
        parser.reset()
        times[0] += time.time()-s
        times[1] += 1
        print(times[0]/times[1]) #~.5 second for 2000 searches, meaning ~16 minutes for the whole program to run

    """
    PAGE_LIMIT = 41 #hardcoded because it was ez pz
    for i in range(1, PAGE_LIMIT): 
        url = '%s/salaries/%s/%s?year=%i&page=%i' % (BASE_URL, STATE, EMPLOYER, 2018, i)
    """