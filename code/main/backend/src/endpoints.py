from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

#api = Api(app)

client = MongoClient("mongodb://localhost:27017/")

db = client["digitalEditions"]
 
texts = db["editions"]    

@app.route("/texts", methods=["GET"])
def get_users():
    allTexts = list(texts.find({}))
    for txt in allTexts:
        txt["id"] = str(txt["id"])  
    return jsonify(allTexts)


if __name__ == "__main__":
    app.run(debug=True)