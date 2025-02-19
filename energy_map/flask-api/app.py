from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from joblib import load  # Use joblib for loading joblib files

app = Flask(__name__)
CORS(app)

# Load the saved models using joblib
model_heating = load('Model_Heating_1104/gbr_best_Y1_compat.joblib')
model_cooling = load('Model_Cooling_1104/gbr_best_Y2_compat.joblib')

# Load pre-trained encoders for the heating model
label_encoders_heating = {
    'X1_Type': load(open('Model_Heating_1104/X1_Type_encoder.pkl', 'rb')),
    'X3_Shape': load(open('Model_Heating_1104/X3_Shape_encoder.pkl', 'rb')),
    'X13_EnergyCode': load(open('Model_Heating_1104/X13_EnergyCode_encoder.pkl', 'rb')),
    'X14_HVAC': load(open('Model_Heating_1104/X14_HVAC_encoder.pkl', 'rb'))
}

# Load pre-trained encoders for the cooling model
label_encoders_cooling = {
    'X1_Type': load(open('Model_Cooling_1104/X1_Type_encoder.pkl', 'rb')),
    'X3_Shape': load(open('Model_Cooling_1104/X3_Shape_encoder.pkl', 'rb')),
    'X13_EnergyCode': load(open('Model_Cooling_1104/X13_EnergyCode_encoder.pkl', 'rb')),
    'X14_HVAC': load(open('Model_Cooling_1104/X14_HVAC_encoder.pkl', 'rb'))
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Convert the incoming JSON data to a DataFrame
    df = pd.DataFrame({
        'X1_Type': [data['Building_Type']],
        'X3_Shape': [data['Building_Shape']],
        'X5_Orientation': [data['Orientation']],
        'X6_Height': [data['Building_Height']],
        'X7_Stories': [data['Building_Stories']],
        'X9_WallArea': [data['Wall_Area']],
        'X10_WindowArea': [data['Window_Area']],
        'X12_RoofArea': [data['Roof_Area']],
        'X13_EnergyCode': [data['energy_code']],
        'X14_HVAC': [data['hvac_category']],
    })

    # Apply label encoders for heating prediction
    df_heating = df.copy()
    for col, encoder in label_encoders_heating.items():
        df_heating[col] = encoder.transform(df_heating[col])

    # Apply label encoders for cooling prediction
    df_cooling = df.copy()
    for col, encoder in label_encoders_cooling.items():
        df_cooling[col] = encoder.transform(df_cooling[col])

    # Make predictions
    heating_load_prediction = model_heating.predict(df_heating) / (data['Roof_Area'] * data['Building_Stories'])
    cooling_load_prediction = model_cooling.predict(df_cooling) / (data['Roof_Area'] * data['Building_Stories'])

    # Return both predictions as JSON
    return jsonify({
        'heating_load_prediction': heating_load_prediction.tolist(),
        'cooling_load_prediction': cooling_load_prediction.tolist()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
