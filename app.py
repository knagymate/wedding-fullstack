from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit_form", methods=["POST"])
def handle_form():
    with app.app_context():
        json = request.json
        user = User(
            name=json.get("name"),
            email=json.get("email"),
            is_join=json.get("is_join"),
            is_shuttle=json.get("is_shuttle"),
            is_food=json.get("is_food"),
            is_hotel=json.get("is_hotel"),
            shuttle_num=json.get("shuttle_num"),
            food_comment=json.get("food_comment"),
            hotel_num=json.get("hotel_num"),
            comment=json.get("comment"),
        )
        for guest in json.get("guests"):
            user.guests.append(Guest(name=guest.get("name"), age=guest.get("age")))
        db.session.add(user)
        db.session.commit()
    return "Form submitted!"


@app.route("/get_guests", methods=["GET"])
def get_guests():
    guests = Guest.query.all()
    users = User.query.all()
    user_jsons = []
    for user in users:
        user_json = {
            "id": user.id,
            "guests": [],
            "name": user.name,
            "email": user.email,
            "is_join": user.is_join,
            "shuttle_num": user.shuttle_num if user.is_shuttle else 0,
            "food_comment": user.food_comment if user.is_food else "",
            "hotel_num": user.hotel_num if user.is_hotel else 0,
            "comment": user.comment,
        }
        user_jsons.append(user_json)
        for guest in guests:
            if guest.user_id == user.id:
                user_jsons.append(
                    {"id": guest.id, "name": guest.name, "age": guest.age}
                )
    return user_jsons


@app.route("/show_guests", methods=["GET"])
def show_guests():
    return render_template("show_guests.html")


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    is_join = db.Column(db.Boolean, nullable=False)
    guests = db.relationship("Guest", backref="user", lazy=True)
    is_shuttle = db.Column(db.Boolean, nullable=False)
    is_food = db.Column(db.Boolean, nullable=False)
    is_hotel = db.Column(db.Boolean, nullable=False)
    shuttle_num = db.Column(db.Integer, nullable=True)
    food_comment = db.Column(db.String, nullable=True)
    hotel_num = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String, nullable=True)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
