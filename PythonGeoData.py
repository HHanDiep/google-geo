import urllib
import json
import sqlite3
import time
import ssl

serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"

scontext = None

conn = sqlite3.connect('geodata1.sqlite')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)
''')

fhand = open ('where.data') # short for fname = ('where.data')
                                      # fhand = open(fname)
count = 0
for line in fhand:
    if count > 205:
        break
    address = line.strip()

    cursor.execute("SELECT geodata FROM Locations WHERE address = ?", (buffer(address), ))
    try: # check to see if this location in is the database if not then it will call google geocode for locations
        data = cursor.fetchone()[0] # give me one row (fetchone),
                                # the row is a list of thing,
                                # and the zero item is geodata because we only select 1 thing SELECT geodata
        print "Found in database " , address #
        continue
    except:
        pass
        #print 'No geodata found in database'

    print 'Resolving', address

    url = serviceurl + urllib.urlencode({'sensor' : 'false', 'address' : address})
    print 'Retrieving' , url

    urlhandle = urllib.urlopen(url , context=scontext)


    data = urlhandle.read()
    #data = data.split()
    print 'Retrieved' , len(data), 'charater', data[:20] # .replace('\n',' ') #, '\n' # print out the first 20 characters
                                                                            # and replace /n (newline) with space
    count = count +1

    try: # this step is to check to see if it's good data or not
        jsdata = json.loads(str(data))
         # converting the data to string in case it's Unicode
        #print jsdata
    except: # if try doesn't work then blow off and continue -> nothing we can do because of bad Json
        continue

    if 'status' not in jsdata or (jsdata['status'] != 'OK' and jsdata['status'] != 'ZERO_RESULTS'):
        print '=== Failure to retrieve ==='
        print data
        break # this step is to stop the program if sth goes wrong , so you can go in and fix it

    cursor.execute('''INSERT INTO Locations (address, geodata)
                    VALUES (?,?)''' ,(buffer(address), buffer(data) ))
    conn.commit() # Commit stay in the loop so you dont lose previous dat if program crashes
    time.sleep(1)
print "Run geodump.py to read the data from the database so you can visualize it on a map."
