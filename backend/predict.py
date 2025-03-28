from fastapi import APIRouter, HTTPException, Form
import pickle
import pandas as pd

router = APIRouter()

# Load trained model and label encoder
model, label_encoder = pickle.load(open("prawn_model.pkl", "rb"))

@router.post("/predict")
async def predict(
    no_of_prawns: float = Form(...),
    age: float = Form(...),
    food: float = Form(...),
    season: str = Form(...)
):
    try:
        # Encode season
        season_encoded = label_encoder.transform([season])[0]

        # Create feature array
        features = pd.DataFrame([[no_of_prawns, age, food, season_encoded]],
                                columns=['No_of_Prawns', 'Age_of_Pond', 'Food_Intake', 'Season'])

        # Predict
        prediction = model.predict(features)[0]
        return {"prediction": f"{prediction:.2f}"}  # Format to 2 decimal places
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
