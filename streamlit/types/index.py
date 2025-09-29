# Definindo os tipos de dados para a API de predição de churn

from pydantic import BaseModel, Field

class InputData(BaseModel):
    Tenure: float
    CityTier: int = Field(..., ge=1, le=3)
    WarehouseToHome: float
    HourSpendOnApp: int
    NumberOfDeviceRegistered: int
    SatisfactionScore: int = Field(..., ge=1, le=5)
    NumberOfAddress: int
    DaySinceLastOrder: int
    CashbackAmount: float
    Complain: int = Field(..., ge=0, le=1)
    PreferedOrderCat: str
    MaritalStatus: str
    PreferredPaymentMode: str
    PreferredLoginDevice: str
    Gender: str