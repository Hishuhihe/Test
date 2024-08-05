## API ShowSerialpaso

## Features

- Endpoint: `/api/showSerialpaso/`
- Method: POST
- Content-Type: application/json
- Retrieves HTML files based on file name, environment, and server parameters
- Returns file content in base64 encoding

## Requirements

- Python 3.6+
- Flask

## Installation

1. Clone this repository:
   git clone https://github.com/Hishuhihe/Test.git
   cd test_2
   
2. Install the required packages:
   pip install flask

## Run app 
1. Start the Flask application:
  python app.py

3. The server will start on `http://127.0.0.1:5000/`

5. Send a POST request to `http://127.0.0.1:5000/api/showSerialpaso/` with a JSON body:
```json
{
  "file": "example",
  "app_env": 0,
  "contract_server": 1
}



   
