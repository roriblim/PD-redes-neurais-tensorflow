# Importando as bibliotecas necessárias
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import joblib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de Predição de Churn em E-Commerce", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # quem pode acessar a API
    allow_credentials=True,
    allow_methods=["POST"],   
    allow_headers=["*"],   
)

try:
    scaler = joblib.load("models/robust_scaler_final.pkl")
except FileNotFoundError:
    scaler = None
    print("Arquivo do escalonador não encontrado. A aplicação continuará sem ele.")

try:
    model = load_model('models/model_final_nn.h5')
except (FileNotFoundError, IOError):
    model = None
    print("Arquivo do modelo não encontrado. A aplicação continuará sem ele.")

# Definindo o modelo de dados de entrada com Pydantic
# Isso garante que os dados recebidos na requisição terão o formato esperado.
class InputData(BaseModel):
    Tenure: float
    CityTier: int = Field(..., ge=1, le=3) # Garante que o valor esteja entre 1 e 3
    WarehouseToHome: float
    HourSpendOnApp: int
    NumberOfDeviceRegistered: int
    SatisfactionScore: int = Field(..., ge=1, le=5) # Garante que o valor esteja entre 1 e 5
    NumberOfAddress: int
    DaySinceLastOrder: int
    CashbackAmount: float
    Complain: int = Field(..., ge=0, le=1) # Garante que o valor seja 0 ou 1
    PreferedOrderCat: str
    MaritalStatus: str
    PreferredPaymentMode: str
    PreferredLoginDevice: str
    Gender: str

    class Config:
        schema_extra = {
            "example": {
                "Tenure": 10.0,
                "CityTier": 1,
                "WarehouseToHome": 20.0,
                "HourSpendOnApp": 3,
                "NumberOfDeviceRegistered": 3,
                "SatisfactionScore": 5,
                "NumberOfAddress": 2,
                "DaySinceLastOrder": 5,
                "CashbackAmount": 150.0,
                "Complain": 0,
                "PreferedOrderCat": "Laptop & Accessory",
                "MaritalStatus": "Married",
                "PreferredPaymentMode": "Credit Card",
                "PreferredLoginDevice": "Mobile Phone",
                "Gender": "Male"
            }
        }

# 4. Criando o endpoint de inferência
@app.post("/predict")
async def predict(data: InputData):
    """
    Recebe os dados de entrada, realiza o pré-processamento,
    aplica o escalonador, faz a inferência com o modelo
    e retorna a probabilidade.
    """
    if scaler is None or model is None:
        return {"erro": "Modelo ou escalonador não carregado."}

    # Pré-processamento e One-Hot Encoding manual
    # Criando um dicionário para facilitar a conversão
    processed_data = {
        'Tenure': data.Tenure,
        'CityTier': data.CityTier,
        'WarehouseToHome': data.WarehouseToHome,
        'HourSpendOnApp': data.HourSpendOnApp,
        'NumberOfDeviceRegistered': data.NumberOfDeviceRegistered,
        'SatisfactionScore': data.SatisfactionScore,
        'NumberOfAddress': data.NumberOfAddress,
        'DaySinceLastOrder': data.DaySinceLastOrder,
        'CashbackAmount': data.CashbackAmount,
        'Complain': data.Complain,
        'PreferedOrderCat_Laptop & Accessory': 1 if data.PreferedOrderCat == "Laptop & Accessory" else 0,
        'PreferedOrderCat_Mobile Phone': 1 if data.PreferedOrderCat == "Mobile Phone" else 0,
        'MaritalStatus_Single': 1 if data.MaritalStatus == "Single" else 0,
        'MaritalStatus_Married': 1 if data.MaritalStatus == "Married" else 0,
        'PreferredLoginDevice_Mobile Phone': 1 if data.PreferredLoginDevice == "Mobile Phone" else 0,
        'PreferredPaymentMode_COD': 1 if data.PreferredPaymentMode == "COD" else 0,
        'PreferredLoginDevice_Phone': 1 if data.PreferredLoginDevice == "Phone" else 0,
        'PreferredPaymentMode_E wallet': 1 if data.PreferredPaymentMode == "E wallet" else 0,
        'PreferredLoginDevice_Computer': 1 if data.PreferredLoginDevice == "Computer" else 0,
        'PreferredPaymentMode_Debit Card': 1 if data.PreferredPaymentMode == "Debit Card" else 0,
        'Gender_Female': 1 if data.Gender == "Female" else 0,
        'PreferredPaymentMode_Credit Card': 1 if data.PreferredPaymentMode == "Credit Card" else 0
    }

    # Garantindo a ordem correta das features
    feature_order = [
        'Tenure', 'CityTier', 'WarehouseToHome', 'HourSpendOnApp', 'NumberOfDeviceRegistered',
        'SatisfactionScore', 'NumberOfAddress', 'DaySinceLastOrder', 'CashbackAmount', 'Complain',
        'PreferedOrderCat_Laptop & Accessory', 'PreferedOrderCat_Mobile Phone', 'MaritalStatus_Single',
        'MaritalStatus_Married', 'PreferredLoginDevice_Mobile Phone', 'PreferredPaymentMode_COD',
        'PreferredLoginDevice_Phone', 'PreferredPaymentMode_E wallet', 'PreferredLoginDevice_Computer',
        'PreferredPaymentMode_Debit Card', 'Gender_Female', 'PreferredPaymentMode_Credit Card'
    ]

    # Convertendo para um array numpy na ordem correta
    input_array = np.array([processed_data[feature] for feature in feature_order]).reshape(1, -1)

    # Aplicando o escalonador
    scaled_data = scaler.transform(input_array)

    # Realizando a inferência
    prediction = model.predict(scaled_data)

    # A saída do modelo de rede neural para classificação geralmente é um array.
    # Vamos extrair a probabilidade (assumindo que seja a primeira e única saída).
    probability = float(prediction[0][0])

    # Retornando o resultado
    return {"probabilidade": probability}

# Executando a API
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)