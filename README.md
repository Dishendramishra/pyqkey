### :dart: Aim

This project aims to develop a key delivery system for QKD(Quantum key distribution) system using HTTPS REST API as per ETSI standard.

#### Python Dependencies

```shell
pip install -r python_server/requirements.txt
```



## Generating SSL Certificate

```shell
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

