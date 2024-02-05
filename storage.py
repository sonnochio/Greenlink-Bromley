import firebase_admin
from firebase_admin import credentials, storage, firestore
import streamlit as st


openai_api_key=st.secrets["openai"]


cred = credentials.Certificate(
    {
  "type": "service_account",
  "project_id": "gl-bromley",
  "private_key_id": st.secrets["private_key_id"],
  "private_key":st.secrets["private_key"],
  "client_email": st.secrets["client_email"],
  "client_id":st.secrets["client_id"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": st.secrets["client_x509_cert_url"],
  "universe_domain": "googleapis.com"
}
)


# Function to initialize Firebase app
def initialize_firebase():
    # Check if the app has already been initialized
    if not firebase_admin._apps:
        # Initialize the Firebase app with the service account file
        firebase_admin.initialize_app(cred)
    else:
        # Firebase app is already initialized
        print("Firebase app already initialized.")

# Call the function to ensure Firebase is initialized
initialize_firebase()

db = firestore.client() # For Firestore Database
bucket = storage.bucket() # For Firebase Storage

def upload_image(image_file, destination_path):
    bucket = storage.bucket()
    blob = bucket.blob(destination_path)
    blob.upload_from_file(image_file, content_type='image/jpeg')
    blob.make_public()  # Make the image publicly accessible
    return blob.public_url

def create_data_point(image_url, geolocation, summarization, raw, type, category, time):
    db = firestore.client()
    data_point = {
        'image_url': image_url,
        'geolocation': geolocation,  # This should be a dict with 'lat' and 'long'
        'raw' : raw,
        'summarization':summarization,
        'type': type,
        'category': category,
        'time' : time
    }
    # Add a new document in collection 'data_points'
    db.collection('data_points').add(data_point)
    print("Data point created with image and textual data.")


def save_data_point(image_url, geolocation, summarization, raw, type, category):
    db = firestore.client()
    doc_ref = db.collection(u'data_points').document()  # Creates a new document in the `data_points` collection
    doc_ref.set({
        u'image_url': image_url,
        u'geolocation': geolocation,  # This can be a map with latitude and longitude fields
        u'summarization': summarization,
        u'raw': raw,
        u'type': type,
        u'category': category
    })
    print(f"Data point with ID: {doc_ref.id} has been added.")


