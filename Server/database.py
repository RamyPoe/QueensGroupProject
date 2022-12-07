import os, time
from turtle import update
import config
import json
import protocol

class Database:

    """ Constructor """
    def __init__(self):
        # Name of file with database info
        self.REL_FILEPATH = "database.json"
        
        # Get relevant directories for reading files
        self.DIR = str ( os.path.dirname(os.path.realpath(__file__)) )
        self.FILE_DIR = self.DIR + "/" + self.REL_FILEPATH

        # Organizing data indexes
        self.data_indexes = protocol.DATA_INDEXES

        # Read file into RAM as dictionary
        self._data = self.read_file(self.FILE_DIR)

    """ Reads the file upon start to load all data """
    def read_file(self, filepath):
        # Var to be returned
        final_dict = {}
        # Read File
        with open(self.FILE_DIR) as json_file:
            # Turn json to dictionary
            final_dict = json.load(json_file)
        # Return dictionary
        return final_dict


    """ Returns True if the key exists in the database """
    def keyExists(self, key : str) -> bool:
        return key in self._data

    """ Writes new entry to database given a key and its data """
    def addKey(self, key : str, data):
        if config.VERBOSE_OUTPUT: print(f"[DATABASE] Adding new data: ({key}, {data})")
        # Write data locally
        self._data[key] = data
        # Write data to file
        self.updateOnFile()

    """ Change data of a key """
    def updateKey(self, key : str, data, data_type : int):
        # Verify correct input
        if not data_type in self.data_indexes: raise ValueError(f"Invalid argument for type of data: {data_type}")
        # Key doesn't exist, nothing to update
        if not self.keyExists(key): return
        # Update locally
        index = self.data_indexes[data_type]
        # Add one to jump over hash index
        self._data[key][index+1] = data
        # Update on file
        self.updateOnFile()
        

    """ Writes disctionary contents to file"""
    def updateOnFile(self):
        # Update on file
        with open(self.FILE_DIR, "w") as json_file:
            json_file.write( json.dumps ( self._data, indent=4 ) )


    """ Returns all data on the key on database """
    def keyDump(self, key : str):
        if not self.keyExists(key): return None
        if config.VERBOSE_OUTPUT: print(f"[DATABASE] Data for user \"{key}\" : " + str(self._data[key][1:]))
        return self._data[key][1:]


    """ Returns the PassHash of the User """
    def getPassHash(self, key : str):
        if ( not key in self._data): raise ValueError("Key Does not Exist in Database")
        return self._data[key][ 0 ]

    
    
                
""" Dump database contents, used for debugging """
def dump():
    db = Database()
    return db._data
