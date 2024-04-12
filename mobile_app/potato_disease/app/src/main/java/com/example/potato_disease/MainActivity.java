package com.example.potato_disease;

import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import org.jetbrains.annotations.NotNull;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    private static final int PICK_IMAGE_REQUEST = 1;
    private Spinner plantSpinner;
    private ImageView imageView;
    private Button selectImageButton;
    private String selectedPlant;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        plantSpinner = findViewById(R.id.plantSpinner);
        imageView = findViewById(R.id.imageView);
        selectImageButton = findViewById(R.id.selectImageButton);

        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.plant_types, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        plantSpinner.setAdapter(adapter);

        plantSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                selectedPlant = parent.getItemAtPosition(position).toString();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });

        selectImageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openFileChooser();
            }
        });
    }

    private void openFileChooser() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Choose Image Source");
        builder.setItems(new CharSequence[]{"Gallery", "Camera"}, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                switch (which) {
                    case 0:
                        Intent galleryIntent = new Intent(Intent.ACTION_GET_CONTENT);
                        galleryIntent.setType("image/*");
                        startActivityForResult(galleryIntent, PICK_IMAGE_REQUEST);
                        break;
                    case 1:
                        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                        if (cameraIntent.resolveActivity(getPackageManager()) != null) {
                            startActivityForResult(cameraIntent, PICK_IMAGE_REQUEST);
                        } else {
                            Toast.makeText(MainActivity.this, "No camera app found", Toast.LENGTH_SHORT).show();
                        }
                        break;
                }
            }
        });
        builder.show();
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (resultCode == RESULT_OK) {
            if (requestCode == PICK_IMAGE_REQUEST && data != null && data.getData() != null) {
                Uri imageUri = data.getData();

                try {
                    Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), imageUri);
                    imageView.setImageBitmap(bitmap);
                    processAndSendImage(bitmap);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            } else if (requestCode == PICK_IMAGE_REQUEST && data != null && data.getExtras() != null && data.getExtras().get("data") != null) {
                Bitmap bitmap = (Bitmap) data.getExtras().get("data");
                imageView.setImageBitmap(bitmap);
                processAndSendImage(bitmap);
            }
        }
    }


    private void processAndSendImage(Bitmap bitmap) {
        // Process the bitmap (resize, convert to suitable format, etc.)
        // For example, let's assume you have a method to convert the bitmap to byte array
        byte[] imageBytes = bitmapToByteArray(bitmap);

        // Now, send the image bytes to the prediction link based on the selected plant
        String predictionLink;
        if ("Potato".equals(selectedPlant)) {
            System.out.println("Potato Plant Selected.");
            predictionLink = "https://us-central1-ordinal-ember-417403.cloudfunctions.net/predict";
        } else if ("Tomato".equals(selectedPlant)) {
            System.out.println("Tomato Plant Selected.");
            predictionLink = "https://us-central1-ethereal-brace-418207.cloudfunctions.net/predict";
        } else {
            Toast.makeText(this, "Invalid plant selection", Toast.LENGTH_SHORT).show();
            return;
        }

        sendImageToPredictionLink(imageBytes, predictionLink);
    }

    private byte[] bitmapToByteArray(Bitmap bitmap) {
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
        return stream.toByteArray();
    }

    private void sendImageToPredictionLink(byte[] imageBytes, String predictionLink) {
        OkHttpClient client = new OkHttpClient();

        RequestBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", "image.jpg",
                        RequestBody.create(MediaType.parse("image/jpeg"), imageBytes))
                .build();

        Request request = new Request.Builder()
                .url(predictionLink)
                .post(requestBody)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(MainActivity.this, "Failed to send image", Toast.LENGTH_SHORT).show();
                    }
                });
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                final String responseData = response.body().string();
                try {
                    JSONObject jsonObject = new JSONObject(responseData);
                    final String predictedClass = jsonObject.getString("class");
                    final double confidence = jsonObject.getDouble("confidence");

                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            displayPredictionResult(predictedClass, confidence);
                        }
                    });
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    private void displayPredictionResult(String predictedClass, double confidence) {
        // Display the predicted class and confidence
        final String predictionText = "Predicted Disease: " + predictedClass + "\nConfidence: " + confidence + "%";
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                TextView predictionTextView = findViewById(R.id.predictionTextView);
                predictionTextView.setText(predictionText);
                predictionTextView.setVisibility(View.VISIBLE);
            }
        });
    }

}
