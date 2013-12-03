import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )


import cogentviewer.models as models
from ..models import meta as meta
from ..models import user

Base = meta.Base
#DBSession = meta.Session()


import getpass
import transaction


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)


def populateUser():
    """
    Add a new user to the system
    """
    session = meta.Session()
    
    
    newUser = raw_input("Login Name: ")
    userEmail = raw_input("User Email: ")
    passOne = "FOO"
    passTwo = "BAR"
    while passOne != passTwo:
        passOne = getpass.getpass()
        passTwo = getpass.getpass("Repeat Password: ")
        if passOne != passTwo:
            print "Passwords do not match"
        
    #Setup a new User
    thisUser = user.User(username=newUser,
                         email=userEmail,
                         password=meta.pwdContext.encrypt(passOne),
                         level="user"
                         )
    session.add(thisUser)
    session.flush()
    transaction.commit()


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    meta.Session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    DBSession = meta.Session()
    #DBSession.configure(bind=engine)
    
    #populateData.init_data(DBSession)
    populateUser()