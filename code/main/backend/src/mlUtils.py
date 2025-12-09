from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import random
import torch
import matplotlib.pyplot as plt
import numpy as np
from transformers import BertTokenizer, BertModel, BertConfig

from transformers import AutoTokenizer, AutoModel

import pymongo

from collections import defaultdict



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
                
                embeddings = outputs.last_hidden_state[:, 0, :]
                out.append(embeddings.squeeze(0))
            print(out[0].shape)
        else:
            out=[]
            for elem in data:
                wordRep=[]
                for word in elem:

                    inputs = self.tokenizer(word, return_tensors="pt", padding=True, truncation=True)
                
                    with torch.no_grad():
                        outputs = self.model(**inputs)
                
                    embedding = outputs.last_hidden_state[:, 0, :]
                    wordRep.append(embedding)
                out.append(torch.concat(wordRep).squeeze(0))
            print(out[0].shape)

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
                # Format: Manuscript # Theology # Liturgy 
                keywords=keywords.replace(" ","").split("#")
                #print(len(keywords))
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
    
    def getGraphEncoding(self, data):
        # attribute → list of item IDs
        index = defaultdict(list)
        for itemId, attrs in enumerate(data):
            for a in attrs:
                index[a].append(itemId)

        
        edges = defaultdict(int)

        for attr, itemList in index.items():
            # for each attribute, connect all items that share it
            for i in range(len(itemList)):
                for j in range(i + 1, len(itemList)):
                    a, b = itemList[i], itemList[j]
                    if a != b:
                        u, v = min(a, b), max(a, b)
                        edges[(u, v)] += 1  

       
        #print(edges[0:10])
        
        edges = [(a, b, w) for (a, b), w in edges.items()]
        #print("after")

        #print(edges[0:10])


        return edges
    


class visModel():
    def __init__(self,nClusters):
        self.kmodel = KMeans(n_clusters=nClusters, random_state=42)
        self.model=None
        return

    def loadModel(self,path):
        return

    def saveModel(self,path):
        return  
    
    def run(self,data):

        return
    
    def train(self,data,mode):
        if mode == "d":
            self.model=self.kmodel.fit(data)
            res=PCA(n_components=2).fit_transform(data)
        else:
            if type(data[0]) == list:
                data = list(map(lambda x: torch.flatten(torch.Tensor(x)),data))
            else:
                data = list(map(lambda x: torch.flatten(x),data))

            self.model=self.kmodel.fit(data)
            #res=PCA(n_components=2).fit_transform(data)#
            res=[]

        labels = self.model.labels_

        print(len(labels))
        if len(res)>0:
            res= res.T


     
        return labels , res
      

    

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

