from flask import Flask, jsonify, request
from monitor import get_system_health
from security.auth import authenticate

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from API Gateway!'

@app.route('/health-checker')
def health_check():
    return jsonify(get_system_health())

@app.route('/auth', methods=['POST'])
def auth():
    return authenticate(request.json)

if __name__ == '__main__':
    app.run(debug=True)
