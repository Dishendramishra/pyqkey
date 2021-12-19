from flask import *
from flask_mongoengine import MongoEngine
import pymongo
import os
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from pymongo import response
from waitress import serve
import random
import uuid
import hashlib
import base64

PYQKEY_FLASK_SEC_KEY    = os.environ["PYQKEY_FLASK_SEC_KEY"]
PYQKEY_KME_ID           = os.environ["PYQKEY_KME_ID"]
PYQKEY_MONGO_COLL       = os.environ["PYQKEY_MONGO_COLL"]
PYQKEY_MONGO_DB         = os.environ["PYQKEY_MONGO_DB"]
PYQKEY_MONGO_DOMAIN     = os.environ["PYQKEY_MONGO_DOMAIN"]
PYQKEY_MONGO_PASSWD     = os.environ["PYQKEY_MONGO_PASSWD"]
PYQKEY_MONGO_PORT       = os.environ["PYQKEY_MONGO_PORT"]
PYQKEY_MONGO_USER       = os.environ["PYQKEY_MONGO_USER"]

pyqkey_app = Flask(__name__, template_folder='templates')


MAX_KEY_PER_REQUEST = 1     # Maximum number of keys per request
MAX_KEY_SIZE        = 160   # Maximum size of key the KME can deliver to the SAE (in bit)
MIN_KEY_SIZE        = 160   # Minimum size of key the KME can deliver to the SAE (in bit)
KEY_SIZE            = 160   # Default size of key the KME can deliver to the SAE (in bit)
MAX_KEY_COUNT       = 100   # Maximum number of stored_key_count

# Dynamic value fetch from DB
STORED_KEY_COUNT    = None  # Number of stored keys KME can deliver to the SAE

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

def add_keys():
    mycoll.delete_many({})
    
    unique_random_numbers = random.sample(range(1,1000),100)
    
    for number in unique_random_numbers:
        result        = hashlib.sha1(str(number).encode())
        hex_digest    = result.hexdigest().encode() 
        base64_digest = base64.b64encode(hex_digest)

        mycoll.insert_one({"key_ID": str(uuid.uuid4()), "key": base64_digest.decode()})

@pyqkey_app.route('/add_dummpy_keys')
def add_dummpy_keys():
    add_keys()
    return "Keys Added!", 200

@pyqkey_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(pyqkey_app.root_path, 'static/img'),'prl.png')

@pyqkey_app.route('/', methods=['GET',"POST"])
def home():
   return render_template("index.html")

@pyqkey_app.route('/api/v1/keys/<slave_SAE_ID>/status', methods=['GET'])
def get_status(slave_SAE_ID):
    
    key_data = mycoll.find({})

    if key_data:
        STORED_KEY_COUNT = len(list(key_data))
    else:
        STORED_KEY_COUNT = 0
    
    response_data = {
        "source_KME_ID"         : PYQKEY_KME_ID,
        # "target_KME_ID"       : "EEEEFFFFGGGGHHHH",
        "master_SAE_ID"         : slave_SAE_ID,
        # "slave_SAE_ID"        : slave_SAE_ID,
        "key_size"              : KEY_SIZE,
        "stored_key_count"      : STORED_KEY_COUNT,
        "max_key_count"         : MAX_KEY_COUNT,
        "max_key_per_request"   : MAX_KEY_PER_REQUEST,
        "max_key_size"          : MAX_KEY_SIZE,
        "min_key_size"          : MIN_KEY_SIZE,
        "max_SAE_ID_count"      : 0
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
        
        keys = {"keys" : []}
        key = {"key_ID": key_data["key_ID"], "key": key_data["key"]}
        
        keys["keys"].append(key)

        mycoll.delete_one({"key_ID": key_data["key_ID"]})

        return jsonify(keys)
    else:
        add_keys()
        key_data = mycoll.find_one()

        key = {"key_ID": key_data["key_ID"], "key": key_data["key"]}
        response_data = {
            "keys" : key
        }

        mycoll.delete_one({"key_ID": key_data["key_ID"]})

        return jsonify(response_data)


if __name__ == "__main__":
    pyqkey_app.run( 
        host='0.0.0.0', 
        port=443,
        debug= True,
        ssl_context=('cert.pem', 'key.pem'))
    # serve(pyqkey_app, host='0.0.0.0', port=8080, url_scheme='https')
