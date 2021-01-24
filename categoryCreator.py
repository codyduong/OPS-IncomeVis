#a script used to make the positions into several distinct categories
import json
import dataHandler


CATEGORIES = [
    'Adminstrative',
    'Grade-School',
    'Humanities', #history, archaeology, human geography, law, politics, religion, art
    'Art & Music',
    'Math & Science',
    'English/Foreign Languages',
    'Custodial & Food Services',
    'Support Staff', #other positions basically
    'Para/Assitive Teachers',
    'Physical Education'
]


def findCAT_KEY():
    try:
        with open('CAT_KEY.json') as f:
            return (json.loads(f.read()))
    except FileNotFoundError:
        return {}
    

def prompt(spPosition, CAT_STRING):
    try:
        return int(input("Where should the position: (%s) go?\n%s" % (spPosition, CAT_STRING))) -1
    except:
        if str(input("Error thrown, exit program [Y/N] (N will continue to prompt)")).lower == 'y':
            raise("Program exited")
        else:
            return prompt(spPosition, CAT_STRING)


def promptCategory(spPosition, ck):
    CAT_STRING = ''
    for i in range(1, len(CATEGORIES)+1):
        CAT_STRING += ("%s[%i]\n" % (CATEGORIES[i-1], i))
    val = prompt(spPosition, CAT_STRING)
    print("Position (%s) assigned to (%s)\n" % (spPosition, CATEGORIES[val]))
    ck[spPosition] = CATEGORIES[val]
    dataHandler.writeToJson(ck,"CAT_KEY.json")


def catergorize(j):
    ck = findCAT_KEY()
    jloaded = json.loads(j)
    for person in jloaded['employees']:
        #print(j['employees'][str(person)]['position']) for some reason person[] indiced wont want to work
        try:
            jloaded['employees'][str(person)]['category'] = ck[jloaded['employees'][str(person)]['position']]
            print('Autoconverted from %s to %s' % (jloaded['employees'][str(person)]['position'], ck[jloaded['employees'][str(person)]['position']]))
        except:
            promptCategory(j['employees'][str(person)]['position'], ck)
            jloaded['employees'][str(person)]['category'] = ck[jloaded['employees'][str(person)]['position']]

    #print(jloaded)
    return jloaded
            

if __name__ == "__main__":
    employeesRaw = None
    with open('employees.json') as f:
        employeesRaw = json.loads(f.read())
    if employeesRaw==None:
        raise("uh oh")

    catergorize(employeesRaw)
