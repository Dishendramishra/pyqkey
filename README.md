### :dart: Aim

This project aims to develop a key delivery system for QKD(Quantum key distribution) system using HTTPS REST API as per ETSI standard.

# **Follow the steps as below:**



#### 1. Python Dependencies

Run command below in the path containing `app.py` file.

```shell
pip install -r python_server/requirements.txt
```



#### 2. Generating SSL Certificate

Run command below in the path containing `app.py` file.

```shell
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```



**Tutorial:**

![](./python_server/images/cert_creation.gif)



#### 3. Define environment variables

```
PYQKEY_FLASK_SEC_KEY
PYQKEY_KME_ID
PYQKEY_MONGO_COLL
PYQKEY_MONGO_DB
PYQKEY_MONGO_DOMAIN
PYQKEY_MONGO_PASSWD
PYQKEY_MONGO_PORT
PYQKEY_MONGO_USER
```



**Tutorial:**

![](./python_server/images/environ_vars.gif)



#### 4. Launching app

 `cmd `  or  `powershell`as administrator to run the server.

```
python app.py
```



Output will be something like below:

```
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on https://127.0.0.1:443
```

Use the address as shown by the output to access the webpage. for eg.`https://127.0.0.1:443`

---



### MongoDB Download

1. **MongoDB Windows**: https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.19-signed.msi

2. **MongoDB compass** https://downloads.mongodb.com/compass/mongosh-1.8.0-win32-x64.zip

