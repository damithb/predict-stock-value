from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import random
import pandas as pd
import os
from datetime import datetime, timedelta

app = FastAPI()

# Models
class DataPoint(BaseModel):
    stock_id: str
    timestamp: str
    stock_price: float

class FileRequest(BaseModel):
    exchange_name: str
    file_name: str

class PredictionRequest(BaseModel):
    stock_id: str
    data_points: List[DataPoint]

class FileProcessingRequest(BaseModel):
    exchange_name: str
    data_points: List[DataPoint]
    predicted_data_points: List[DataPoint]

DATA_PATH = "./sample_data"


def load_csv(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)


@app.post("/get_data_points/")
def get_data_points(request: FileRequest) -> List[DataPoint]:
    file_path = os.path.join(DATA_PATH, request.exchange_name, request.file_name)
    
    try:
        print(file_path)
        data = load_csv(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

   

    # Random 10 values
    if len(data) < 10:
        raise HTTPException(status_code=400, detail="File has fewer than 10 rows")
    start_idx = random.randint(0, len(data) - 10)
    selected_data = data.iloc[start_idx:start_idx + 10]

    # creating the reponse
    response = [
        DataPoint(
            stock_id=row[0],
            timestamp=row[1],
            stock_price=row[2]
        )
        for _, row in selected_data.iterrows()
    ]
    return response


@app.post("/predict_stock_prices/")
def predict_stock_prices(request: PredictionRequest) -> List[Dict[str, Any]]:
    data_points = request.data_points
    if len(data_points) != 10:
        raise HTTPException(status_code=400, detail="Exactly 10 data points are required")
    
    prices = [dp.stock_price for dp in data_points]

    n1 = sorted(prices)[-2]  # 2nd highest value
    n2 = n1 - (n1 - prices[-1]) / 2 # 2nd predicted value based on requirement
    n3 = n2 - (n2 - n1) / 4 # 3rd predicted value based on requirement

    last_timestamp = datetime.strptime(data_points[-1].timestamp, "%d-%m-%Y")
    timestamps = [
        (last_timestamp + timedelta(days=i)).strftime("%d-%m-%Y") for i in range(1, 4)
    ]

    # Format the response
    predictions = [
        {"stock_id": request.stock_id, "timestamp": timestamps[0], "stock_price": n1},
        {"stock_id": request.stock_id, "timestamp": timestamps[1], "stock_price": n2},
        {"stock_id": request.stock_id, "timestamp": timestamps[2], "stock_price": n3},
    ]
    return predictions

@app.post("/process_file/")
def process_exchange_file(request: FileProcessingRequest):
    
    combined_data = [{
                "stock_id": dp.stock_id,
                "timestamp": dp.timestamp,
                "stock_price": dp.stock_price,
            }
            for dp in request.data_points
        ]
    combined_data_2 = [
            {
                "stock_id": dp.stock_id,
                "timestamp": dp.timestamp,
                "stock_price": dp.stock_price,
            }
            for dp in request.predicted_data_points
        ]
    combined_data = combined_data + combined_data_2
    output_file_path = os.path.join(request.exchange_name, f"combined_output.csv")
    pd.DataFrame(combined_data).to_csv(output_file_path, index=False)
    
    
    return {"message": "Processed and combined", "output_file": output_file_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
