import csv
import urllib.request
from bs4 import BeautifulSoup
import time

csvout = csv.writer(open("venmo.csv", "a"))
#csvout.writerow(['name1', 'name2', 'message'])

baseurl = "https://venmo.com/api/v5/public?since=1476921600&until=1476921660&limit=1000000"

#time.sleep(30)

with urllib.request.urlopen(baseurl) as response:
    html = response.read()

bigstring = html.decode('ASCII')

bigstringlist = bigstring.split(",")
print(bigstringlist)
finalstring = []
for x in bigstringlist:
    if "username" in x:
        if "actor" in x:
            x = x.replace('\"', '')
            spaceindex = x.rfind(' ')
            finalstring.append("\n actor:" + x[spaceindex:])
            print(finalstring)
            print(type(finalstring))
            exit()
        if "transactions" in x:
            x = x.replace('\"', '')
            spaceindex = x.rfind(' ')
            finalstring.append("target:" + x[spaceindex:])

print(finalstring)
exit()
csvout.writerow(finalstring)