from flask import *
from flask_mongoengine import MongoEngine
import pymongo
import os
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin

DOMAIN = "localhost"
KME_ID = "iamoneofakind"
MONGOUSER   = os.environ["MONGOUSER"]
MONGOPASSWD = os.environ["MONGOPASSWD"]

app = Flask(__name__, template_folder='templates')


# ==================================================================
#                           MongoDB Setup
# ==================================================================
app.config['MONGODB_SETTINGS'] = {
    'db'  : 'pyqkey',
    'host': 'localhost', #os.environ["MONGOIP"],
    'port': 27017,
}
app.secret_key = "nothing"

# db = MongoEngine()
# db.init_app(app)

# class User(UserMixin,db.Document):
#     meta = {"collection":"keys"}
#     key = db.StringField()

myclient = pymongo.MongoClient(
    "mongodb://{}:27017/".format(DOMAIN), 
    username = MONGOUSER,
    password = MONGOPASSWD
    )

mydb = myclient["pyqkey"]
mycoll = mydb["keys"]
# ==================================================================

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),'prl.png')

@app.route('/', methods=['GET',"POST"])
def home():
   return render_template("index.html")

@app.route('/api/v1/keys/<slave_SAE_ID>/status', methods=['GET'])
def get_status(slave_SAE_ID):
    response_data = {
        "source_KME_ID": KME_ID,
        "target_KME_ID": "EEEEFFFFGGGGHHHH",
        "master_SAE_ID": "IIIIJJJJKKKKLLLL",
        "slave_SAE_ID": slave_SAE_ID,
        "key_size": 352,
        "stored_key_count": 10,
        "max_key_count": 1000,
        "max_key_per_request": 2,
        "max_key_size": 1024,
        "min_key_size": 64,
        "max_SAE_ID_count": 0
    }

    return jsonify(response_data)

# @app.route('/api/v1/keys/<slave_SAE_ID>/enc_keys', methods=['POST', 'GET'])
# def get_key(slave_SAE_ID):
#     response_data = {
#     }

#     return jsonify(response_data)

# @app.route('/api/v1/keys/<master_SAE_ID>/dec_keys', methods=['POST'])
# def get_key_with_id(master_SAE_ID):
#     response_data = {
#     }

#     return jsonify(response_data)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=443, 
        debug=True,
        ssl_context =("certificate.pem", "key.pem") 
        ) 