# Import Fast API, File, UploadFile
from fastapi import FastAPI, File, UploadFile
# Import uvicorn
import uvicorn
# Import numpy 
import numpy as np
from io import BytesIO
# Module to read images
from PIL import Image

# Create an app/ instance of FAST API
app = FastAPI()

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
    return

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)