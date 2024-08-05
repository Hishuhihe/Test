from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, validates, validate
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
db = SQLAlchemy(app)

# logging config
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Model definition
class Account(db.Model):
    registerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(20))

    @validates('login')
    def validate_login(self, key, login):
        if not login:
            raise ValueError("Login không được để trống")
        if len(login) < 3:
            raise ValueError("Login phải có ít nhất 3 ký tự")
        if not login.isalnum():
            raise ValueError("Login chỉ được chứa chữ cái và số")
        return login

    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise ValueError("Password không được để trống")
        if len(password) < 8:
            raise ValueError("Password phải có ít nhất 8 ký tự")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password phải chứa ít nhất một số")
        if not any(char.isupper() for char in password):
            raise ValueError("Password phải chứa ít nhất một chữ hoa")
        return password

    def __repr__(self):
        return f'<Account {self.login}>'

# Schema definition
class AccountSchema(Schema):
    registerID = fields.Int(dump_only=True)
    login = fields.Str(required=True, validate=[
        validate.Length(min=3, max=20, error="Login phải có độ dài từ 3 đến 20 ký tự"),
        validate.Regexp(r'^[a-zA-Z0-9]+$', error="Login chỉ được chứa chữ cái và số")
    ])
    password = fields.Str(required=True, validate=[
        validate.Length(min=8, max=40, error="Password phải có độ dài từ 8 đến 40 ký tự"),
        validate.Regexp(r'(?=.*\d)(?=.*[A-Z])', error="Password phải chứa ít nhất một số và một chữ hoa")
    ])
    phone = fields.Str(validate=validate.Length(max=20))

    @validates('login')
    def validate_unique_login(self, value):
        if Account.query.filter_by(login=value).first():
            raise ValidationError("Login đã tồn tại")

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

@app.route('/accounts/create-new', methods=['POST'])
def create_account():
    try:
        data = request.json
        new_account = Account(**account_schema.load(data))
        db.session.add(new_account)
        db.session.commit()
        logger.info(f"Tạo tài khoản mới đã tạo thành công: {new_account.login}")
        return jsonify(account_schema.dump(new_account)), 201
    except ValidationError as err:
        logger.error(f"Lỗi xác thực khi tạo tài khoản: {err.messages}")
        return jsonify({"errors": err.messages, }), 400
    except ValueError as err:
        logger.error(f"Lỗi giá trị khi tạo tài khoản: {str(err)}")
        return jsonify({"message": f"Lỗi giá trị: {str(err)}."}), 400
    except Exception as e:
        logger.error(f"Lỗi khi tạo tài khoản: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Có lỗi xảy ra khi tạo tài khoản"}), 500

@app.route('/accounts/get-list', methods=['GET'])
def get_accounts():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        accounts = Account.query.paginate(page=page, per_page=per_page, error_out=False)
        result = accounts_schema.dump(accounts.items)
        return jsonify({
            "accounts": result,
            "total": accounts.total,
            "pages": accounts.pages,
            "current_page": page
        })
    except Exception as e:
        logger.error(f"Lỗi khi lấy danh sách tài khoản: {str(e)}")
        return jsonify({"message": "Có lỗi xảy ra khi lấy danh sách tài khoản"}), 500


@app.route('/accounts/get/<int:registerID>', methods=['GET'])
def get_account(registerID):
    try:
        account = Account.query.get(registerID)
        if account is None:
            logger.warning(f"Không tồn tại tài khoản với registerID: {registerID}")
            return jsonify({"message": "Tài khoản không tồn tại"}), 404

        return jsonify(account_schema.dump(account))
    except Exception as e:
        logger.error(f"Lỗi khi lấy thông tin tài khoản {registerID}: {str(e)}")
        return jsonify({"message": "Có lỗi xảy ra khi lấy thông tin tài khoản"}), 500

@app.route('/accounts/update/<int:registerID>', methods=['PUT'])
def update_account(registerID):
    try:
        account = Account.query.get_or_404(registerID)
        data = request.json
        if 'login' in data and data['login'] != account.login:
            existing = Account.query.filter_by(login=data['login']).first()
            if existing:
                raise ValidationError({"login": ["Login đã tồn tại"]})
        account_schema.load(data, partial=True)
        for key, value in data.items():
            setattr(account, key, value)
        db.session.commit()
        logger.info(f"Cập nhật tài khoản: {account.login}")
        return jsonify(account_schema.dump(account))
    except ValidationError as err:
        logger.error(f"Lỗi xác thực khi cập nhật tài khoản {registerID}: {err.messages}")
        return jsonify(err.messages), 400
    except ValueError as err:
        logger.error(f"Lỗi giá trị khi cập nhật tài khoản {registerID}: {str(err)}")
        return jsonify({"message": str(err)}), 400
    except Exception as e:
        logger.error(f"Lỗi khi cập nhật tài khoản {registerID}: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Có lỗi xảy ra khi cập nhật tài khoản"}), 500

@app.route('/accounts/delete/<int:registerID>', methods=['DELETE'])
def delete_account(registerID):
    try:
        account = Account.query.get_or_404(registerID)
        db.session.delete(account)
        db.session.commit()
        logger.info(f"Xóa tài khoản: {account.login}")
        return jsonify({"message": "Tài khoản đã được xóa"}), 200
    except Exception as e:
        logger.error(f"Lỗi khi xóa tài khoản {registerID}: {str(e)}")
        return jsonify({"message": "Có lỗi xảy ra khi xóa tài khoản"}), 500

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
