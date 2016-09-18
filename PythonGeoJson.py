import json
import sqlite3
import codecs

conn = sqlite3.connect('geodata1.sqlite')
cursor = conn.cursor()

cursor.execute('SELECT * FROM Locations')
fhand = codecs.open('location.js', 'w', "utf-8")
fhand.write("myData = [\n") # "myData" will be used the html file
count = 0
for row in cursor:
    data = str(row[1])  #row in the databse has 0 (adress), 1(geodata)
    try:
        jsdata = json.loads(str(data))
        #print 'JSON', jsdata
    except:
        continue
# After the row of geodata is loaded as json data
# check the status

    if not ('status' in jsdata and jsdata['status'] == 'OK'):
        continue
    lattitude = jsdata["results"][0]["geometry"]["location"]["lat"] # [0] is list indices
    #print 'LAT' , lattitude
    longitude = jsdata["results"][0]["geometry"]["location"]["lng"]
    if lattitude == 0 or longitude == 0:
        continue
    location = jsdata['results'][0]['formatted_address']
    location = location.replace("'","")
    try:
        print location, lattitude, longitude

        count = count + 1
        if count > 1:   fhand.write(",\n")
        output = "["+str(lattitude)+", "+str(longitude)+", '"+location+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n]; \n")
cursor.close()
fhand.close()
print count, 'record written to location.js'
print "Open where.html to view the data in a browser"
