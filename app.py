from flask import Flask
from flask_cors import CORS
from createuser import createuser_bp
from signIn import login_bp
from searchRoutes import busRoutes_bp
from rfidtap import rfid_bp



# from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hello'
CORS(app)


app.register_blueprint(createuser_bp)
app.register_blueprint(login_bp)
app.register_blueprint(busRoutes_bp)
app.register_blueprint(rfid_bp)




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
