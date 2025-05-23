from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import threading

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timer.db'
db = SQLAlchemy(app)

# Database Models
class Duration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False)
    seconds = db.Column(db.Integer, nullable=False)

class Countdown(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration_id = db.Column(db.Integer, db.ForeignKey('duration.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

# Initialize DB
with app.app_context():
    db.create_all()
    # Seed example durations if not present
    if not Duration.query.all():
        db.session.add_all([
            Duration(label='Test', seconds=15),
            Duration(label='Short Break', seconds=5*60),
            Duration(label='Long Break', seconds=15*60)
        ])
        db.session.commit()

# Start Countdown
@app.route('/start', methods=['POST'])
def start_countdown():
    data = request.json
    duration_id = data.get('duration_id')

    duration = Duration.query.get(duration_id)
    if not duration:
        return jsonify({'error': 'Invalid duration ID'}), 400

    now = datetime.utcnow()
    end_time = now + timedelta(seconds=duration.seconds)
    countdown = Countdown(duration_id=duration.id, start_time=now, end_time=end_time)
    db.session.add(countdown)
    db.session.commit()

    return jsonify({
        'message': 'Countdown started',
        'countdown_id': countdown.id,
        'ends_at': end_time.isoformat()
    })

# Get Active Countdown
@app.route('/status/<int:countdown_id>', methods=['GET'])
def get_status(countdown_id):
    countdown = Countdown.query.get(countdown_id)
    if not countdown:
        return jsonify({'error': 'Countdown not found'}), 404

    remaining = (countdown.end_time - datetime.utcnow()).total_seconds()
    remaining = max(0, int(remaining))
    if remaining == 0 and countdown.is_active:
        countdown.is_active = False
        db.session.commit()

    return jsonify({
        'countdown_id': countdown.id,
        'remaining_seconds': remaining,
        'is_active': countdown.is_active
    })

# List Available Durations
@app.route('/durations', methods=['GET'])
def list_durations():
    durations = Duration.query.all()
    return jsonify([
        {'id': d.id, 'label': d.label, 'seconds': d.seconds}
        for d in durations
    ])

if __name__ == '__main__':
    app.run(debug=True)
