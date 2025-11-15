from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)



client = MongoClient("mongodb://localhost:27017/")

db = client["DigitalEditions"]
 
texts = db["editions"]    

# To get all the editions in a list

@app.route("/texts", methods=["GET"])
def getTexts():
    textList = list(texts.find({}, {"_id": 0}))

    return textList

# To get one edition by id

@app.route("/texts/<id>", methods=["GET"])
def getText(id):
    doc = texts.find_one({"id": int(id)},{"_id": 0})  
    return jsonify(doc)

# To get an attribute of an elemnt by id (to remove later on)

@app.route("/texts/<id>/<attr>", methods=["GET"])
def getTextAttribute(id,attr):
    doc = texts.find_one({"id": int(id)},{"_id": 0})
    #print(doc[attr])
    return jsonify({attr: doc[attr]})

# To get all ids

@app.route("/texts/ids", methods=["GET"])
def getIds():
    idList = list(texts.find({}, {"_id": 0,"id":1}))  
    return idList


# To get all times of publishing

@app.route("/texts/period/name", methods=["GET"])
def getPeriodName():
    timeList = list(texts.find({}, {"_id": 0,"id":1,"Historical Period":1}))  
    return timeList

@app.route("/texts/period", methods=["GET"])
def getTimes():
    timeList = list(texts.find({}, {"_id": 0,"id":1,"Time/Century":1}))  
    return timeList

#   start

@app.route("/texts/period/start", methods=["GET"])
def getStartPeriod():
    timeList = list(texts.find({}, {"_id": 0,"id":1,"period_start":1}))  
    return timeList

@app.route("/texts/period/end", methods=["GET"])
def getEndPeriod():
    timeList = list(texts.find({}, {"_id": 0,"id":1,"period_end":1}))  
    return timeList



#   end

#   period


# To get titles

@app.route("/texts/names", methods=["GET"])
def getNames():
    nameList = list(texts.find({}, {"_id": 0,"id":1,"Edition name":1}))  
    return nameList

@app.route("/texts/<id>/name", methods=["GET"])
def getName(id):
    doc = texts.find_one({"id": int(id)},{"_id": 0,"Edition name":1})
    return doc

# to get author names

@app.route("/texts/authors", methods=["GET"])
def getAuthors():
    nameList = list(texts.find({}, {"_id": 0,"id":1,"Manager or Editor":1}))  
    return nameList

@app.route("/texts/<id>/author", methods=["GET"])
def getAuthor(id):
    doc = texts.find_one({"id": int(id)},{"_id": 0,"Manager or Editor":1})
    return doc

if __name__ == "__main__":
    app.run(debug=True)