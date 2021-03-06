"""
Functionality to upload from a Arch Rock database

Be Warned there is lots of weirdness in the database that does not make this quite
as straight forward as it could be.

Duplicate nodes with different Id's are one such problem,  This arises when a "New" deployment is started.
The way I have been dealing with this is to use node address to index nodes when they are added, 
Rather than 
"""

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__) 
log.setLevel(logging.DEBUG)

#Multiple Logging
fh = logging.FileHandler("transfer.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

log.addHandler(ch)
log.addHandler(fh)

#import orbit_viewer.models as models
#import orbit_viewer.models.meta as meta

#And for the local connection
import sqlalchemy
import sqlalchemy.orm

from sqlalchemy.ext.declarative import declarative_base

import datetime

import mainDb
import models

BASE_NODE_ID = 118118

localBase = declarative_base()

#GLOBALS FOR SENSOR TYPES
ALLOWED_TYPES = [["Humidity","Humidity"],
                 ["LightPAR","Light PAR"],
                 ["LightTSR","Light TSR"],
                 ["Temperature","Temperature"],
                 ["ADC0","CO2"],
                 ["CO2","CO2"],
                 ["Voltage","Battery Voltage"],
                 ]


class Data(localBase):
    """ Meta class to Represent Data in the Reflected Database.
    
    .. warning:: It is not intended for this class to be directly instantiated, only created via sqlalchemy reflection
    """
    __tablename__ = "data"
    data_key = sqlalchemy.Column("data_key",sqlalchemy.Integer,primary_key = True)
    node_key = sqlalchemy.Column("node_key",sqlalchemy.Integer)
    datasource_key = sqlalchemy.Column("datasource_key",sqlalchemy.Integer)
    timestamp = sqlalchemy.Column("timestamp",sqlalchemy.DateTime)
    value = sqlalchemy.Column("value",sqlalchemy.Float)
    text_value = sqlalchemy.Column("text_value",sqlalchemy.Text)
    

    def __str__(self):
        outStr = []
        outStr.append("Key: %s" %self.data_key)
        outStr.append("Node Id: %s" %self.node_key)
        outStr.append("Sensor Id: %s" %self.datasource_key)
        outStr.append("Time: %s" %self.timestamp)
        outStr.append("Value: %s" %self.value)
        return "\t".join(outStr)


class Source(localBase):
    """
    Reflect the Datasource_Dimension Table
    
    @warning: This does not have all the info in the original table.
              Rather, it just includes the stuff we will be using
    """
    __tablename__ = "datasource_dimension"
    datasource_key = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    datasource_created = sqlalchemy.Column(sqlalchemy.DateTime)
    source = sqlalchemy.Column(sqlalchemy.Text)
    addr = sqlalchemy.Column(sqlalchemy.Text)
    name = sqlalchemy.Column(sqlalchemy.Text)

    def __str__(self):
        outStr = []
        outStr.append("dsKey {0}".format(self.datasource_key))
        outStr.append("created {0}".format(self.datasource_created))
        outStr.append("source {0}".format(self.source))
        outStr.append("addr {0}".format(self.addr))
        outStr.append("name {0}".format(self.name))

        return "  ".join(outStr)

class Ar_Node(localBase):
    """ Table to deal with Arch Rock Nodes"""
    __tablename__ = "node_dimension"
    node_key = sqlalchemy.Column(sqlalchemy.Integer,primary_key = True)
    node_created = sqlalchemy.Column(sqlalchemy.DateTime)
    addr = sqlalchemy.Column(sqlalchemy.Text)
    name = sqlalchemy.Column(sqlalchemy.Text)
    short_addr = sqlalchemy.Column(sqlalchemy.Integer)

    def __str__(self):
        outStr = []
        outStr.append("Key: {0}".format(self.node_key))
        outStr.append("Created: {0}".format(self.node_created))
        outStr.append("Addr: {0}".format(self.addr))
        outStr.append("saddr {0}".format(self.short_addr))
        outStr.append("Name: {0}".format(self.name))
        return "  ".join(outStr)
                      

class ArchRockDB(object):
    """Functionality to connect to a Arch Rock Postgresql Database"""
    def __init__(self,url="127.0.0.1",database="pp",address=None):
        """Create the connection"""

        log.debug("Initialising Arch Rock Engine")
        #engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:@{0}:5432/{1}'.format(address,database), convert_unicode=True)

        engine = sqlalchemy.create_engine('postgresql+psycopg2://pp:pr1merp4ck@{0}:5432/{1}'.format(url,database),
                                          convert_unicode=True,
                                          server_side_cursors=True)

        #Bind Metadata to those tables declared in Base
        localBase.metadata.create_all(engine)

        # #And Session Maker
        self.Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.meta = localBase.metadata


        self.houseAddress = address
        #Load all known sensor types
        sensorDict = {}
        #session = meta.DBSession()
        #sensorTypes = session.query(models.sensor.SensorType).all()

        #log.debug("{0} Sensor Types {0}".format("-"*20))
        #for sensor in sensorTypes:
        #    log.debug(sensor)
        #    sensorDict[sensor.sensor_type] = sensor
        #log.debug("{0}".format("-"*40))

        #self.sensorTypes= sensorDict
        #log.debug("PG Engine Init Complete")        
        #self.log = log

    def listTables(self):
        """Print and Return a list of all tables in this database

        :returns: A List of Tables in the database
        """

        for t in self.meta.sorted_tables:
            print t.name

        return self.meta.sorted_tables

    def listNodes(self):
        """Print and return a list of nodes"""
        self.log.debug("{0} Nodes {0}".format("-"*20))
        session = self.Session()
        query = session.query(Ar_Node).all()
        for item in query:
            self.log.debug(item)


    def createDatabase(self):
        """Create the Required Database Objects"""
        session = models.meta.Session()
        arSession = self.Session()
        #log.setLevel(logging.WARNING)
        deploymentName = "archRock"
        houseName = self.houseAddress

        theDep = session.query(models.Deployment).filter_by(name=deploymentName).first()
        log.debug("Checking for existing deployment {0}".format(theDep))
        if theDep is None:
            #Create a new deployment
            theDep = models.Deployment(name=deploymentName)
            session.add(theDep)
            session.flush()
            log.debug("Adding Deployment to database {0}".format(theDep))


        #And check for Houses
        theHouse = session.query(models.House).filter_by(address=houseName).first()
        log.debug("Checking for house {0}".format(theHouse))
        if theHouse is None:
            theHouse = models.House(address=houseName,
                                    deploymentId = theDep.id)
            session.add(theHouse)
            session.flush()
            log.debug("Adding New House {0}".format(theHouse))


        self.theHouse = theHouse

        emptyRoom = session.query(models.RoomType).filter_by(name="Unocupied").first()

        nodeMap = {}
        #Temp storage for <ADDDR> <Node>
        addrMap = {}

        #We want to setup nodes / Rooms / Locations based on the node_dimension table
        log.info("Setting Up Nodes")
        nodeQry = arSession.query(Ar_Node)
        for item in nodeQry:
            #Dont bother with the router
            if item.name == "archrock-router":
                continue

            #Check / Create a node if required
            nodeId = int(item.addr[8:],16)
            log.debug("{0} {1} {2}".format(item,item.addr,nodeId))
            
            #nodeId = BASE_NODE_ID + item.short_addr
            
            theNode = session.query(models.Node).filter_by(id = nodeId).first()
            if theNode is None:
                theNode = models.Node(id=nodeId)
                session.add(theNode)
                session.flush()
                log.debug("Creating New Node {0}".format(theNode))
            
            #Next we create a room / Location
            roomName = item.name
            if not roomName == "":
                log.debug("Room Name is {0}".format(roomName))

                theRoom = session.query(models.Room).filter_by(name=roomName).first()
                if theRoom is None:
                    theRoom = models.Room(name=roomName,
                                          roomTypeId=emptyRoom.id)
                    log.debug("Creating Room {0}".format(theRoom))
                    session.add(theRoom)
                    session.flush()

                #And now we can turn this room into a Location
                theLocation = session.query(models.Location).filter_by(houseId=theHouse.id,
                                                                       roomId = theRoom.id).first()
                if theLocation is None:
                    theLocation = models.Location(houseId = theHouse.id,
                                                  roomId = theRoom.id)
                    session.add(theLocation)
                    log.debug("Creating Location {0}".format(theLocation))
                    session.flush()
            #Last thing we create a mapping between the node and the Location
            nodeMap[item.node_key] = [theNode,theLocation]
            addrMap[item.addr] = theNode

        #log.debug(nodeMap)
        self.nodeMap = nodeMap
        #We also need to do mapping for sensor types etc
        #theQry = arSession.query(Source)

        #Map the Types we are expecting to types from the database
        sensorTypeMap = {}
        log.info("Mapping Sensor Types")
        for sType in ALLOWED_TYPES:
            theType = session.query(models.SensorType).filter_by(name=sType[1]).first()
            
            log.debug("AR: {0}  Local {1}".format(sType,theType))
            sensorTypeMap[sType[0]] = theType
            
        #log.debug(sensorTypeMap)

        sensorMap = {}
        
        sQry = arSession.query(Source)
        for item in sQry:
            thisItem = sensorTypeMap.get(item.source,None)
            if thisItem:
                sensorMap[item.datasource_key] = sensorTypeMap[item.source]

        self.sensorMap = sensorMap
        log.setLevel(logging.DEBUG)
        
        log.info("Commtitting Changes")
        session.flush()
        session.commit()

    def removeDupes(self):
        """Remove Duplicate Items"""
        print "Removing Dupes"

        from sqlalchemy.orm import aliased

        session = self.Session()

        a1 = aliased(Data)
        a2 = aliased(Data)

        query = session.query(a1,a2)
        query = query.filter(a1.datasource_key == a2.datasource_key) #Data sources should be unique
        query = query.filter(a1.node_key == a2.node_key)
        query = query.filter(a1.timestamp == a2.timestamp)
        query = query.filter(a1.data_key < a2.data_key)
        #query = query.limit(10)
        log.debug("Count of Items {0}".format(query.count()))
        #print query.limit(10).all()

        keyList = [item[1].data_key for item in query.all()]
        #log.debug(keyList)

        theQry = session.query(Data).filter(Data.data_key.in_(keyList))
        
        delItems = theQry.delete(False)
        log.debug("Total of {0} items deleted".format(delItems))
        
        session.commit()
#        for item in query.limit(10):
            
            #log.debug("{0} == {1}".format(item[0],item[1]))
        return

        # nodeIds = []
        # for item in query.all():
        #     print "{0}\n{1}\n".format(item[0],item[1])
        #     nodeIds.append(item[0].data_key)

        # query = session.query(Data).filter(Data.data_key.in_(nodeIds))
        # for item in query.all():
        #     print item
        
        # query = session.query(Data).filter(Data.data_key.in_(nodeIds))
        #delItems = query.delete()
        #print "Total Duplicates {0}".format(delItems)

        #nodeIds = [n.data_key for n in query.all()]
        #print "Node Id's Retrieved {0}".format(time.time()-t1)
        
        #query = session.query(Data)
        #query.filter(Data.data_key.in_(nodeIds))
        #delItems = query.delete()
        #print "Items Deleted ",delItems
        #transaction.begin()
        #for item in query:
        #    print item
        #    session.delete(item)

        #    print "{0}\n{1}\n".format(item[0],item[1])
        #query.delete()
        #session.flush()
        #transaction.commit()
        #session.close()



    def transferData(self):
        """
        Transfer Data from the DB

        @param deplotmentName: Name of the Deployment
        @param startDate: If we have more than one deployment can filter here
        @param endDate: as Above
        """
        #log = self.log
        #status = {"deployment":None,
        #          "nodes":[],
        #          "sensors":[]}

        #Create Sessions
        session = models.meta.Session()
        arSession = self.Session()

        nodeMap = self.nodeMap
        sensorMap = self.sensorMap

        theQry = arSession.query(Data)
        theQry = theQry.order_by(Data.timestamp)
        import datetime
        tmpDate = datetime.datetime(2009,11,1,20,32,56)
        theQry = theQry.filter(Data.timestamp >= tmpDate)
        log.debug("Total Of {0} Items in Database!!".format(theQry.count()))
        
        #Lets try stripping that to only include data types we want
        nodeKeys = nodeMap.keys()
        dsKeys = sensorMap.keys()
        
        theQry = theQry.filter(Data.node_key.in_(nodeKeys))
        theQry = theQry.filter(Data.datasource_key.in_(dsKeys))
        #log.debug(theQry)
        totSamples = theQry.count()
        log.debug("Total of {0} samples with filtering".format(totSamples))

        #Try to use Cursors on the Postgress side
        theQry = theQry.yield_per(1000)

        #Probably better to do 
        #theQry = theQry.limit(10)
        objCount = 0
        commitCount = 0
        for item in theQry:
            #log.debug(item)
            #Turn this into a "proper" Reading
            thisNode = nodeMap[item.node_key]
            thisSensor = sensorMap[item.datasource_key]
            theReading = models.Reading(time = item.timestamp,
                                        nodeId = thisNode[0].id,
                                        typeId = thisSensor.id,
                                        locationId = thisNode[1].id,
                                        value = item.value)
            #log.debug(theReading)
            session.add(theReading)
            session.flush()
            objCount += 1
            if objCount == 10000:
                commitCount += 1
                log.debug("Commiting ~{0}".format(commitCount * objCount))
                objCount = 0
                session.commit()
        
        session.commit()



if __name__ == "__main__":
    log.debug("Connecting to central DB")
    mainDb.initDB()

    log.debug("Connecting to Postgresql")

    import time

    #List of Databases etc.

    #Ones with current cost
    # DBLIST = [
    #          ["41PriorPark","PriorPark41"],
    #          ["603SwanLane","SwanLane603"],
    #          ["605SwanLane","SwanLane605"],
    #          ["117Jodrell","jodrell117"],
    #          ["119Jodrell","jodrell119"],
    #          ["127Jodrell","jodrell127"],
    #          ["133Jodrell","jodrell133"],
    #          ["Elm Road","elm"],
    #          ["58Elliot","fiftyeight_elliot_summer"],
    #          ["Leam","leam"],
    #          ["School","schoolnew"],
    #          ["TheGreen","thegreen"],
    #          ["Town Ground","town_ground"],
    #          ["Brays lane","brays2010"],
    #          ["30 Elliot Summer","thirty_elliot_summer"],
    #          ["30 Elliot Winter","thirty_elliot_winter"],
    #          ["Weston Lane","weston"],
    #          ]

    DBLIST = [#["131Jodrell","131Jodrell"],
              #["155Jodrell","155Jodrell"],
              ["227FoleshillA","227Foleshill"],
              ["30Newdigate","30Newdigate"],
              #["Rooftop","rooftopnibe"],
              ]

    

    for item in DBLIST:
        log.debug("Working for item {0}".format(item))
        theDb = ArchRockDB(database=item[1],address=item[0])
        theDb.createDatabase()
        theDb.removeDupes()
        theDb.transferData()



    #theDb = ArchRockDB(database="PriorPark41",address="41PriorPark")
    #theDb.listTables()
    #theDb.createDatabase()
    #theDb.removeDupes()
    #theDb.transferData()
