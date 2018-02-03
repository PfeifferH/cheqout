import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("../keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json")
firebase_admin.initialize_app(cred)

# App is an app object of sorts
App = firebase_admin.initialize_app(cred, None, 'Cheqout')
# Client is a firestore client, the docs is https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html
Client = firebase_admin.firestore.client()
