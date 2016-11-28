from sqlalchemy import *
from sqlalchemy import create_engine
import datetime


# blacklist = Table('blacklist', metadata,
#                   Column('bl_term_id', Integer(), Sequence('blacklist_id_seq'), primary_key=True),
#                   Column('bl_term', String(55), unique=True, index=True),
#                   Column('reason_added', String(255)),
#                   Column('created_by', String(25), default='StreamerBot', nullable=False),
#                   Column('created_on', DateTime(), default=datetime.now()),
#                   Column('date_inactive', DateTime()),
#                   Column('active', Boolean(), default=True),
#                   Column('modified_by', String(), default='StreamerBot', nullable=False),
#                   Column('updated_on', DateTime(), default=datetime.now(), onupdate=datetime.now())
#                   )



db = create_engine('sqlite:///streamerDB.db')
metadata = MetaData(db)
connection = db.connect()
blacklist = Table('blacklist', metadata, autoload=True)
s = select([blacklist])
rp = connection.execute(s)

# pulling existing records from database
dbBlacklistTerms = []

print '[*] Loading current database track values...'

for record in rp:
    dbBlacklistTerms.append(record.bl_term)

# opening track file
print '[*] Opening blacklist file...'
blacklistfile = open('data/blacklist.txt', 'r')

print '[*] Comparing Database values to blacklist text file...'

itemcount = 0

# try to add new terms to the database
try:
    for term in blacklistfile:
        # strip all unnecessary characters from terms in track
        stripWhite = term.strip()
        stripNewLine = stripWhite.strip('\n')
        stripRLine = stripNewLine.strip('\r')
        newTerm = stripRLine.replace(',', '')

        # if the term is not in the database, add it
        if newTerm not in dbBlacklistTerms:
            itemcount = itemcount + 1
            systime = datetime.datetime.now()
            ins = blacklist.insert().values(
                bl_term = newTerm,
                reason_added = '14NOV2016 Update',
                created_by = 'StreamerBot',
                created_on = systime,
                active = True,
                modified_by = 'StreamerBot',
                updated_on = systime
            )

            # commit the changes
            result = connection.execute(ins)

except Exception as e:
    print "\n[!] Error Importing Blacklist Term: %s" % e

print '\n[*] Import Complete...'
print '[*] Added %s new terms...' % itemcount