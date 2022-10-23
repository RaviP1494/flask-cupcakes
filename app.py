"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, redirect, jsonify, make_response
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:drowssap@localhost:5432/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home_view():
    cakes = Cupcake.query.all()
    return render_template('home.html')
    
@app.route('/api/cupcakes/', methods=["GET"])
def list_cupcakes():
    cakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    resp = make_response(jsonify(cupcakes = cakes))
    return resp

@app.route('/api/cupcakes/', methods=["POST"])
def create_cupcake():
    data = request.json
    
    flavor = data['flavor']
    size = data['size']
    rating = data['rating']
    image = data['image'] if data['image'] else None

    cake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cake)
    db.session.commit()
    resp = make_response(jsonify(cupcake = cake.serialize()))
    resp.status_code = 201
    return resp

@app.route('/api/cupcakes/<int:cid>/')
def get_cupcake(cid):
    cake = Cupcake.query.get_or_404(cid)
    resp = jsonify(cupcake = cake.serialize())
    resp.status_code = 200
    return resp


@app.route('/api/cupcakes/<int:cid>/update/', methods=["PATCH"])
def update_cupcake(cid):
    data = request.json

    flavor = data['flavor']
    size = data['size']
    rating = data['rating']
    image = data['image'] if data['image'] else None

    cake = Cupcake.query.get_or_404(cid)

    cake.flavor = flavor
    cake.size = size
    cake.rating = rating
    if(image):
        cake.image = image
    
    print(flavor)
    db.session.add(cake)
    db.session.commit()

    resp = jsonify(cupcake = cake.serialize())
    resp.status_code = 204

    return resp

@app.route('/api/cupcakes/<int:cid>/delete/', methods=["DELETE"])
def delete_cupcake(cid):
    cake = Cupcake.query.get_or_404(cid).delete()
    db.session.delete(cake)
    db.session.commit()

    resp = make_response(jsonify(message = "deleted"))
    resp.status_code = 200

    return resp
    
    
