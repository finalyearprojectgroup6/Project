package com.sarath.skinlesion;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;


import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class PhotoUploadActivity extends AppCompatActivity {

    private static final int PICK_FILE_REQUEST = 1;
    private static final String TAG = MainActivity.class.getSimpleName();
    public static String selectedFilePath,cacheFilePath;

    private String SERVER_URL = Variables.mobile_patient_test_master_add;//Variables.putphoto;//"https://kitessarath.000webhostapp.com/sitemate/a.php";
    ImageView ivAttachment;
    TextView bUpload;
    TextView tvFileName,tvHeading;
    ProgressDialog dialog;
    Switch cameraSW;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Variables.FROM_CAMERA=false;

        setContentView(R.layout.activity_photo_upload);
        ivAttachment = (ImageView) findViewById(R.id.ivAttachment);
        ivAttachment.setImageResource(R.drawable.g);
        bUpload =  findViewById(R.id.b_upload);
        tvFileName = (TextView) findViewById(R.id.tv_file_name);
        tvFileName.setText("");
        tvHeading=(TextView)findViewById(R.id.tvHeading);
        cameraSW = (Switch)findViewById(R.id.cameraSW);
        cameraSW.setOnCheckedChangeListener(new Switch.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                Variables.FROM_CAMERA=isChecked;
                if(isChecked)
                    ivAttachment.setImageResource(R.drawable.c);
                else
                    ivAttachment.setImageResource(R.drawable.g);
            }
        });

        ivAttachment.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!Variables.FROM_CAMERA){
                    //on attachment icon click
                    showFileChooser();
                }
                else{
                    dispatchTakePictureIntent();
                }
            }
        });
        bUpload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                //on upload button Click
                if(selectedFilePath != null){
                    dialog = ProgressDialog.show(PhotoUploadActivity.this,"","Uploading File...",true);

                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            //creating new thread to handle Http Operations
                            uploadFile(cacheFilePath);
                        }
                    }).start();
                }else{
                    Toast.makeText(PhotoUploadActivity.this,"Please choose a File First",Toast.LENGTH_SHORT).show();
                }


            }
        });
        //tvHeading.setText("Touch the icon. below to upload "+Variables.selected_site+" picture to server");
        //SERVER_URL = Variables.upload_url;
    }
    private void showFileChooser() {
        Intent intent = new Intent();
        //sets the select file to all types of files
        intent.setType("*/*");
        //allows to select data and return it
        intent.setAction(Intent.ACTION_GET_CONTENT);
        //starts new activity to select file and return data
        startActivityForResult(Intent.createChooser(intent,"Choose File to Upload.."),PICK_FILE_REQUEST);
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(resultCode == Activity.RESULT_OK && !Variables.FROM_CAMERA){
            if(requestCode == PICK_FILE_REQUEST){
                if(data == null){
                    //no data present
                    return;
                }


                Uri selectedFileUri = data.getData();

                selectedFilePath = FilePath.getPath(this,selectedFileUri);
                Log.i(TAG,"Selected File Path:" + selectedFilePath);

                if(selectedFilePath != null && !selectedFilePath.equals("")){
                    if(selectedFilePath.endsWith("png")||selectedFilePath.endsWith("jpg")) {
                        cacheFilePath = scaleAndCacheFile(selectedFilePath);
                        //tvFileName.setText(cacheFilePath);
                        Bitmap bmp = BitmapFactory.decodeFile(cacheFilePath);
                        ivAttachment.setImageBitmap(bmp);
                        tvFileName.setText("Ready to upload");//"File selected:"+new File(selectedFilePath).getName());
                    }
                    else{
                        selectedFilePath="";
                        tvFileName.setText("Please select image files");
                    }
                }else{

                    Toast.makeText(this,"Cannot upload file to server"+selectedFilePath,Toast.LENGTH_SHORT).show();
                }
            }
        }
        /////////////////////////

        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK && Variables.FROM_CAMERA) {
            try {


                ivAttachment.setImageURI(mHighQualityImageUri);
                Bitmap imageBitmap=BitmapFactory.decodeFile(cacheFilePath);
                String nn = System.currentTimeMillis() + "_cam.jpg";
                File f2 = new File(this.getExternalCacheDir(), nn);
                FileOutputStream fout = new FileOutputStream(f2);
                imageBitmap.compress(Bitmap.CompressFormat.JPEG, Variables.PIC_SCALE, fout);
                fout.flush();
                fout.close();
                ivAttachment.setImageBitmap(imageBitmap);
                new File(cacheFilePath).delete();

                cacheFilePath=f2.getAbsolutePath();

                //cacheFilePath=mHighQualityImageUri.getPath();
                tvFileName.setText("Ready to upload");
                selectedFilePath=cacheFilePath;
            }catch (Exception e){
                Toast.makeText(this, "CAM ERR>>"+e, Toast.LENGTH_SHORT).show();
            }
        }
        //////////////////////////
    }
    public void createDIR(String path){
        try {
            File testFile = new File(this.getExternalFilesDir(null), path);
            boolean flag=testFile.mkdirs();
            //Toast.makeText(this, testFile.getAbsolutePath()+","+flag, Toast.LENGTH_SHORT).show();

        }catch (Exception e){
            Toast.makeText(this, "createDIR Err>>"+e, Toast.LENGTH_SHORT).show();
        }
    }
    public String scaleAndCacheFile(String inpath){
        String newPath=null;
        try {
            File f1 = new File(inpath);
            String nn = System.currentTimeMillis() + "" + f1.getName();
            File f2 = new File(this.getExternalCacheDir(),  nn);
            FileOutputStream fout = new FileOutputStream(f2);

            Bitmap bitmapImage = BitmapFactory.decodeFile(selectedFilePath);
            bitmapImage.compress(Bitmap.CompressFormat.JPEG, Variables.PIC_SCALE, fout);
            fout.flush();
            fout.close();
            newPath=f2.getAbsolutePath();

        }catch(Exception e){
            Toast.makeText(this, "Err>>"+e, Toast.LENGTH_SHORT).show();
        }
        return newPath;
    }
    public String saveFile(String inpath){
        String newPath=null;
        try {
            File f1 = new File(inpath);
            String nn = f1.getName();
            File f2 = new File(this.getExternalFilesDir(null),  Variables.PIC_DIR+"/"+nn);
            f1.renameTo(f2);
            newPath=f2.getAbsolutePath();

        }catch(Exception e){
            Toast.makeText(this, "Err>>"+e, Toast.LENGTH_SHORT).show();
        }
        return newPath;
    }
    ////////////////////////////////////////
    static final int REQUEST_IMAGE_CAPTURE = 2;
    private Uri mHighQualityImageUri = null;

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            String nn = System.currentTimeMillis() + "_cam.jpg";
            File f2 = new File(this.getExternalCacheDir(), nn);
            cacheFilePath=f2.getAbsolutePath();
            try {

                mHighQualityImageUri = FileProvider.getUriForFile(this,"com.sarath.skinlesion.fileprovider",f2);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, mHighQualityImageUri);
                startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
            }catch (Exception e){
                Toast.makeText(this, "dispatchTakePictureIntent>>"+e, Toast.LENGTH_SHORT).show();
            }
        }
    }



    ////////////////////////////////////////
    public void appendToFile(String fname,String data){
        try {
            File testFile = new File(this.getExternalFilesDir(null), fname);
            FileOutputStream fout=new FileOutputStream(testFile,true);
            fout.write(data.getBytes());
            fout.close();
        }catch (Exception e){

            Toast.makeText(this, "appendToFile Err>>"+e, Toast.LENGTH_SHORT).show();
        }
    }
    ///////////////////////////////////////////////
    //android upload file to server
    String replyMessage="";
    public int uploadFile(final String selectedFilePath){

        int serverResponseCode = 0;

        HttpURLConnection connection;
        DataOutputStream dataOutputStream;
        DataInputStream dataInputStream;
        String lineEnd = "\r\n";
        String twoHyphens = "--";
        String boundary = "*****";


        int bytesRead,bytesAvailable,bufferSize;
        byte[] buffer;
        int maxBufferSize = 1 * 1024 * 1024;
        File selectedFile = new File(selectedFilePath);


        String[] parts = selectedFilePath.split("/");
        final String fileName = parts[parts.length-1];

        if (!selectedFile.isFile()){
            dialog.dismiss();

            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    tvFileName.setText("Source File Doesn't Exist: " + selectedFilePath);
                }
            });
            return 0;
        }else{
            try{
                FileInputStream fileInputStream = new FileInputStream(selectedFile);
                URL url = new URL(SERVER_URL);
                connection = (HttpURLConnection) url.openConnection();
                connection.setDoInput(true);//Allow Inputs
                connection.setDoOutput(true);//Allow Outputs
                connection.setUseCaches(false);//Don't use a cached Copy
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Connection", "Keep-Alive");
                connection.setRequestProperty("ENCTYPE", "multipart/form-data");
                connection.setRequestProperty("Content-Type", "multipart/form-data;boundary=" + boundary);
                connection.setRequestProperty(/*"uploaded_file"*/"imagefile",selectedFilePath);

                //creating new dataoutputstream
                dataOutputStream = new DataOutputStream(connection.getOutputStream());

                //////////Form Data///////////////////////
                dataOutputStream.writeBytes(twoHyphens + boundary + lineEnd);
                dataOutputStream.writeBytes("Content-Disposition: form-data; name=\"id\""+ lineEnd);
                dataOutputStream.writeBytes("Content-Type: text/plain; charset=utf-8"+lineEnd);
                dataOutputStream.writeBytes(lineEnd);
                dataOutputStream.writeBytes(Variables.user_id+lineEnd);
                dataOutputStream.flush();
                /////////////////

                //////////////File Data/////////////////////
                //writing bytes to data outputstream
                dataOutputStream.writeBytes(twoHyphens + boundary + lineEnd);
                dataOutputStream.writeBytes("Content-Disposition: form-data; name=\"imagefile\";filename=\""
                        + selectedFilePath + "\"" + lineEnd);

                dataOutputStream.writeBytes(lineEnd);

                //returns no. of bytes present in fileInputStream
                bytesAvailable = fileInputStream.available();
                //selecting the buffer size as minimum of available bytes or 1 MB
                bufferSize = Math.min(bytesAvailable,maxBufferSize);
                //setting the buffer as byte array of size of bufferSize
                buffer = new byte[bufferSize];

                //reads bytes from FileInputStream(from 0th index of buffer to buffersize)
                bytesRead = fileInputStream.read(buffer,0,bufferSize);

                //loop repeats till bytesRead = -1, i.e., no bytes are left to read
                while (bytesRead > 0){
                    //write the bytes read from inputstream
                    dataOutputStream.write(buffer,0,bufferSize);
                    bytesAvailable = fileInputStream.available();
                    bufferSize = Math.min(bytesAvailable,maxBufferSize);
                    bytesRead = fileInputStream.read(buffer,0,bufferSize);
                }

                dataOutputStream.writeBytes(lineEnd);
                dataOutputStream.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);

                serverResponseCode = connection.getResponseCode();
                String serverResponseMessage = connection.getResponseMessage();

                Log.i(TAG, "Server Response is: " + serverResponseMessage + ": " + serverResponseCode);
                replyMessage = "Server Response is: " + serverResponseMessage + ": " + serverResponseCode;

                //response code of 200 indicates the server status OK
                if(serverResponseCode == 200){
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {

                            createDIR(Variables.PIC_DIR);
                            String newPath= saveFile(cacheFilePath);
                            Toast.makeText(PhotoUploadActivity.this, replyMessage, Toast.LENGTH_SHORT).show();
                            tvFileName.setText("File Upload completed");
                            PhotoUploadActivity.selectedFilePath="";
                            PhotoUploadActivity.cacheFilePath="";

                            if(Variables.FROM_CAMERA)
                                ivAttachment.setImageResource(R.drawable.c);
                            else
                                ivAttachment.setImageResource(R.drawable.g);
                        }
                    });
                }

                //closing the input and output streams
                fileInputStream.close();
                dataOutputStream.flush();
                dataOutputStream.close();



            } catch (FileNotFoundException e) {
                e.printStackTrace();
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(PhotoUploadActivity.this,"File Not Found",Toast.LENGTH_SHORT).show();
                    }
                });
            } catch (MalformedURLException e) {
                e.printStackTrace();
                Toast.makeText(PhotoUploadActivity.this, "URL error!", Toast.LENGTH_SHORT).show();

            } catch (IOException e) {
                e.printStackTrace();
                Toast.makeText(PhotoUploadActivity.this, "Cannot Read/Write File!", Toast.LENGTH_SHORT).show();
            }
            dialog.dismiss();
            return serverResponseCode;
        }

    }

    //////////////////////////////////////////////
}
