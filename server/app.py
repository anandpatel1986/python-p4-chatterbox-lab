from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by("created_at").all()
        messages_dict = []
        for message in messages:
            messages_dict.append(message.to_dict())
        response = make_response(jsonify(messages_dict), 200)
        return response
    elif request.method == "POST":
        new_data = request.get_json()
        new_message = Message(body=new_data["body"], username=new_data["username"])
        db.session.add(new_message)
        db.session.commit()
        response = make_response(jsonify(new_message.to_dict()), 201)
        return response


@app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == "PATCH":
        data_to_be_updated = request.get_json()
        for attr in data_to_be_updated:
            setattr(message, attr, data_to_be_updated[attr])
        db.session.add(message)
        db.session.commit()
        response = make_response(jsonify(message.to_dict()), 200)
        return response

    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        response = make_response(jsonify({"note": "message deleted successfully"}), 200)
        return response


if __name__ == "__main__":
    app.run(port=5555)
