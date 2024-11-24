from os import name
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
# Initialize SQLAlchemy
db = SQLAlchemy(app)

class Drinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description=db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"
    
@app.route('/')
def index():
    return 'Hello User!'

@app.route('/drinks',methods=['POST'])
def add_drink():
    drink = Drinks(name=request.json['name'],description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {"id":drink.id}

@app.route('/drinks/<int:id>',methods=['POST'])
def add_drink_at(id):
    drink = Drinks(id=id, name=request.json['name'],description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {"id":drink.id}

@app.route('/drinks/<int:id>',methods=['GET'])
def get_drink(id):
    drink=Drinks.query.get(id)
    if drink is None:
        return {'Message':f"Drink with id {id} is not found!"}
    
    return {'id': drink.id,"name":drink.name, "description": drink.description}

@app.route('/drinks',methods=['GET'])
def get_drinks():
    drinks=Drinks.query.all()
    if drinks is None:
        return {'Message':'Drinks not found'}
    output=[]
    for drink in drinks:
        drink_data = {'id': drink.id,'name': drink.name,'description':drink.description}
        output.append(drink_data)
    return {"Drinks":output}

@app.route('/drinks/<int:id>', methods=['PUT'])
def update_drink(id):
    if id is None:
        return {"message":f"Drink with id {id} does not exist!"}

    drink = Drinks.query.get(id)

    # Update fields if they exist in the payload
    
    drink.name = request.json['name']
    drink.description = request.json['description']


    # Commit changes
    db.session.commit()
    return jsonify({"message" : f"Drink with id {id} updated!"})


@app.route('/drinks/<int:id>',methods=['DELETE'])
def delete_drink(id):
    drink = Drinks.query.get(id)
    if drink is None:
        return {'error':'Drink not found'}

    db.session.delete(drink)
    db.session.commit()
    return {'deleted drink': id}
    
if __name__ == "__main__":
    app.run(debug=True)

