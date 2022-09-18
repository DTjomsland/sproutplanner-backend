from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import psycopg2

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://david:Cygyxy64rtfg@localhost:5432/sprout_planner"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

class CardSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'user_email', 'user_password')


# User table creation
class Users(db.Model):
        __tablename__="users"

        user_id = db.Column(db.Integer, primary_key=True)
        user_email = db.Column(db.String, unique=True, nullable=False)
        user_password = db.Column(db.Text(60), nullable=False)


@app.cli.command('create')
def create_db():
    db.create_all()
    print("Creating tables...")

# Seeding the database
@app.cli.command('seed')
def seed_db():
    users = Users(
        user_email="user@gmail.com",
        user_password="password"
    )

    db.session.add(users)

    db.session.commit()
    print("Seeding tables...")

@app.route('/')
def welcome():
    return "Sprout Planner under construction"

@app.route('/users')
def users():
    users_list = Users.query.all()
    result = CardSchema(many=True).dump(users_list)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')