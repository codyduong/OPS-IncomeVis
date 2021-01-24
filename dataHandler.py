import json
import csv


#For the curious, the JSON is formatted such that each employee is given their own unique key-name for easier accessing of specific employees.
def writeToJson(e, filename): 
    """
    Converts {employee: [Location, Position],...} to JSON
    """
    with open(filename, "w") as f:
        content = json.dumps(e, indent=4)
        f.write(content)
        #YML below
        # s = 'employees:\n\n'
        # for person in e:
        #     s += '- name: %s\n  location: %s\n  position: %s\n\n' % (person, e[person][0], e[person][1])
        # f.write(s)


#handles the funky way I store json to CSV, rather than standardized json
def writeWeirdJSONtoCSV(weirdJSON, filename):
    fields = ['name', 'location', 'position', 'category', 'income']
    rows = [] #--> [[Name, Location, Position, Income], ...]
    for name in weirdJSON:
        nD = weirdJSON[name] #nameDumped, because for some reason it thinks name == string. idk java explicit typecasting better smh
        rows.append([name, nD['location'], nD['position'], nD['category'], nD['income']])

    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

