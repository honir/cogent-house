import logging
logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO,filename="push.log")

__version__ = "0.3.1"

"""
Modified version of the push script that will fetch all items,
convert to JSON and (eventually) transfer across REST

This replaces the ssh tunnel database access curretly used to transfer samples.

However, for the moment syncronising the Locations etc (or the complex bit) is
still done via SQLA. As this takes a fraction of the transfer time its probably
a good idea to leave it.



    .. warning::

        This will fail if the database type is SQ-Lite, currently a connection
        cannot issue a statement while another is open.  Therefore the loop
        through the readings, appending new items fails with a DATABASE LOCKED
        error.

        I am at a loss of what to do to fix this.  However, as we will be
        pushing to mySQL, its not really a problem except for some test cases

    .. note::

        I currently add 1 second to the time the last sample was transmitted,
        this means that there is no chance that the query to get readings will
        return an item that has all ready been synced, leading to an integrity
        error.

        I have tried lower values (0.5 seconds) but this pulls the last synced
        item out, this is possibly a error induced by mySQL's datetime not
        holding microseconds.

    .. warning::

       In My experience you may need to bugger about with connection strings
       Checking either Localhost or 127.0.0.1 Localhost worked on my machine, my
       connecting to Cogentee wanted 127.0.0.1

    .. since 0.1::

       Moved ssh port forwarding to paramiko (see sshclient class) This should
       stop the errors when there is a connection problem.

    .. since 0.2::

       * Better error handling
       * Pagination for sync results, transfer at most PUSH_LIMIT items at a
         time.

    .. since 0.3::

       Moved Nodestate Sync into the main readings sync class, this should stop
       duplicate nodestates turning up if there is a failiure

    .. since 0.4::

       Overhall of the system to make use of REST to upload samples rather than
       transfer data across directly.

    .. since 0.5::

       Make use of an .ini style config file to set everything up

       Split functionalility into a Daemon, and Upload classes.  This should
       make maintainance of any local mappings a little easier to deal with.
"""

import sqlalchemy
import remoteModels

import cogent
import cogent.base.model as models
import cogent.base.model.meta as meta
from datetime import datetime
from datetime import timedelta

import subprocess

import paramiko
import sshClient
import threading
import socket

import time

import ConfigParser
#To Parse Configuration files
#import cfgparse
import configobj
import os

import dateutil.parser

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
#log.setLevel(logging.INFO)

#Reset Paramiko logging to reduce output cruft.
plogger = paramiko.util.logging.getLogger()
plogger.setLevel(logging.WARNING)

#URL of local database to connect to
LOCAL_URL = 'mysql://test_user:test_user@localhost/pushSource'
PUSH_LIMIT = 5000 #Limit on samples to transfer at any one time
SYNC_TIME = 60*10  #How often we want to call the sync (Every 10 Mins)

#RSA KEY
RSA_KEY = None
#RSA_KEY = "/home/dang/.ssh/id_rsa.pub"
RSA_KEY = "/home/dang/.ssh/work_key.pub"

#Knwon Hosts file
KNOWN_HOSTS = None
KNOWN_HOSTS = "/home/dang/.ssh/known_hosts"


