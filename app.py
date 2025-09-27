from flask import Flask
from flask_cors import CORS

from routes import register_all_blueprint


app = Flask(__name__)
cors = CORS(app)


register_all_blueprint(app)


if __name__ == "__main__":
    app.run(debug=True)
