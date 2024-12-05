# predict-stock-value

## Table of Contents
- [Installation](#installation)
- [Usage](#Usage)
- [API Endpoints](#api-endpoints)

## Installation
To set up this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/damithb/predict-stock-value/
   cd predict-stock-value
   ```
2. Install the required packages:
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage
1. Place your stock data CSV files in the `sample_data` directory.
2. Run the Flask application:
   ```bash
   python predict-stock-value.py
   ```
3. Use the API to make predictions.

## API Endpoints
### `POST /predict`
Predicts stock prices for a given exchange.

**Request Body:**
```json
{
    "exchange_name": "your_exchange_type",
    "file_name": filename.csv
}
```

- `exchange_name`: name of the exchange folder name.
- `file_name`: file name.

**Request Body:**
```json
{
    "exchange_name": "your_exchange_type",
    "file_name": filename.csv
}
```

- `exchange_name`: name of the exchange folder name.
- `file_name`: file name.




