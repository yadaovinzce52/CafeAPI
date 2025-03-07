from random import choice

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def serialize(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random():
    results = db.session.execute(db.select(Cafe))
    all_cafes = results.scalars().all()
    random_cafe = choice(all_cafes)

    return jsonify(cafe=random_cafe.serialize())

@app.route("/all", methods=["GET"])
def get_all():
    results = db.session.execute(db.select(Cafe))
    all_cafes = results.scalars().all()
    return jsonify(cafes=[cafe.serialize() for cafe in all_cafes])

@app.route("/search", methods=["GET"])
def search_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.serialize() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


    # HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    new_name = request.form.get("name")
    new_map_url = request.form.get("map_url")
    new_img_url = request.form.get("img_url")
    new_location = request.form.get("location")
    new_seats = request.form.get("seats")
    new_has_toilet = request.form.get("has_toilet")
    new_has_wifi = request.form.get("has_wifi")
    new_has_sockets = request.form.get("has_sockets")
    new_can_take_calls = request.form.get("can_take_calls")
    new_coffee_price = request.form.get("coffee_price")

    db.session.add(Cafe(name=new_name,
                        map_url=new_map_url,
                        img_url=new_img_url,
                        location=new_location,
                        seats=new_seats,
                        has_toilet=bool(new_has_toilet),
                        has_wifi=bool(new_has_wifi),
                        has_sockets=bool(new_has_sockets),
                        can_take_calls=bool(new_can_take_calls),
                        coffee_price=new_coffee_price))
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

    # HTTP PUT/PATCH - Update Record

    # HTTP DELETE - Delete Record

if __name__ == '__main__':
    app.run(debug=True)
