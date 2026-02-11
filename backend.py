import joblib
import os 
import pandas as pd

path = os.path.join("model",'Final_Model.pkl')
_model = None

def load_model():
    global _model
    if _model is None:
        _model=joblib.load(path)
    return _model

def predict(data : dict) -> dict:
    _model = load_model()
    df= pd.DataFrame([data])
    prediction= _model.predict(df)[0]
    return {
        "Rank":float(prediction[0]),
        "Percentile":float(prediction[1])
    }

def predict_csv(csv_path : str)-> list:
    _model =load_model()
    df=pd.read_csv(csv_path)
    prediction = _model.predict(df)
    return prediction.tolist()