# IVDA Project

## Interactive Exploration of a Catalog of Digital Editions

**Motivation/Goal:** _The Catalog of Digital Editions is a metadata collection of 350 works from Digital Humanities
projects, manually curated by Greta Franzini. The solution will be in the realm of exploratory search: combining
open-ended information-seeking behavior (exploration) with directed search and exploration support. Think about
how interactive visualizations can allow users to explore the data. Choose appropriate visualizations for the different
facets (e.g., time, geo, categorical, numerical, binary) and combine them in an interactive interface. Make appropriate
assumptions in cases where the features in the dataset are not self-explanatory. If interested, you can also think of
LLM-Based Data Enrichment for yet other, non-existing attributes/metadata._

## Project structure

``` txt
code|
    |-> exampleStuff: Assigment 1 example code
    |
    |-> main|: Actual project code
            |
            |-> backend |: api and ml utilities for the app
            |           |
            |           |-> src: main backend code 
            |
            |-> frontend|: Vue project for frontend programming
                        |
                        |-> src |: App.vue & main.js
                                |
                                |-> components: Helloworld.vue (main page) 

```

## How to build the DataBase

- Open _*MongoDBCompass*_
- Connect to locallhost
- Click "Create database" (the "+" sign to the side of localhost)
- Database name: _*DigitalEditions*_
- Collection name: _*editions*_
- Click "ADD DATA" and "Import JSON or CSV"
- Select _*data\processed_data.csv*_
- Select delimiter "Comma"
- Click "Import"

## How to run

- **Frontend**
Run ```runFront.bat```, or
    - go into ```cd code\\main\\frontend```
    - run ```npm run dev```

- **Backend**
Run ```runBack.bat```, or
    - go into ```cd code\\main\\backend```
    - run ```.\env\Scripts\activate.bat```
    -  **IF FIRST TIME** run ```installReq.bat```
    - run ```python app.py```
