# Import Fast API, File, UploadFile
from fastapi import FastAPI, File, UploadFile
# Import uvicorn
import uvicorn
# Import numpy 
import numpy as np
from io import BytesIO
# Module to read images
from PIL import Image
# Import Tensorflow
import tensorflow as tf
# Adding middlewares to avoid CORS(Cross Origin Resource Sharing) Error
from fastapi.middleware.cors import CORSMiddleware


# Create an app/ instance of FAST API
app = FastAPI()

# If we upload image, to our website without the code written below, it will give Cross Origin Resource Sharing Error
# as website is running on port 3000 and backend fast api server is running on port 8000
origins = [
    "*"
    #"https://localhost",
    # React.JS UI is running on port 3000
    #"https://localhost:3000",
    
]
# Here we are telling FAST API, add middleware and allow the above origins
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)
# Load the saved tensorflow model
# For now just loading model number 1
MODEL = tf.keras.models.load_model("../saved_models/6/6.h5")
# Class Names need to be consistent with: ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]



# ping method to make sure server is alive.
@app.get("/ping")
async def ping():
    return "Hello, I am alive."

# Function to take bytes as input and return np.ndarray
# Used to get the image in form of numpy array, which can be used for predictions
def read_file_as_image(data) -> np.ndarray:
    # data is basically bytes
    image = np.array(Image.open(BytesIO(data))) # Open/Read those bytes as PIL Image, and then convert PIL Image into numpy array
    return image # numpy array of the image
    

# Predict Method: It is a post routine as here we are not trying to get a record or something, we are doing model prediction and post is appropriate for it
@app.post("/predict")
async def predict(
    # Arguments
    # A file sent by an application or a website, an image of a potato plant leaf
    # FastAPI provides in-build validation, we use upload file as datatype
    # so we use: file: UploadFile = File(...)
    # When we use this, FastAPI makes sure that whovever is calling predict method has to send image/file as the input
    # so if anyone sends int or string as input, it will not work.

    # DataType: UploadFile
    # DefaultValue: File(...)
    # file: In PostMan, select POST method, In Body inside form-data,we add a key named file (We are sending image files using postman)
    file: UploadFile = File(...)
):
    # Convert the received file into numpy array or Tensor so model can make predictions
    # To do that read the file to get the bytes
    # bytes = await file.read() (Next: Convert these bytes to numpy array)
    image = read_file_as_image(await file.read()) # Numpy Array
    
    # predict dosen't accept a single image, it has to be a batch image
    # Meaning: say we have an image: [256, 256, 3]
    # predict cannot accept just [256, 256, 3]
    # So we need to convert this image to a batch, [[256, 256, 3]]
    # Just converting it from 1D to 2D, by this: np.expand_dims(image, 0)
    image_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(image_batch)
    # Since we have only 1 image, so take the 1st prediction: prediction[0]
    # prediction[0]: [0.11, 0.99, 0.25] as we have used softmax function which gives probablities
    # Compare it with: ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
    # now whichever of 3 has maximum value, that is our prediction: Late Blight (Example)
    # so by using argmax we get index 0,1, or 2
    # Pass this index to CLASS_NAMES array, to get  actual class name
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    # Confidence will be 0.99 value in this prediction[0]: [0.11, 0.99, 0.25] array
    confidence = np.max(predictions[0])
    
    # Return predicted_class and confidence as a dictionary
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
    
# COMMAND TO RUN  THIS FILE ON LOCAL HOST: uvicorn main:app --reload