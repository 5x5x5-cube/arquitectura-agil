from flask import Flask, jsonify
from monitor import get_system_health

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from API Gateway!'

@app.route('/health-checker')
def health_check():
    return jsonify(get_system_health())

if __name__ == '__main__':
    app.run(debug=True)
