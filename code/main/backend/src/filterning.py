import numpy as np

from pymongo import MongoClient


class filterModel:

    def __init__(self,parameters=None):

        self.params=parameters
        
        return
    
    def parseParams(self):
        return

    def update(self,parameters):
        self.params = parameters
        return
    
    def infer(self,data):

        


        return
    

'''
filters = {
    # Period range filter - array of [min, max]
    "periodRange": [500, 1500],  # Example: 500 CE to 1500 CE
    
    # Authority/Authoritativeness filter - number 0-100
    "authoritativeness": 70,  # Minimum authority score
    
    # Renown filter - number 0-100
    "renown": 50,  # Minimum renown score
    
    # Historical period filter - array of objects with name and status
    "historicalPeriod": [
        {"name": "medieval", "status": "selected"},
        {"name": "renaissance", "status": "selected"},
        {"name": "modern", "status": "excluded"}
    ],
    
    # Scholarly filter - boolean
    "scholarly": True,  # Only scholarly editions
    
    # Digital filter - boolean
    "digital": True,  # Only digital editions
    
    # Images filter - string
    "hasImages": "yes",  # "yes", "partly", or "no"
    
    # XML-TEI filter - string
    "hasXMLTEI": "yes",  # "yes", "partly", or "no"
    
    # API filter - boolean
    "hasAPI": True,  # Only editions with API access
    
    # Open access filter - string
    "openAccess": "yes",  # "yes" or "no"
    
    # Language filter - array of objects with name and status
    "language": [
        {"name": "latin", "status": "selected"},
        {"name": "greek", "status": "selected"},
        {"name": "english", "status": "excluded"}
    ],
    
    # Writing support filter - array of objects with name and status
    "writingSupport": [
        {"name": "parchment", "status": "selected"},
        {"name": "paper", "status": "selected"},
        {"name": "papyrus", "status": "excluded"}
    ],
    
    # Keywords filter - array of objects with name and status
    "keywords": [
        {"name": "philosophy", "status": "selected"},
        {"name": "theology", "status": "selected"},
        {"name": "poetry", "status": "excluded"}
    ]
}
'''