import sys
import pymongo

# Locations collection has the form:
#        'location': 'London',
#        'description': ['london'],
#        'isTaken': 0
#
# words collection has the form:
#        'word': 'something',
#        'count': 0

### Create seed data

SEED_DATA = [
    {
        'location': 'London',
        'description': ['london'],
        'isTaken': 0
    },
    {
        'location': 'Washington',
        'description': ['washington'],
        'isTaken': 0
    },
    {
        'location': 'Newyork',
        'description': ['newyork', 'new york', 'new-york', 'ny'],
        'isTaken': 0
    },
	{
        'location': 'Liverpool',
        'description': ['liverpool'],
        'isTaken': 0
    },
	{
        'location': 'Dublin',
        'description': ['dublin'],
        'isTaken': 0
    }
]
#-----------------------------------------------------------------------
# util functions

dbuser = 'test'
dbpassword = 'nnnn1858'
dbname = 'python_twitter'
host = 'ds121861.mlab.com'
port = 21861

def list_db(mydb, n=0):

    i = 0

    for doc in mydb.find():
        if (n > 0 and i>n): break
        i += 1
        print(doc)
		
 def connect_to_db():
    
    # Connect to data base
    connection = pymongo.MongoClient(host, port)
    db = connection[dbname]
    
    db.authenticate(dbuser, dbpassword)
    print('db', db)
    return db, connection   
###############################################################################
# main
###############################################################################

def main(args):

    db, connection = connect_to_db()
    locations = db['locations']
    print('locations', locations)
	
    # drop old location collection
    db.drop_collection('locations')
    
    locations.insert_many(LOCATION_DATA)
    print('locations', locations)
    print('==========================')

    list_locations(locations)
	
    cursor = db.locations.find({"isTaken": 0}) 

    print ('=========== data base =====================')
    for doc in cursor:
        print ('location %s is it taken ?  %d ' %
               (doc['location'], doc['isTaken']))
			   
    # query london location and make it taken
    for doc in db.locations.find(): print(doc) 
    
    query = {'location': 'London'}
    print('query', query)
	
    locations.update_one(query, {'$set': {'isTaken': 1}})

    list_db(locations)

    ### Only close the connection when your app is terminating

    connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])