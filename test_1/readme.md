# Flask Account Management API

M?t API qu?n lý tài kho?n ??n gi?n ???c xây d?ng b?ng Flask và SQLAlchemy.

## requirements

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Marshmallow
- SQLite

## setup 

1. Clone repository:

 ```bash
   git clone https://github.com/Hishuhihe/Test.git
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
1. T?o tài kho?n:

    URL: /accounts/create-new
    Method: POST
    ``` Body: 
    {
      "login": "exampleUser",
      "password": "ExamplePassword1",
      "phone": "123-456-7890"
    }

2. L?y danh sách tài kho?n:

    URL: /accounts/get-list
    Method: GET
    Params:
    page (optional, default: 1)
    per_page (optional, default: 10)

3. L?y thông tin tài kho?n:

    URL: /accounts/get/<registerID>
    Method: GET
    Params: registerID (ID c?a tài kho?n)
    
4. C?p nh?t tài kho?n:

   URL: /accounts/update/<registerID>
   Method: PUT
   Params: registerID (ID c?a tài kho?n)
   ```Body:
    {
    "login": "newLogin",
    "password": "NewPassword1",
    "phone": "098-765-4321"
    }

5. Xóa tài kho?n:

    URL: /accounts/delete/<registerID>
    Method: DELETE
    Params:
    registerID (ID c?a tài kho?n)





