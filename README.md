# Potato_Disease_Classification
This project aims to provide a user-friendly **Web Interface + Android Application** for classifying diseases in plant leaves using machine learning techniques. It leverages a deep learning model trained on a dataset of plant leaf images to predict the presence of diseases such as Early Blight, Late Blight, or Healthy leaves, etc.
# Website Features
1: **Image Upload**: Users can upload images of plant leaves through a drag-and-drop interface.


2: **Real-time Processing**: The uploaded image is processed in real-time to generate predictions about the presence of diseases.


3: **Prediction Display**: Predicted disease label and confidence score are displayed to the user.


4: **Clear Functionality**: Users can clear the uploaded image and prediction results with a single click


5: **Responsive Design**: The web interface is designed to be responsive and compatible with various devices and screen sizes.


# Technologies Used - Website
1: **Frontend**: React.js, Material-UI 


2: **Backend**: FastAPI (Python) 


3: **Machine Learning**: TensorFlow (Keras) 


# Website Screenshots
# Welcome Page
![frontend_1](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/933c9598-7b02-43ff-986a-47312eed69c2)
# Uploading an Image - Actual Early Blight Leaf Image
![frontend_3](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/54ab4eda-10be-45fb-bdcf-34b105995b38)
# Prediction - Early Blight
![frontend_4](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/e92fda64-46d4-4c92-b82e-8f7014e15f85)
# Uploading an Image - Actual Healthy Leaf Image
![frontend_5](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/3657e78e-d1ba-473a-9296-c8493a198541)
# Prediction - Healthy
![frontend_6](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/1182a46d-d558-4e51-b0f0-c19ffd260b90)
# Uploading an Image - Actual Late Blight Leaf Image
![frontend_7](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/5114f817-0ea3-4e23-b156-78e969b03669)
# Prediction - Late Blight
![fronend_8](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/4b328f1d-324a-4be5-9a79-3913bb485eef)

# Android App Features
1: **Image Upload**: Users can upload images of potato plant leaves from their device's gallery.


2: **Real-Time Processing**: The uploaded image is processed in real-time to generate predictions about the presence of diseases.


3: **Prediction Display**: Predicted disease label and confidence score are displayed below the upload button.


4: **Clear Functionality**: Users can clear the uploaded image and prediction results with a single click.


5: **Responsive Design**: The app interface is designed to be responsive and compatible with various devices and screen sizes.


# Technologies Used - Android App
- **Development Language**: Java

  
- **IDE**: Android Studio


- **Libraries**:

  
  - OkHttp: For making network requests to the prediction link.
 

  - Gson: For parsing JSON responses from the prediction link.



- **APIs**:


  - MediaStore: For accessing and retrieving images from the device's storage.
 


- **UI Components**:


  - ImageView: For displaying images selected by the user.
 

  - Button: For user interaction to select images.

 
- **Other Components**:

  
  - Uri: For handling image URIs.
 
    
  - BitmapFactory: For decoding image files into Bitmaps.
 
    
  - ByteArrayOutputStream: For converting Bitmaps to byte arrays.
 
    
  - RequestBody: For creating HTTP request bodies.
 
    
  - OkHttpClient: For making HTTP requests and handling responses asynchronously.
 
    
  - Request: For building HTTP requests.
 
    
- **Concurrency**:

  
  - Callback: For handling asynchronous responses from HTTP requests and updating the UI accordingly.

# Prediction Link
The app sends images to a prediction link hosted on Google Cloud Platform (GCP) for processing. The prediction link for Potato Plant is [https://us-central1-ordinal-ember-417403.cloudfunctions.net/predict](https://us-central1-ordinal-ember-417403.cloudfunctions.net/predict). And similarly we have links for other plant models.

# Android App Screenshots
# Homepage
![image](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/3c50213c-efb3-46bd-bc3e-7f51dfde5dfc)
# Select Plant To Detect Disease For
![image](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/4af552fd-2e9a-4e89-97f1-ce5581d87f43)
# Select Source of Image
![image](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/2b618a3a-aed9-4f41-ac4a-a17dd282ff99)
# Prediction - Early Blight
![image](https://github.com/BhavyaPatel305/Potato_Disease_Classification/assets/93842768/008c58bc-2972-41d1-ab36-e62d9c1d0ab7)



