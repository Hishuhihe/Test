# Flask Account Management API

M?t API qu?n l� t�i kho?n ??n gi?n ???c x�y d?ng b?ng Flask v� SQLAlchemy.

## requirements

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Marshmallow
- SQLite

## setup 

1. Clone repository:

 ```bash
   git clone https://github.com/username/repository-name.git
   cd repository-name
```
2. Create virtual environment and install requirements:
    python -m venv venv
    source venv/bin/activate   #  Windows: `venv\Scripts\activate`
    pip install -r requirements.txt
3. Run the application once to create the database:
    python app.py
4. Run app: 
    python app.py
The application will run on http://127.0.0.1:5000/.

## API Endpoints
1. T?o t�i kho?n:

    URL: /accounts/create-new
    Method: POST
    ``` Body: 
    {
      "login": "exampleUser",
      "password": "ExamplePassword1",
      "phone": "123-456-7890"
    }

2. L?y danh s�ch t�i kho?n:

    URL: /accounts/get-list
    Method: GET
    Params:
    page (optional, default: 1)
    per_page (optional, default: 10)

3. L?y th�ng tin t�i kho?n:

    URL: /accounts/get/<registerID>
    Method: GET
    Params: registerID (ID c?a t�i kho?n)
    
4. C?p nh?t t�i kho?n:

   URL: /accounts/update/<registerID>
   Method: PUT
   Params: registerID (ID c?a t�i kho?n)
   ```Body:
    {
    "login": "newLogin",
    "password": "NewPassword1",
    "phone": "098-765-4321"
    }

5. X�a t�i kho?n:

    URL: /accounts/delete/<registerID>
    Method: DELETE
    Params:
    registerID (ID c?a t�i kho?n)





