from flask import *
from flask_mongoengine import MongoEngine
import pymongo
import os
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from pymongo import response
from waitress import serve

PYQKEY_FLASK_SEC_KEY    = os.environ["PYQKEY_FLASK_SEC_KEY"]
PYQKEY_KME_ID           = os.environ["PYQKEY_KME_ID"]
PYQKEY_MONGO_COLL       = os.environ["PYQKEY_MONGO_COLL"]
PYQKEY_MONGO_DB         = os.environ["PYQKEY_MONGO_DB"]
PYQKEY_MONGO_DOMAIN     = os.environ["PYQKEY_MONGO_DOMAIN"]
PYQKEY_MONGO_PASSWD     = os.environ["PYQKEY_MONGO_PASSWD"]
PYQKEY_MONGO_PORT       = os.environ["PYQKEY_MONGO_PORT"]
PYQKEY_MONGO_USER       = os.environ["PYQKEY_MONGO_USER"]

pyqkey_app = Flask(__name__, template_folder='templates')

# ==================================================================
#                           MongoDB Setup
# ==================================================================
pyqkey_app.config['MONGODB_SETTINGS'] = {
    'db'  : PYQKEY_MONGO_DB,
    'host': PYQKEY_MONGO_DOMAIN,
    'port': PYQKEY_MONGO_PORT,
}
pyqkey_app.secret_key = PYQKEY_FLASK_SEC_KEY

# db = MongoEngine()
# db.init_app(pyqkey_app)

# class User(UserMixin,db.Document):
#     meta = {"collection":"keys"}
#     key = db.StringField()

myclient = pymongo.MongoClient(
    "mongodb://{}:27017/".format(PYQKEY_MONGO_DOMAIN), 
    username = PYQKEY_MONGO_USER,
    password = PYQKEY_MONGO_PASSWD
    )

mydb = myclient[PYQKEY_MONGO_DB]
mycoll = mydb[PYQKEY_MONGO_COLL]
# ==================================================================

@pyqkey_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(pyqkey_app.root_path, 'static/img'),'prl.png')

@pyqkey_app.route('/', methods=['GET',"POST"])
def home():
   return render_template("index.html")

@pyqkey_app.route('/api/v1/keys/<slave_SAE_ID>/status', methods=['GET'])
def get_status(slave_SAE_ID):
    response_data = {
        "source_KME_ID": PYQKEY_KME_ID,
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

# @pyqkey_app.route('/api/v1/keys/<slave_SAE_ID>/enc_keys', methods=['POST', 'GET'])
# def get_key(slave_SAE_ID):
#     response_data = {
#     }

#     return jsonify(response_data)

@pyqkey_app.route('/api/v1/keys/<master_SAE_ID>/dec_keys', methods=['POST'])
def get_key_with_id(master_SAE_ID):    
    key_data = mycoll.find_one()

    if key_data:
        key = {"key_ID": key_data["key_ID"], "key": key_data["key"]}
        response_data = {
            "keys" : key
        }

        mycoll.delete_one({"key_ID": key_data["key_ID"]})

        return jsonify(response_data)
    else:
        return "No Keys Left!"