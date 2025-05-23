from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app)

# Sample model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50))
    cuisine = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    name = db.Column(db.String(100))
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(20))

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    step_number = db.Column(db.Integer)
    instruction = db.Column(db.Text)

with app.app_context():
    db.create_all()

    # Just an example recipes if none exist
    if not Recipe.query.first():
        sample_recipe = Recipe(
            title='Spaghetti Bolognese',
            description='A classic Italian pasta dish with meat sauce.',
            difficulty='Medium',
            cuisine='Italian'
        )
        db.session.add(sample_recipe)
        db.session.commit()
        ingredients = [
            Ingredient(recipe_id=sample_recipe.id, name='Spaghetti', quantity=200, unit='grams'),
            Ingredient(recipe_id=sample_recipe.id, name='Ground Beef', quantity=150, unit='grams'),
            Ingredient(recipe_id=sample_recipe.id, name='Tomato Sauce', quantity=100, unit='ml'),
        ]
        db.session.add_all(ingredients)
        steps = [
            Step(recipe_id=sample_recipe.id, step_number=1, instruction='Boil spaghetti until al dente.'),
            Step(recipe_id=sample_recipe.id, step_number=2, instruction='Brown the ground beef in a skillet.'),
            Step(recipe_id=sample_recipe.id, step_number=3, instruction='Add tomato sauce and simmer for 15 minutes.'),
            Step(recipe_id=sample_recipe.id, step_number=4, instruction='Combine spaghetti and sauce before serving.')
        ]
        db.session.add_all(steps)

        db.session.commit()


@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()
    steps = Step.query.filter_by(recipe_id=recipe_id).order_by(Step.step_number).all()

    return jsonify({
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'difficulty': recipe.difficulty,
        'cuisine': recipe.cuisine,
        'created_at': recipe.created_at.isoformat(),
        'ingredients': [
            {'name': ing.name, 'quantity': ing.quantity, 'unit': ing.unit}
            for ing in ingredients
        ],
        'steps': [
            {'step_number': s.step_number, 'instruction': s.instruction}
            for s in steps
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
