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
    print(doc[attr])
    return jsonify({attr: doc[attr]})



if __name__ == "__main__":
    app.run(debug=True)