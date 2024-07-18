from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Monster, monster_schema, monsters_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/monsters', methods=['POST'])
@token_required
def create_monster(current_user_token):
    name = request.json['name']
    height = request.json['height']
    weight = request.json['weight']
    type = request.json['type']
    user_token = current_user_token.token

    monster = Monster(
        name=name,
        height=height,
        weight=weight,
        type=type,
        user_token=user_token
    )

    db.session.add(monster)
    db.session.commit()

    response = monster_schema.dump(monster)
    return jsonify(response)
    
@api.route('/monsters', methods = ['GET'])
@token_required
def get_monsters(current_user_token):
    a_user = current_user_token.token
    monsters = Monster.query.filter_by(user_token = a_user).all()
    response = monsters_schema.dump(monsters)
    return jsonify(response)

@api.route('/monsters/<id>', methods = ['GET'])
@token_required
def get_individual_monster(current_user_token, id):
    monster = Monster.query.get(id)
    response = monster_schema.dump(monster)
    return jsonify(response)

@api.route('/monsters/<id>', methods=['POST','PUT'])
@token_required
def update_monster(current_user_token, id):
    monster = Monster.query.get(id)
    monster.name = request.json['name']
    monster.height = request.json['height']
    monster.weight = request.json['weight']
    monster.type = request.json['type']
    monster.user_token = current_user_token.token

    db.session.commit()

    response = monster_schema.dump(monster)
    return jsonify(response)
    
@api.route('/monsters/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    monster = Monster.query.get(id)
    db.session.delete(monster)
    db.session.commit()
    response = monster_schema.dump(monster)
    return jsonify(response)