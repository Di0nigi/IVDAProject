from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from .mlUtils import visModel,dataEncoder
import random
import json
from urllib.parse import unquote



#from .filterning import filterModel

app = Flask(__name__)
CORS(app)

# visM=visModel()


client = MongoClient("mongodb://localhost:27017/")

db = client["DigitalEditions"]
 
texts = db["editions"]    


#scM = ScoreModel()
#fM = filterModel()

#@app.route("/texts/filter", methods=["POST"])
#def setFilterParams():
#    return


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

@app.route("/texts/language/name", methods=["GET"])
def getLanguageName():
    langList = list(texts.find({}, {"_id": 0, "id": 1, "Language": 1}))
    return langList

@app.route("/texts/writingsupport/name", methods=["GET"])
def getWritingSupportName():
    supportList = list(texts.find({}, {"_id": 0, "id": 1, "Writing support": 1}))
    return supportList

#   period

@app.route("/texts/period", methods=["GET"])
def getTimes():
    timeList = list(texts.find({}, {"_id": 0,"id":1,"Time/Century":1}))  
    return timeList

#   start

@app.route("/texts/period/start", methods=["GET"])
def getStartPeriod():
    timeList = list(texts.find({}, {"_id": 0,"id":1,"period_start":1}))  
    return timeList

#   end
@app.route("/texts/period/end", methods=["GET"])
def getEndPeriod():
    timeList = list(texts.find({}, {"_id": 0,"id":1,"period_end":1}))  
    return timeList


# ML endopoints

@app.route("/texts/graphPoints/<modPoints>", methods=["GET"])
def getAndComputeGraphPoints(modPoints):
    dc = dataEncoder(textType='k')
    vM=visModel(nClusters=5)
    
    decoded=unquote(modPoints)
    modEditions = json.loads(decoded)

    print(f"modeeds{modEditions}")

    if modEditions == []:
        keyWordsList = list(texts.find({}, {"_id": 0,"id":1,"Keywords":1,"keywordsEmbed":1}))
        formatted = dc.formatData(keyWordsList)
        edges= dc.getGraphEncoding(formatted)
        encoded = [elem["keywordsEmbed"] for elem in keyWordsList]
        random.shuffle(edges)
    else:
        keyWordsList = list(texts.find({}, {"_id": 0,"id":1,"Keywords":1,"keywordsEmbed":1}))

        #print(keyWordsList[0])

        for modEd in modEditions:
            #print(modEd)
            id = modEd["id"]
            mask = modEd["mask"]
            custom = modEd["customKeywords"]
            customWords=""
            for k in custom:
                customWords+=f"# {k}"

            result = next((item for item in keyWordsList if item["id"] == id), None)
            for ind in mask:
                rm=result["Keywords"].pop(int(ind))

            result["Keywords"]+=customWords
        
            

        formatted = dc.formatData(keyWordsList)
        edges= dc.getGraphEncoding(formatted)
        encoded = [elem["keywordsEmbed"] for elem in keyWordsList]
        #encoded = dc.encode(formatted)
        random.shuffle(edges)

    #dc.saveData(encoded, "keywordsEmbed", client, db, texts)

    
    labs = vM.train(encoded,mode="k")[0].tolist()



    ids=[elem["id"] for elem in keyWordsList]

    #ret={"labels":labs.tolist(),"edges":list(edges),"nodes":ids}

    nodeList=[{"id":elem["id"],"label":labs[ind]} for ind,elem in enumerate(keyWordsList)]
    linkList=[{"from":ed[0],"to":ed[1],"weight":ed[2]} for ed in list(edges)]


    ret = {"nodes":nodeList,"links":linkList}
    #ret={}

    
    
    #print(encoded[0])
    #dc.saveData(encoded, "keywordsEmbed", client, db, texts)
    #print("done")

    return jsonify(ret)

@app.route("/texts/scatterPoints", methods=["GET"])
def getAndComputeScatterPoints():
    dc = dataEncoder(textType='d')
    vM=visModel(nClusters=7)
    descriptionLists = list(texts.find({}, {"_id": 0,"id":1,"Content_Description":1,"descritpionEmbed":1}))
    #formatted = dc.formatData(descriptionLists)
    #encoded = dc.encode(formatted)
    #dc.saveData(encoded, "descritpionEmbed", client, db, texts)
    encoded = [elem["descritpionEmbed"] for elem in descriptionLists]

    labs , points = vM.train(encoded,mode="d")

    ids = [elem["id"] for elem in descriptionLists]

    ret = {"ids":ids ,"labels":labs.tolist(),"xCoor":points[0].tolist(),"yCoor":points[1].tolist()}
    #ret={}

    

    #print("done")


    return jsonify(ret)


# to compute scores

@app.route("/texts/reliability",methods = ["POST"])
def calculateReliabilityScores():
    data = request.json
    weights = data.get('weights', {'citations': 50, 'witnesses': 50, 'audience': 50})
    
    # Normalize weights to sum to 1
    total = weights['citations'] + weights['witnesses'] + weights['audience']
    if total == 0:
        total = 1
    
    w_citations = weights['citations'] / total
    w_witnesses = weights['witnesses'] / total
    w_audience = weights['audience'] / total
    
    # Get all editions and calculate scores
    all_texts = list(texts.find({}, {"_id": 0, "id": 1, "Citation_bin": 1, 
                                      "Value_of_witnesses_yes": 1, "Audience": 1}))
    
    scores = []
    for text in all_texts:
        # Get binary values (default to 0 if not present)
        citation_val = text.get('Citation_bin', 0)
        witnesses_val = text.get('Value_of_witnesses_yes', 0)
        # Audience is categorical, convert to binary (1 if specified, 0 if not)
        audience_val = 1 if text.get('Audience') and text.get('Audience').lower() not in ['not provided', 'nan', ''] else 0
        
        # Calculate weighted score (0-100)
        score = (citation_val * w_citations + witnesses_val * w_witnesses + audience_val * w_audience) * 100
        
        scores.append({
            'id': text['id'],
            'reliabilityScore': round(score)
        })
    
    return jsonify(scores)

@app.route("/texts/reliability/<id>",methods = ["GET"])
def getScores():
    return


# to get tags

@app.route("/texts/tags",methods = ["GET"])
def getAllTags():
    dc = dataEncoder(textType='k')

    keyWordsList = list(texts.find({}, {"_id": 0,"id":1,"Keywords":1}))

    formatted = dc.formatData(keyWordsList)
    l=set([])
    for elem in formatted:
        for word in elem:
            l.add(word.lower())

    ret = {"allTags": list(l)}
    



    return jsonify(ret)

@app.route("/texts/tags/<id>",methods = ["GET"])
def getEditionTags(id):

    keyWordsList = list(texts.find({"id": int(id)}, {"_id": 0,"id":1,"Keywords":1}))

    dc = dataEncoder(textType='k')

    keywords = dc.formatData(keyWordsList)[0]

    ret = {"tags": keywords}

    return jsonify(ret)


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