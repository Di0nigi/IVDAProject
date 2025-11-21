from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


import torch
import matplotlib.pyplot as plt
import numpy as np
from transformers import BertTokenizer, BertModel, BertConfig

from transformers import AutoTokenizer, AutoModel

import pymongo



class dataEncoder():
    def __init__(self, textType=""):

        modelName = "bert-base-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(modelName)
        self.model = AutoModel.from_pretrained(modelName)

        self.tp=textType

        return
    
    # to optimize

    def encode(self,data):

        out = []
        
        if self.tp=="d":

            for elem in data:

                inputs = self.tokenizer(elem, return_tensors="pt", padding=True, truncation=True)
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                
                embeddings = outputs.last_hidden_state
                out.append(embeddings)
        else:
            out=[]
            for elem in data:
                wordRep=[]
                for word in elem:

                    inputs = self.tokenizer(elem, return_tensors="pt", padding=True, truncation=True)
                
                    with torch.no_grad():
                        outputs = self.model(**inputs)
                
                    embedding = outputs.last_hidden_state
                    wordRep.append(embedding)
                out.append(torch.concat(wordRep))

        return out 
    

    def formatData(self,data):

        dataPoints=[]

        if self.tp=="d":
            for edition in data:
                description=edition["Content_Description"]
                dataPoints.append(description)
        else:
            for edition in data:
                keywords=edition["Keywords"]
                # Format: Manuscript # Theology # Liturgy # Philology # Religion
                keywords=keywords.replace(" ","").split("#")
                dataPoints.append(keywords)
                
        return dataPoints
    

    def saveData(self,data,target,client, db, collection):
        #embeddings = data
        for ind,doc in enumerate(collection.find({})):
            
            tensorList = data[ind].tolist()

            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {target: tensorList}}
            )   
        
        return


class visModel():
    def __init__(self,mode,nClusters):
        self.kmodel = KMeans(n_clusters=nClusters, random_state=42)
        return

    def loadModel(self,path):
        return

    def saveModel(self,path):
        return  
    
    def train(self,data):
        self.kmodel.fit(data)
        
        

        return
    
    def run(self,data):
        
        return



    
    

### demo code not final 

def demoPipeline(data):
    

    #model_name = "bert-base-uncased"
    #tokenizer = AutoTokenizer.from_pretrained(model_name)
    #model = AutoModel.from_pretrained(model_name)

    #text = "Hello, how are you today?"

    
    #print(embeddings[0])


    return





def main():

    #demoPipeline(["A digital facsimile and transcription of the Weissenburg manuscript, a significant 8th-century collection of catechetical texts, creeds, and glossaries.","A comprehensive archive of the 18th-century poet's complete poems, selected prose, and correspondence."])

    return "done"


if __name__ == "__main__":
    print(main())

