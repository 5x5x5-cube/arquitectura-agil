from app import create_app
from app.routes import api_bp

app = create_app()
app.register_blueprint(api_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
