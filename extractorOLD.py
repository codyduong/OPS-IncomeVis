from html.parser import HTMLParser
import requests

"""
DEPRECATED
"""


BASE_URL = 'https://www.olatheschools.org'
#LINKS = ['%s/domain/2402' % (BASE_URL)]
LINKS = {
    #'Olathe Northwest': '%s/domain/2402' % (BASE_URL),
    'Olathe North': '%s/domain/2611' % (BASE_URL)
}

#dept keywords
DEPARTMENTS = { #better than running through a linked list
    'Administration': True,
    'Academic Specialists': True,
    'AVID': True,
    'Art': True,
    'Business & Computers': True,
    'Family and Consumer Science': True,
    'Family & Consumer Science': True,
    'Language Arts': True,
    'Library Media Center': True,
    'Mathematics': True,
    'Performing Arts': True,
    'Physical Education': True,
    'Science': True,
    'Social Studies': True,
    'Technology Education': True,
    'World Languages': True,
    'Support Staff': True,
} #21st not included

def handleLinks(d):
    """
    d - list of keys and keyvalues (dict)
    returns a list of data, formatted in a list
    """
    r_list = {}
    for school in d:
        r = requests.get(d[school])
        if r.status_code == 200:
            r_list[school] = r.text
        else:
            print('There is an error with %s listing code: %s' % (d[school], r.status_code))
            return 
    return r_list


class htmlParserBase(HTMLParser):
    """
    Handles the parsing of the main webpages used by our school in the faculty directories. Basically searches for these tags:
    <a href = "/Page/####" ... ...>DEPT TITLE</a>, and then returns it in the format: {'DEPT TITLE': 'LINK'} in a dictionary
    for later use by the rest of the program
    """
    linksToCheck = {} #formatted {pos: 'link', }
    departmentLinks = {} #formatted {'deptName': 'link', }

    def handle_starttag(self, tag, attrs):
        links = self.linksToCheck
        if str(tag) == 'a':
            if str(attrs[0][0]) == 'href':
                print(attrs[0], self.getpos()[0])
                links[(self.getpos()[0])] = (str(attrs[0][1]))
        self.linksToCheck = links

    def handle_data(self, data):
        if str(data) in DEPARTMENTS:
            print(str(data))
            posLine = self.getpos()[0]
            lTC = self.linksToCheck
            if posLine in lTC:
                self.departmentLinks[str(data)] = '%s%s' % (BASE_URL, lTC[posLine])
                self.linksToCheck.pop(posLine)
            print(data, self.getpos()[0])

class htmlParserDepartments(HTMLParser):
    """
    Parses the employees in each Department, then can return the employee name and position
    """
    print()


if __name__ == "__main__":
    dataList = (handleLinks(LINKS))
    employees = {}
    for school in dataList:
        parser = htmlParserBase()
        parser.feed(dataList[school])
        for each in parser.departmentLinks:
            print(school, each, parser.departmentLinks[each])