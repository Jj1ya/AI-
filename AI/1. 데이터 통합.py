# load_data.py
import pandas as pd
from pymongo import MongoClient

def load_data():
    client = MongoClient('mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/')
    db = client['국제시장_분석데이터']
    
    collection_names = db.list_collection_names()
    dataframes = []

    for collection_name in collection_names:
        collection = db[collection_name]
        data = list(collection.find({}, {'_id': 0}))
        df = pd.DataFrame(data)
        dataframes.append(df)

    df = pd.concat(dataframes, ignore_index=True)
    return df

if __name__ == "__main__":
    df = load_data()
    print(df.head())
