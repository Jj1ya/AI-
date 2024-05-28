import pandas as pd
import pickle

def predict(new_data):
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    predictions = model.predict(new_data)
    return predictions