class PushServer(object):
    """
    Class to deal with pushing updates to a group of remote databases

    This class is designed to be run as a daemon, managing a group of individual
    pusher objects, and facilitating the transfer of data between remote and
    local DB's
    """

    def __init__(self,localURL=None):
        """Initialise the push server object

        This should:

        #. Create a connection to the local database,
        #. Read the Configuration files.
        #.Setup Necessary Pusher objects for each database that needs
          synchronising.

        :var localURL:  The DBString used to connect to the local database.
                        This can be used to overwrite the url in the config file
        """

        log.info("Initialising Push Server")


        #Read the Configuration File
        generalConf,locationConfig = self.readConfig()

        #Store the config
        self.generalConf = generalConf

        if not localURL:
            localURL = generalConf["localUrl"]

        log.debug("Connecting to local database at {0}".format(localURL))

        #Initalise the local database connection
        log.debug("Initalise Session for {0}".format(localURL))
        engine = sqlalchemy.create_engine(localURL)
        models.initialise_sql(engine)
        localSession = sqlalchemy.orm.sessionmaker(bind=engine)
        self.localSession = localSession



        #Create a new Pusher object for this each item given in the config
        syncList = []
        for item in locationConfig:
            syncList.append(Pusher(localSession,item))

        self.syncList = syncList
        #self.theConfig = theConfig

    def readConfig(self):
        """Read configuration from the config file.

        This will parse the synchronise.conf file, and produce a local
        dictionary of all objects that need synchronising.

        :return: A dictionary of parameters (as a list) where syncronisation is
        required
        """

        confParser = configobj.ConfigObj("synchronise.conf")
        log.debug("Processing Config File")

        #Dictionary to return
        syncDict = {}

        generalOpts = confParser["general"]


        #Get the Locations
        locations = confParser["locations"]

        for loc in locations:
            isBool = locations.as_bool(loc)
            log.debug("--> Processing Location {0} {1}".format(loc,isBool))
            if isBool:
                items = confParser[loc]
                if items.get("lastupdate",None) in [None,"None"]:
                    items["lastupdate"] = None
                else:
                    #We need to parse the last time
                    theTime = dateutil.parser.parse(items["lastupdate"])
                    items["lastupdate"] = theTime
                syncDict[loc] = items
        # #Get the URLS we need to deal with
        # syncItems = confParser.items("locations")
        # syncDict = {}
        #confParser.write()
        self.confParser = confParser
        return generalOpts,syncDict


    def sync(self):
        """
        Run one instance of the synchroniseation mechnism,

        For each item in the config file, perform synchronisation.

        :return: True on success,  False otherwise
        """
        for item in self.syncList:
            log.debug("Synchronising {0}".format(item))




