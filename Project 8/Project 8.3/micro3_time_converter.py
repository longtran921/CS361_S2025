from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert_time():
    data = request.json
    input_time = data.get('input_time')
    target_format = data.get('target_format')

    if not input_time or target_format not in ['12', '24']:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        try:
            parsed = datetime.strptime(input_time, "%I:%M %p")
        except ValueError:
            parsed = datetime.strptime(input_time, "%H:%M")

        if target_format == '12':
            output = parsed.strftime("%I:%M %p")
        else:
            output = parsed.strftime("%H:%M")

        return jsonify({
            'input_time': input_time,
            'converted_time': output,
            'format': target_format
        })

    except Exception as e:
        return jsonify({'error': 'Failed to parse time', 'details': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
