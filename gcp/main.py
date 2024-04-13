# Import the necessary libraries
from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np

# Variable to store model
model = None
interpreter = None
input_index = None
output_index = None

# Define the class names for prediction output
class_names = ['Citrus Black spot', 'Citrus Healthy', 'Citrus canker', 'Citrus greening']
# Here you need to put the name of your GCP bucket
BUCKET_NAME = "citrus_disease_classification" 

# blob: binary large object
# source_blob_name: The blob on the bucket
# destination_file_name: download_blob function will be running on a different server in Google Cloud and that server will be downloading model from the bucket(Created on Google Cloud)
# so when it download's it locally on that server in the cloud, destination_file_name is the destination file path where it should be storing
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # Download the model from the bucket
    storage_client = storage.Client()
    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)
    # Get the blob
    blob = bucket.blob(source_blob_name)
    # Download the blob to this destination: destination_file_name
    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

# predict method to predict the class of the image using loaded model
# request: request object containing image data 
def predict(request):
    # model variable is global
    global model
    # This function will be executed multiple times, so execute this method only on the first call
    if model is None:
        # Download the model
        download_blob(
            # Name of the bucket
            BUCKET_NAME,
            # This is in the bucket on cloud
            "models/citrus.h5",
            # Download model locally into the tmp directory of the server
            "/tmp/citrus.h5",
        )
        # Loading the model
        # Load the model with custom object mapping
        model = tf.keras.models.load_model("/tmp/citrus.h5")


    # request has parameter called files and it has a key called file(Similar to Postman)
    # Now whenever an image is uploaded from Postman or mobil app, it will be stored in the image variable
    image = request.files["file"]

    # Uploaded image could be of any size, so re-size it to 256x256 and convert it to numpy array as well
    image = np.array(
        Image.open(image).convert("RGB").resize((256, 256)) # image resizing
    )

    #image = image/255 # normalize the image in 0 to 1 range
    # model.predict expects a batch of images, so we need to add a dimension to the image
    img_array = tf.expand_dims(image, 0)
    # Predict the class of the image
    predictions = model.predict(img_array)

    print("Predictions:",predictions)

    # Get the class name and confidence
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    
    # Next: Deploying the predict function to the cloud

    return {"class": predicted_class, "confidence": confidence}

# To deploy this model on gcp, in gcp shell, using cd, come inside gcp folder and then run this command:
# gcloud functions deploy predict --runtime python38 --trigger-http --memory 1024 --project ordinal-ember-417403
# After that go to Postman and send an image to this URL using POST(For Potato Model):  https://us-central1-ordinal-ember-417403.cloudfunctions.net/predict
# For Tomato Model Command on gcp shell:  gcloud functions deploy predict --runtime python38 --trigger-http --memory 1024 --project ethereal-brace-418207
# Tomato URL:  https://us-central1-ethereal-brace-418207.cloudfunctions.net/predict
# Apple Model Command on gcp shell:  gcloud functions deploy predict --runtime python38 --trigger-http --memory 1024 --project unified-century-420204
# Apple URL:  https://us-central1-unified-century-420204.cloudfunctions.net/predict
# Bell Pepper Model Command on gcp shell:  gcloud functions deploy predict --runtime python38 --trigger-http --memory 1024 --project bell-pepper-disease-420204
# Bell Pepper URL:  https://us-central1-bell-pepper-disease-420204.cloudfunctions.net/predict
# Cherry Model Command on gcp shell:  gcloud functions deploy predict --runtime python38 --trigger-http --memory 1024 --project moonlit-helper-420205
# Cherry URL:  https://us-central1-moonlit-helper-420205.cloudfunctions.net/predict
# Citrus Model Command on gcp shell:  gcloud functions deploy predict --runtime python38 --trigger-http --memory 1024 --project citrus-disease-classification
# Citrus URL:  https://us-central1-citrus-disease-classification.cloudfunctions.net/predict