class Pusher(object):
    """Class to push updates to a remote database.

    This class contains the code to deal with the nuts and bolts of syncronising
    remote and local databases

    """

    def __init__(self,localSession,config):
        """Initalise a pusher object

        :param localSession: A SQLA session, connected to the local database
        :param config: Config File options for this particular pusher object
        """

        self.localSession = localSession
        self.config = config


    def sync(self):
        """
        Perform one synchronisation step for this Pusher object

        :return: True if the sync is successfull, False otherwise
        """

        config = self.config
        log.debug("Sync with config {0}".format(config))

        return

        #First off create the ssh tunnel
        theTunnel = self._startTunnel(value)
        if theTunnel:
            server,ssh = theTunnel
        else:
            log.warning("Unable to Sync")
            return
    #    value["lastupdate"] = datetime.now()

        #We can then Initialise the remote Location
        self.initRemote(value["dbstring"])

        #Things to do, First we want to synchronise all Nodes
        #self.syncNodes()

        #Sync Deployment / House / Location etc
        self.mapLocations(value["lastupdate"])
        #Sync Node States

        #Sync Readings

        #And run a test query

        #rSession = self.RemoteSession()
        #qry = rSession.query(models.RoomType).all()
        #for item in qry:
        #    print item

        log.debug("Shutting Down")
        server.shutdown()
        server.socket.close()
        ssh.close()


    def syncOld(self):
        """Main loop for Synchronisation"""
        log.debug("="*50)
        log.debug("Synchronising Data")
        session = self.LocalSession()
        syncDict = self.readConfig()
        import pprint
        pprint.pprint(syncDict)

        
        #return

        #And try to update something
        for key,value in syncDict.iteritems():
            log.debug("SYNC DICT ITEM {0}".format(value))
            
        #     #First off create the ssh tunnel
        #     theTunnel = self._startTunnel(value)
        #     if theTunnel:
        #         server,ssh = theTunnel
        #     else:
        #         log.warning("Unable to Sync")
        #         return
        # #    value["lastupdate"] = datetime.now()
        
        #     #We can then Initialise the remote Location
        #     self.initRemote(value["dbstring"])

        #     #Things to do, First we want to synchronise all Nodes
        #     #self.syncNodes()

        #     #Sync Deployment / House / Location etc
        #     self.mapLocations(value["lastupdate"])
        #     #Sync Node States

        #     #Sync Readings

        #     #And run a test query
            
        #     #rSession = self.RemoteSession()
        #     #qry = rSession.query(models.RoomType).all()
        #     #for item in qry:
        #     #    print item

        #     log.debug("Shutting Down")
        #     server.shutdown()
        #     server.socket.close()
        #     ssh.close()

        #pprint.pprint(syncDict)
        #self.confParser.write()

    def mapLocations(self,lastUpdate = None):
        """Syncronise Locations
        
        This functions attempts to map the locations on the local server, to
        those on the remote server
        
        ..param:: lastUpdate timestamp of the last update
        ..return:: Dictionaty of [<local>] :<remote> pairs

        We start by examining the database for all Deplyoments / Houses that do
        not have a finish date.  Or those where the finish date is after the
        last update.  This should ensure that only properties that need updating
        will be transfered.
        
        """

        #Really the Houses, Deployments and Rooms are immaterial, BUT we need to
        #update them to build a location
        mappedDeployments = {}
        mappedHouses = {}
        mappedRooms = {}
        mappedLocations = {}

        lSess = self.LocalSession()
        rSess = self.RemoteSession()

        log.debug("Filtering Deployments based on {0}".format(lastUpdate))

        #Get the list of deployments that may need updating
        updateDeployments = lSess.query(models.Deployment)
        if lastUpdate:
            updateDeployments = updateDeployments.filter(sqlalchemy.or_(models.Deployment.endDate >= lastUpdate,
                                                                        models.Deployment.endDate == None))

        #Rather than use sqla tunneling, this may be a great oppotunity to use REST.GET statements
        log.debug("Deployments to update:")
        for item in updateDeployments:
            #Make the assumption that all deplyoments will have unique names
            rItem = rSess.query(remoteModels.Deployment).filter_by(name=item.name).first()
            if rItem is None:
                log.debug("--> No Item Exists, Creating")
                rItem = remoteModels.Deployment(name=item.name)
                rSess.add(rItem)
            #While we are at it we can update the rest of the parameters
            rItem.description = item.description
            rItem.startDate = item.startDate
            rItem.endDate = item.endDate

            log.debug("--> {0} ## {1}".format(item,rItem))
            mappedDeployments[item.id] = rItem

        #We could fetch the houses by associating with each deployment, BUT it
        #can be possible for a house not to have a parent deployment (when using
        #the old myISAM engine) Therefore we fetch the houses here

        #It is probably a good idea to do a flush here
        rSess.flush()
        
        #import pprint
        #print "="*20
        #pprint.pprint(mappedDeployments)
        #print "="*20

        updateHouses = lSess.query(models.House)
        if lastUpdate:
            updateHouses = updateHouses.filter(sqlalchemy.or_(models.House.endDate >= lastUpdate,
                                                              models.House.endDate == None))

        #Houses we can make unique by linking to a deployment
        log.debug("Houses to update:")
        for item in updateHouses:
            log.debug("--> {0}".format(item))
            rItem = rSess.query(remoteModels.House).filter_by(address= item.address,
                                                              deploymentId = mappedDeployments[item.deploymentId].id).first()
            if rItem is None:
                log.debug("No Item Exists, Creating")
                rItem = remoteModels.House(address = item.address,
                                           deploymentId = mappedDeployments[item.deploymentId].id)
            #And update any other parameters
            rItem.startDate = item.startDate
            rItem.endDate = item.endDate

            mappedHouses[item.id] = rItem

        #After that we want to get all locations assoicated with a House
        houseIds = [x.id for x in updateHouses]


        updateLocations = lSess.query(models.Location)
        log.debug("Total Locathons {0}".format(updateLocations.count()))
        #Filter by the houses we need to update
        updateLocations = updateLocations.filter(models.Location.houseId.in_(houseIds))

        #We put off adding locations for the moment, instead making sure that we have the rooms sorted correctly
            
        #And all the rooms associated with a location
        locationIds = set([x.roomId for x in updateLocations])
        log.debug(locationIds)
        updateRooms = lSess.query(models.Room)
        updateRooms = updateRooms.filter(models.Room.id.in_(locationIds))

        log.debug("Filtered Rooms")
        for item in updateRooms:
            log.debug("--> {0}".format(item))
        
        #And Room Types
        roomTypeIds = set([x.roomTypeId for x in updateRooms])
        updateRoomTypes = lSess.query(models.RoomType).filter(models.RoomType.id.in_(roomTypeIds))
        
        log.debug("Filtered Room Types")
        for item in updateRoomTypes:
            log.debug("--> {0}".format(item))


        log.debug("Filtered Locations {0}".format(updateLocations.count()))
        for item in updateLocations:
            log.debug("--> {0}".format(item))
                
        #updateDeployments = lSess.query(remoteModels.Deployment).filter(sqlalchemy._or(remoteModels.Deployment.
        
        #Get the list of Houses that need updating.


    def _startTunnel(self,locDict):
        """Start an ssh tunnel based on parametrs given in locDict
        
        .. param:: locDict Dictionary of values as per config file
        """

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        #Try to load the known Hosts file
        dotSSH = locDict["sshfolder"]
        rsa = locDict["sshkey"]
        knownHosts = os.path.join(dotSSH,"known_hosts")
        rsaKey = os.path.join(dotSSH,rsa)
        log.debug("--> Known Hosts {0}".format(knownHosts))
        log.debug("--> Key {0}".format(rsaKey))
        ssh.load_host_keys(knownHosts)

        try:
            ssh.connect(locDict["url"],username=locDict["sshuser"],key_filename=rsaKey)
        except socket.error,e:
            log.warning("Connection Error {0}".format(e))
            return None
        except paramiko.AuthenticationException:
            log.warning("Authentication error")
            return None
        
        log.debug("Connection Ok")
        transport = ssh.get_transport()

        #Next setup tunnelling
        server = sshClient.forward_tunnel(3307,"127.0.0.1",3306,transport)
        serverThread = threading.Thread(target=server.serve_forever)
        serverThread.daemon = True
        serverThread.start()        
        return server,ssh
        
    # def syncOLD(self):
    #     """Main Loop for Synchronisation"""
    #     #For Each remote connection
    #     log.debug("Sync Data")
    #     session = self.LocalSession()
    #     theQry = session.query(models.UploadURL)
    #     #theQry = theQry.filter_by(url="dang@127.0.0.1")
        
    #     session.close()
    #     for syncLoc in theQry[-1:]:
    #         startTime = time.time()
    #         log.info("-------- Sync Nodes for {0} ----------------".format(syncLoc))
    #         sshUrl = syncLoc.url
    #         self.currentUrl = sshUrl
    #         log.debug("SSH URL: {0}".format(sshUrl))
    #         log.info("--> Creating SSH Tunnel {0}".format(sshUrl))
    #         ssh = paramiko.SSHClient()
    #         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #         if KNOWN_HOSTS:
    #             ssh.load_host_keys(KNOWN_HOSTS)
                
            
    #         user,host = sshUrl.split("@")
    #         #Connection
    #         try:
    #             ssh.connect(host,username=user,key_filename=RSA_KEY)
    #         except socket.error,e:
    #             log.warning("Connection Error {0}".format(e))
    #             break
    #         except paramiko.AuthenticationException:
    #             log.warning("Authentication Error")
    #             break

    #         log.debug("Connection Ok")
    #         transport = ssh.get_transport()
    
    #         # #Next setup tunnelling
    #         server = sshClient.forward_tunnel(3307,"127.0.0.1",3306,transport)
    #         serverThread = threading.Thread(target=server.serve_forever)
    #         serverThread.daemon = True
    #         serverThread.start()
            
    #         tunnelTime = time.time()
    #         log.info("--> Initialise Remote Connection")
    #         dburl = syncLoc.dburl
    #         log.debug("--> {0}".format(dburl))
    #         #time.sleep(5)
    #         #raw_input("Key to Continue")

    #         #We need to wait for the connection to come update
    #         self.initRemote(syncLoc)
    #         remoteTime = time.time()


            
    #         log.debug("--> Synchronising Objects")
    #         log.debug("-->--> Nodes")
    #         try:
    #             self.syncNodes()
    #         except sqlalchemy.exc.OperationalError,e:
    #             log.warning(e)
    #             server.shutdown()
    #             server.socket.close()
    #             ssh.close()
    #             break

    #         nodeTime = time.time()
    #         log.info("Nodes Synced")
                
    #         # log.debug("-->--> State")
    #         # #Synchronise State
    #         # try:
    #         #     self.syncState()
    #         # except sqlalchemy.exc.OperationalError,e:
    #         #     log.warning(e)
    #         #     server.shutdown()
    #         #     server.socket.close()
    #         #     ssh.close()
    #         #     break


    #         # #Synchronise Readings
    #         # log.debug("-->--> Readings")
    #         try:
    #             needsSync = True #Simple Pagination
    #             count = 0
    #             while needsSync:
    #                 needsSync = self.syncReadings()
    #                 if count > 2:
    #                     needsSync = False
    #                 count+= 1
    #         except sqlalchemy.exc.OperationalError,e:
    #             log.warning(e)
    #             server.shutdown()
    #             server.socket.close()
    #             ssh.close()
    #         #     break
    #         readingTime = time.time()

    #         server.shutdown()
    #         server.socket.close()
    #         ssh.close()
    #         endTime = time.time()
    #         time.sleep(1) #Let things settle down
    #         profileLog.debug("{},{},{},{},{},{},{},{}".format(sshUrl,
    #                                                        startTime,
    #                                                        endTime,
    #                                                        endTime - startTime,
    #                                                        tunnelTime - startTime,
    #                                                        remoteTime - startTime,
    #                                                        nodeTime - startTime,
    #                                                        readingTime - startTime))
        #End Location

    def initRemote(self,remoteUrl):
        """Initialise a connection to the database and reflect all Remote Tables

        :param remoteUrl:  a :class:`models.remoteURL` object that we need to connect to

        Timeout code may not be necessary (if we have a decent connection)
        But trys to address the following problem.
        1) Database is not available on connect [FAILS GRACEFULLY]
        
        2) Database is there on connect:
           Database / Network goes away during query [HANGS]

        I hope that putting a timeout on the querys will fix this.


        .. since:: 0.3  
            Connection timeout added.  
        """

        RemoteSession = sqlalchemy.orm.sessionmaker()

        self.rUrl = remoteUrl
        #log.info("Initialising Remote Engine {0}".format(remoteUrl.dburl))

        #engine = sqlalchemy.create_engine(remoteUrl.dburl)
        engine = sqlalchemy.create_engine(remoteUrl)
        log.debug("--> Engine {0}".format(engine))
        RemoteSession.configure(bind=engine)
        RemoteMetadata = sqlalchemy.MetaData()
        
        
        log.debug("Reflecting Remote Tables")
        remoteModels.reflectTables(engine,RemoteMetadata)
        self.RemoteSession=RemoteSession
        

    # ------------------ MOVED TO GLOBAL CLASS
    # def initLocal(self,engine):
    #     """Initialise a local connection"""
    #     log.debug("Initialising Local Engine")
    #     models.initialise_sql(engine)
    #     LocalSession = sqlalchemy.orm.sessionmaker(bind=engine)
    #     self.LocalSession = LocalSession


    # def testRemoteQuery(self):
    #     """
    #     Return all room types in our remote object (Test Method)
    #     """
    #     session = self.RemoteSession()
    #     theQry = session.query(remoteModels.RoomType)
    #     return theQry.all()

    # def testLocalQuery(self):
    #     """
    #     Return all room types in our local object (Test Method)
    #     """
    #     session = self.LocalSession()
    #     theQry = session.query(models.RoomType)
    #     return theQry.all()

    def syncNodes(self):
        """Syncronise nodes:

        Check if we need to syncronise Nodes
        If there are any nodes missing, make sure they are created along with the relevant sensors

        Ideas to deal with this without using SQLA would be

        1) Download a list of remote nodes / Sensors
        2) Diff and then use REST to add any new or missing items

        We also need to consider what happens if a new sensor is added to a node. Currently our code doesn't support this.
        """
        lSess = self.LocalSession()
        rSess = self.RemoteSession()
        
        #We can get away with just asking for Ids
        rQuery = [x[0] for x in rSess.query(remoteModels.Node.id)]
        log.debug("Remote Ids --> {0}".format(rQuery))
        
        #Have a check here, if the remote DB is empty, then using _in throws a Error
        if rQuery:
            lQuery = lSess.query(models.Node).filter(~models.Node.id.in_(rQuery))
        else:
            lQuery = lSess.query(models.Node).all()
        #log.debug("Local Query -> {0}".format(lQuery.all()))

        if lQuery is None:
            log.debug("No Nodes to Synchronise")
            return False
        
        #Otherwise we need to update a set of Nodes
        for node in lQuery:
            log.debug("Creating node {0} on remote server".format(node))
            #Create the Node
            newNode = remoteModels.Node(id=node.id)
            rSess.add(newNode)
            rSess.flush() #Avoid Integrety Error

            #And Any attached Sensors
            for sensor in node.sensors:
                log.debug("Creating Sensor")

                #We shouldn't have to worry about sensor types as they should be global
                newSensor = remoteModels.Sensor(sensorTypeId=sensor.sensorTypeId,
                                                nodeId = newNode.id,
                                                calibrationSlope = sensor.calibrationSlope,
                                                calibrationOffset = sensor.calibrationOffset)
        
                rSess.add(newSensor)
            rSess.flush()
        
        rSess.commit()

        return True

        #TO Ensure all sensors are updated
        for node in lQuery:
            log.debug("Checking sensors for Node {0}".format(node))
                      
    def syncLocation(self,locId):
        """Code to Synchronise a given locations

        Locations are a combination of Rooms/Houses therefore they are also synchronised 
        during this process.
        
        # Check we have a room of this (name/type) in the remote databases (Create)
        # Check we have a house of this (name/deployment) in the remote (Create)
        # Check we have a location with these parameters (create)

        :param locId: LocationId to Synchronise
        :return Equivalent Location Id in the Remote Database



        :since 0.1: Fixed House Name based bug.  Consider the
            following Say we have one house -> Deployment combo (Say
            Summer Deployments), then revisit at a later time (Winter
            Deployments)

            The Following should happen,
        
            Deployment1 -> House1 --(Location1)->  Room1 -> Node1 ...
            Deployment2 -> House2 --(Location2)->  Room1 -> Node1 ...

            Our Original Code for syncing locations did this:

            Deployment1 -> House1 --(Location1)->  Room1 -> Node1 ...
            Deployment2 -> House1 --(Location1)->  Room1 -> Node1 ...
        """

        lSess = self.LocalSession()
        rSess = self.RemoteSession()


        theLocation = lSess.query(models.Location).filter_by(id=locId).first()
        log.debug("{2} Synchronising Location {1} {2}".format(locId,theLocation,"="*10))

        # #This is a little unfortunate, but I cannot (without over complicating reflection) 
        # #Setup backrefs on the remote tables this should be a :TODO:
        # #So We need a long winded query

        # localRoom = theLocation.room
        # log.debug("Local Room {0}".format(localRoom))
        # remoteRoom = rSess.query(remoteModels.Room).filter_by(name=localRoom.name).first()
        # if remoteRoom is None:
        #     log.debug("--> No Such Room {0}".format(localRoom.name))

        #     localRoomType = localRoom.roomType
        #     log.debug("--> Local Room Type {0}".format(localRoomType))
        #     #We also cannot assume that the room type will exist so we need to check that
        #     roomType = rSess.query(remoteModels.RoomType).filter_by(name=localRoomType.name).first()
        #     if roomType is None:
        #         log.debug("--> --> No Such Room Type {0}".format(localRoomType.name))
        #         roomType = remoteModels.RoomType(name=localRoomType.name)
        #         rSess.add(roomType)
        #         rSess.flush()

        #     remoteRoom = remoteModels.Room(name=localRoom.name,
        #                                    roomTypeId = roomType.id)

        #     rSess.add(remoteRoom)
        #     rSess.flush()

        # rSess.commit()
        # log.debug("==> Remote Room is {0}".format(remoteRoom))
        
        # #Then Check the House
        # localHouse = theLocation.house
        # #To address the bug above, Add an intermediate step of checking the deployment
        # localDeployment = localHouse.deployment
        # log.debug("--> Local Deployment {0}".format(localDeployment))
        
        # #Assume that all deployments will have a unique name
        # remoteDeployment = rSess.query(remoteModels.Deployment).filter_by(name=localDeployment.name).first()

        # if remoteDeployment is None:
        #     log.debug("--> --> Create new Deployment")
        #     remoteDeployment = remoteModels.Deployment(name=localDeployment.name,
        #                                                description = localDeployment.description,
        #                                                startDate = localDeployment.startDate,
        #                                                endDate = localDeployment.endDate)
        #     rSess.add(remoteDeployment)
        #     rSess.commit()

        # log.debug("--> Remote Deployment {0}".format(remoteDeployment))
        
        # remoteHouse = rSess.query(remoteModels.House).filter_by(deploymentId = remoteDeployment.id,
        #                                                         address = localHouse.address).first()

        # log.debug("--> Local House {0}".format(localHouse))   

        # if not remoteHouse:
        #     #We should have created the deployment before   
        #     log.debug("--> --> Create new House")
        #     remoteHouse = remoteModels.House(address=localHouse.address,
        #                                      deploymentId=remoteDeployment.id)
        #     rSess.add(remoteHouse)
        #     rSess.flush()
        #     rSess.commit()

        # log.debug("--> Remote House is {0}".format(remoteHouse))

        # remoteLocation = rSess.query(remoteModels.Location).filter_by(houseId = remoteHouse.id,
        #                                                               roomId=remoteRoom.id).first()

        # log.debug("--> DB Remote Location {0}".format(remoteLocation))
        # rSess.flush()
        # if not remoteLocation:
        #     remoteLocation = remoteModels.Location(houseId=remoteHouse.id,
        #                                            roomId = remoteRoom.id)
        #     rSess.add(remoteLocation)
        #     log.debug("Adding New Remote Location")
            
        # log.debug("--> Remote Location is {0}".format(remoteLocation))
        # rSess.commit()

        # locId = remoteLocation.id
        # lSess.close()
        # rSess.close()
        # return locId
        # pass

    def syncReadings(self,cutTime=None):
        """Synchronise readings between two databases

        :param DateTime cutTime: Time to start the Sync from
        :return: True if sync was succesfull there are still nodes to sync
                 False if there were no nodes to Sync
                 -1 if there was an Error

        This assumes that Sync Nodes has been called.

        The Algorithm for this is:

        Initialise Temporary Storage, (Location = {})
        
        #. Get the time of the most recent update from the local database
        #. Get all Local Readings after this time.
        #. For Each Reading

            #. If !Location in TempStore:
                #. Add Location()
            #. Else:
                #. Add Sample

        # If Sync is successful, fix the last update timestamp and return 
        """


        lSess = self.LocalSession()
        session = self.RemoteSession()

        log.info("Synchronising Readings")
        
        startTime = time.time()

        #Time stamp to check readings against
        if not cutTime:
            rUrl = self.rUrl
            lastUpdate = lSess.query(models.UploadURL).filter_by(url=self.rUrl.url).first()
            log.info("--> Time Query {0}".format(lastUpdate))

            if lastUpdate:
                cutTime = lastUpdate.lastUpdate
            else:
                cutTime = None

        fetchLast = time.time()
        #Update Node States
                  
        #Get the Readings
        readings = lSess.query(models.Reading).order_by(models.Reading.time)
        if cutTime:
            log.debug("Filter all readings since {0}".format(cutTime))
            readings = readings.filter(models.Reading.time >= cutTime)

        log.info("Total Readings to Sync {0}".format(readings.count()))
        
        #Lets try the Limit
        readings = readings.limit(PUSH_LIMIT)

        makeQuery = time.time()

        #Init Temp Storage
        locationStore = {}
        newReading = None
        for reading in readings:  
            #print reading
            mappedLoc = locationStore.get(reading.locationId,None)
            #Check if we have the location etc
            if mappedLoc is None:
                #Deal with readings that have no location
                if reading.locationId is None:
                    mapId = None
                else:
                    mapId = self.syncLocation(reading.locationId)
                    #And update the nodes Location
                    if not mapId:
                        log.warning("Error Creating Location {0}".format(reading.locationId))
                        return -1
                                
                locationStore[reading.locationId] = mapId
            #Otherwise, We should just be able to sync the Reading
            newReading = remoteModels.Reading(time = reading.time,
                                              nodeId = reading.nodeId,
                                              type = reading.typeId,
                                              locationId = mapId,
                                              value = reading.value)
                     
            session.add(newReading)
            #session.commit()

        addReadings = time.time()
        if newReading is None:
            #If we had no data to update
            return False

        log.debug("Last Reading Added Was {0}".format(newReading))

        try:
            lastTime = newReading.time + timedelta(seconds = 1)
            session.flush()
            session.commit()
            session.close()
            #Update the Local Time stamp

            newUpdate = lSess.query(models.UploadURL).filter_by(url=self.rUrl.url).first()
            #Add a bit of jitter otherwise we end up getting the same reading.
            newUpdate.lastUpdate = lastTime
            lSess.flush()
            lSess.commit()
            log.info("Commit Successful Last update is {0}".format(newUpdate))
        except Exception, e:
            log.warning("Commit Fails {0}".format(e))
            return -1
        
        commitReadings = time.time()
        lSess.close()
        session.close()

        #Synchonise States
        log.info("Synchronising Nodestate")
        self.syncState(cutTime,lastTime)

        syncTime = time.time()

        readingLog.warning("{},{},{},{},{},{},{},{},{}".format(self.currentUrl,
                                                               startTime,
                                                               syncTime,
                                                               syncTime - startTime,
                                                               fetchLast - startTime,
                                                               makeQuery - startTime,
                                                               addReadings - startTime,
                                                               commitReadings - startTime,
                                                               syncTime - startTime))                                                

                                                        
                                        
        return True
        # pass

    def syncState(self,cutTime=None,endTime=None):
        """
        Synchronise any node state information

        Currently this just syncronises the node state table based on a given start date.
        Actually this is pretty easy, as our constaints on unique node names mean that 
        We dont have to do any error checking.

        :param DateTime startTime: Time to start filtering the states from
        """
        lSess = self.LocalSession()
        session = self.RemoteSession()

        nodeStates = lSess.query(models.NodeState).order_by(models.NodeState.time)
        log.debug("Total Nodestates {0}".format(nodeStates.count()))
        if cutTime:
            nodeStates = nodeStates.filter(models.NodeState.time >= cutTime)
        if endTime:
            nodeStates = nodeStates.filter(models.NodeState.time <= endTime)

        log.info("Total NodeStates to Sync {0}".format(nodeStates.count()))
                  
        stateCount = 0
        for item in nodeStates:
            newState = remoteModels.NodeState(time=item.time,
                                              nodeId = item.nodeId,
                                              parent = item.parent,
                                              localtime = item.localtime)
            session.add(newState)
            #log.info("--> Adding State {0}".format(newState))
            
        session.flush()
        session.commit()
        session.close()

        lSess.close()





if __name__ == "__main__":
    logging.debug("Testing Push Classes")
    
    #import time

    server = PushServer()
    server.sync()
    #push = Pusher()
    #push.sync()
    #for x in range(10):
    #    push.sync()
                       
    #while True: #Loop for everything
    #    t1= time.time()
    #    log.info("----- Synch at {0}".format(datetime.now()))
        #push.sync()
        #log.info("---- Total Time Taken for Sync {0}".format(time.time() - t1))
        #time.sleep(SYNC_TIME)
    #push.sync()
