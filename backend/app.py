from flask import Flask, request, jsonify
from config import Config
from models import db, User, Expense
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from ai_service import parse_expense
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=["http://localhost:5174"])

db.init_app(app)
jwt = JWTManager(app)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "API Running"


@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if data is None:
        return jsonify({
            "message": "JSON body is required."
        }), 400

    if not isinstance(data, dict):
        return jsonify({
            "message": "JSON body must be an object."
        }), 400

    username = data.get("username", "")
    email = data.get("email", "")
    password = data.get("password", "")

    if not all(isinstance(i, str) for i in (username, email, password)):
        return jsonify({
            "message": "All fields must be strings."
        }), 400

    username = username.strip()
    email = email.strip().lower()
    password = password.strip()

    if not username or not email or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "message": "Password must be at least 8 characters."
        }), 400

    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({
            "message": "Invalid email format"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 409

    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully"
    }), 201


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    if data is None:
        return jsonify({
            "message": "JSON body is required."
        }), 400

    if not isinstance(data, dict):
        return jsonify({
            "message": "JSON body must be an object."
        }), 400

    email = data.get("email", "")
    password = data.get("password", "")

    if not all(isinstance(i, str) for i in (email, password)):
        return jsonify({
            "message": "All fields must be strings."
        }), 400

    email = email.strip().lower()
    password = password.strip()

    if not email or not password:
        return jsonify({
            "message": "Email and password are required."
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    if not check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 200


@app.route("/protected")
@jwt_required()
def identity_user():
    current_user_id = get_jwt_identity()

    return jsonify({
        "message": "Access granted",
        "user_id": current_user_id
    }), 200


@app.route("/ai/parse-expense", methods=["POST"])
@jwt_required()
def ai_parse_expense():
    data = request.get_json()
    if data is None:
        return jsonify({
            "message": "JSON body is required."
        }), 400

    if not isinstance(data, dict):
        return jsonify({
            "message": "JSON body must be an object."
        }), 400

    text = data.get("text", "")
    if not (isinstance(text, str)):
        return jsonify({
            "message": "All fields must be strings."
        }), 400

    text = text.strip()

    if not text:
        return jsonify({
            "message": "All fields are required"
        }), 400

    current_user_id = int(get_jwt_identity())
    user = User.query.filter_by(id=current_user_id).first()

    if not user:
        return jsonify({
            "message": "User no longer exists."
        }), 401

    parse_payment = parse_expense(text).model_dump()

    new_expense = Expense(
        amount=parse_payment.get("amount"),
        merchant=parse_payment.get("merchant"),
        category=parse_payment.get("category"),
        description=parse_payment.get("description"),
        user_id=current_user_id

    )
    db.session.add(new_expense)
    db.session.commit()

    return jsonify({
        "message": "Expense created successfully",
        "expense_id": new_expense.id,
        "expense": parse_payment
    }), 201


@app.route("/expenses", methods=["GET"])
@jwt_required()
def get_expenses():
    current_user_id = int(get_jwt_identity())
    expenses = Expense.query.filter_by(
        user_id=current_user_id
    ).all()

    expense_list = []

    for expense in expenses:
        expense_list.append({
            "id": expense.id,
            "amount": float(expense.amount),
            "merchant": expense.merchant,
            "category": expense.category,
            "description": expense.description,
            "user_id": expense.user_id
        })

    return jsonify({
        "expenses": expense_list
    }), 200


@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expenses(expense_id):
    current_user_id = int(get_jwt_identity())
    expense_delete = Expense.query.filter_by(
        id=expense_id, user_id=current_user_id).first()

    if not expense_delete:
        return jsonify({
            "message": "Expense not found"
        }), 404

    db.session.delete(expense_delete)
    db.session.commit()

    return jsonify({
        "message": "Expense has been deleted"
    }), 200


@app.route("/expenses/<int:expense_id>", methods=["PATCH"])
@jwt_required()
def update_expense(expense_id):
    current_user_id = int(get_jwt_identity())

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=current_user_id
    ).first()

    if not expense:
        return jsonify({
            "message": "Expense not found"
        }), 404
    data = request.get_json()

    if data is None:
        return jsonify({
            "message": "JSON body is required."
        }), 400

    if not isinstance(data, dict):
        return jsonify({
            "message": "JSON body must be an object."
        }), 400

    if not data:
        return jsonify({
            "message": "No fields to update."
        }), 400

    allowed_fields = {"amount", "merchant", "category", "description"}
    if not allowed_fields.intersection(data.keys()):
        return jsonify({
            "message": "No fields to update."
        }), 400

    amount_num = data.get("amount")
    if "amount" in data:
        if not (isinstance(amount_num, (int, float))) or isinstance(amount_num, bool):
            return jsonify({
                "message": "Amount must be a number"
            }), 400

        expense.amount = amount_num

    merchant_str = data.get("merchant", "")
    if "merchant" in data:
        if not isinstance(merchant_str, (str, type(None))):
            return jsonify({
                "message": "Merchant must be a string or null"
            }), 400
        if isinstance(merchant_str, str):
            merchant_str = merchant_str.strip()
        if not merchant_str:
            merchant_str = None
        expense.merchant = merchant_str

    category_str = data.get("category", "")
    if "category" in data:
        if not isinstance(category_str, str):
            return jsonify({
                "message": "Category must be a string"
            }), 400
        category_str = category_str.strip()

        if not category_str:
            return jsonify({
                "message": "Category cannot be empty"
            }), 400
        expense.category = category_str

    description_str = data.get("description", "")
    if "description" in data:
        if not isinstance(description_str, str):
            return jsonify({
                "message": "description must be a string"
            }), 400

        description_str = description_str.strip()
        if not description_str:
            return jsonify({
                "message": "description cannot be empty"
            }), 400
        expense.description = description_str

    db.session.commit()

    return jsonify({
        "message": "Expense updated successfully",
        "expense": {
            "id": expense.id,
            "amount": float(expense.amount),
            "merchant": expense.merchant,
            "category": expense.category,
            "description": expense.description,
            "user_id": expense.user_id
        }
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
