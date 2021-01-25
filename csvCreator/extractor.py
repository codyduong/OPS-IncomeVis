"""
This file parses the mhtml and converts it to a json of employees
"""
from html.parser import HTMLParser
import json
import dataHandler
import categoryCreator


JSON_STORE = None


def parseContent():
    """
    Reformats to a more friendly htmlParser format
    """
    content = ''
    with open("directory.mhtml") as f:
        lines = f.readlines()
        stored = ''
        for line in lines:
            lineS = line.strip()
            if stored == '':
                if lineS != '' and lineS[-1] == "=":
                    stored = lineS.strip('=')
                else:
                    content += ('%s' % lineS)
            else:
                lineS = stored+lineS
                stored = ''
                content += (lineS)

    return content


class htmlParser(HTMLParser):
    posConfirm = {}  # lists pos where <td class=3D"xform"> exists
    employees = {}
    """
    {
    employee: [Location, Position],
    }
    """
    employee = None
    location = None
    position = None

    def handle_starttag(self, tag, attrs):
        try:
            if str(tag) == "td" and attrs[0]:
                #print(attrs[0], self.getpos())
                self.posConfirm[self.getpos()[0]] = True
        except:
            pass

    def handle_data(self, data):
        if self.getpos()[0] in self.posConfirm:
            #print(data)
            #There are employees without email/phone, so instead I just opted to remove that entirely, since I don't need it. Also because properly handling it
            #wont work with the limitations of the htmlparser, unless I devise some way to find empty data fields.
            if len(data.split('@')) == 2:
                return
            elif len(data.split('-')) == 3:
                # apparently there's people out there with 2 hyphens in their name, so this is the weirdest edgecase i've had to code in. (Anne-Marie Bixler-Funk)
                try:
                    if int(data.split('-')[0]):
                        return
                except:
                    pass

            if self.employee == None:
                self.employee = data
            elif self.location == None:
                self.location = data
            elif self.position == None:
                self.position = data
                self.employees[self.employee] = {'location': self.location, 'position': self.position}
                self.employee, self.location, self.position = None, None, None


if __name__ == "__main__":
    parser = htmlParser()
    parser.feed(parseContent())
    dumped = json.dumps({'employees': parser.employees}, indent=4)
    undumped = categoryCreator.catergorize(JSON_STORE)
    dataHandler.writeToJson(JSON_STORE, "employees.json") #this redumps it
    print("Exported to JSON") #dumped
else:
    parser = htmlParser()
    parser.feed(parseContent())
    JSON_STORE = json.dumps({'employees': parser.employees}, indent=4)
    JSON_STORE = json.dumps(categoryCreator.catergorize(JSON_STORE), indent=4)
    print("Passing JSON") #dumped