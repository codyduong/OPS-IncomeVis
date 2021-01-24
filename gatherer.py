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
    allPageLinks = {} #formatted {pos: 'link', }
    finalList = {} #formatted {'employee': [($, link),($, link),...]}
    employee = None

    def __init__(self, person):
        HTMLParser.__init__(self)
        self.employee = person

    def handle_starttag(self, tag, attrs):
        links = self.allPageLinks
        if str(tag) == 'a':
            if str(attrs[0][0]) == 'href' and str(attrs[0][1]) != '/salaries/%s/%s' % (STATE, EMPLOYER): #and not str(attrs[0][1] in ('/', '/jobs'))
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
                        print('%s appended (%i, %s)' % (self.employee, moneyInt, lTC[posLine])) #the print command uses the less verbose url for the sake of me
                        #print(self.finalList[self.employee])
                        self.finalList[self.employee].append((moneyInt, url))
                except:
                    print('%s first link (%i, %s)' % (self.employee, moneyInt, lTC[posLine]))
                    self.finalList[self.employee] = [(moneyInt, url)]
                finally:
                    self.allPageLinks.pop(posLine)
                    #print(data, self.getpos()[0])


def gatherFromJSON(j):
    """
    Takes JSON and runs the check through govsalaries.com
    """
    decoded = json.loads(j)
    for person in decoded['employees']:
        #url = '%s/search?employer=%s&year=%i&employee=%s&state=%s' % (BASE_URL, 'olathe', 2018, urllib.parse.quote(person), 'KS')
        url = '%s/search?employer=%s&employee=%s&state=%s' % (BASE_URL, 'olathe', urllib.parse.quote(person), 'KS')
        #print(url)
        parser = htmlParserSearch(str(person))
        parser.feed(requester.runRequest(url))
        
