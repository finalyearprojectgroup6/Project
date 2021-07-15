package com.sarath.skinlesion;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;



import android.Manifest;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import java.util.ArrayList;
public class MainActivity extends AppCompatActivity {

    LinearLayout linearLayout;
    ArrayList<String> menuList =new ArrayList<>();
    final String[] menuLabels= new String[]{"Test Skin","Test History","Ask Doctor ?","Doctor Updates","Change Password","Logout"};
    static final int TESTSKIN_OPTION = 1;
    static final int TESTHISTORY_OPTION = 2;
    static final int ASKDOCTOR_OPTION = 3;
    static final int DOCTORUPDATES_OPTION = 4;
    static final int CHANGEPASSWORD_OPTION = 5;
    static final int LOGOUT_OPTION = 6;
   // TextView profileBT,exitBT,settingsBT,historyBT,askBT;
  //  Button doctorBT;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Variables.isLoggedIn=(Boolean)Variables.getValues(getApplicationContext()).get(0);
        if(!Variables.isLoggedIn){
            Intent in = new Intent(MainActivity.this,LoginActivity.class);
            startActivity(in);
            finish();
        }
        else{
            checkStoragePermission();
            Variables.uname=(String)Variables.getValues(getApplicationContext()).get(1);
            Variables.passwd=(String)Variables.getValues(getApplicationContext()).get(2);
            Variables.user_id=(String)Variables.getValues(getApplicationContext()).get(3);
            //Variables.ip=(String)Variables.getValues(getApplicationContext()).get(4);
            //messageDialog("User>"+Variables.uname+"\nPassword>"+Variables.passwd+"\nId>"+Variables.user_id);
        }
        linearLayout=(LinearLayout)findViewById(R.id.ll);
        menuList =new ArrayList<>();
        int[] imgPool =new int[]{R.drawable.c,R.drawable.mr,R.drawable.doc2,
                R.drawable.dr,R.drawable.changepassword,R.drawable.logout};

        for (int i=0;i<menuLabels.length;i++) {
            CardView cardView = (CardView) LayoutInflater.from(getApplicationContext()).inflate(R.layout.chapters_view, null, true);
            cardView.setUseCompatPadding(true);
            cardView.setContentPadding(16, 5, 16, 5);
            cardView.setPreventCornerOverlap(true);
            TextView tv = cardView.findViewById(R.id.titleTXT);
            ImageView img = cardView.findViewById(R.id.img);
            tv.setText(menuLabels[i]);
            img.setImageResource(imgPool[i]);
            menuList.add(menuLabels[i]);
            linearLayout.addView(cardView);
            setSingleEvent(linearLayout);
        }
/*
        askBT = (TextView)findViewById(R.id.askBT);
        askBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent in = new Intent(MainActivity.this,ChaptersActivity.class);
                startActivity(in);
            }
        });
        doctorBT = (Button)findViewById(R.id.doctorBT);
        doctorBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent in = new Intent(MainActivity.this,DoctorQueryHistoryActivity.class);
                startActivity(in);
            }
        });

        profileBT = (TextView)findViewById(R.id.profileBT);
        profileBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //messageDialog("Feature not enabled");
                //Intent in = new Intent(MainActivity.this,ProfileActivity.class);
                //startActivity(in);
                Intent in = new Intent(MainActivity.this,PhotoUploadActivity.class);
                startActivity(in);
            }
        });
        historyBT = (TextView)findViewById(R.id.historyBT);
        historyBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //messageDialog("Feature not enabled");
                //Intent in = new Intent(MainActivity.this,ProfileActivity.class);
                //startActivity(in);
                Intent in = new Intent(MainActivity.this,TestHistoryActivity.class);
                startActivity(in);
            }
        });
        settingsBT = findViewById(R.id.settingsBT);
        settingsBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //messageDialog("Feature not enabled");

                Intent in = new Intent(MainActivity.this,ChangePasswordActivity.class);
                startActivity(in);
            }
        });
        exitBT = (TextView)findViewById(R.id.exitBT);
        exitBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Variables.storeValues(getApplicationContext(),false,"","","","192.168.1.13");
                Intent in = new Intent(MainActivity.this,LoginActivity.class);
                startActivity(in);
                finish();

            }
        });

 */
    }
    private void setSingleEvent(LinearLayout gridLayout) {
        for(int i = 1; i<gridLayout.getChildCount();i++){
            CardView cardView=(CardView)gridLayout.getChildAt(i);
            final int finalI= i;

            cardView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {

                    //Snackbar.make(view, "Clicked at  "+ chapterList.get(finalI), Snackbar.LENGTH_LONG)
                    //        .setAction("Action", null).show();
                   // Toast.makeText(MainActivity.this,"Clicked at index "+ menuLabels[finalI-1],
                    //        Toast.LENGTH_SHORT).show();
                    if(finalI == TESTSKIN_OPTION){
                        Intent in = new Intent(MainActivity.this,PhotoUploadActivity.class);
                        startActivity(in);
                    }
                    else if(finalI == TESTHISTORY_OPTION){
                        Intent in = new Intent(MainActivity.this,TestHistoryActivity.class);
                        startActivity(in);
                    }
                    else if(finalI == ASKDOCTOR_OPTION){
                         Intent in = new Intent(MainActivity.this,DoctorQueryActivity.class);
                         startActivity(in);
                    }
                    else if(finalI == DOCTORUPDATES_OPTION){
                        Intent in = new Intent(MainActivity.this,DoctorQueryHistoryActivity.class);
                        startActivity(in);
                    }
                    else if(finalI == CHANGEPASSWORD_OPTION){
                        Intent in = new Intent(MainActivity.this,ChangePasswordActivity.class);
                        startActivity(in);
                    }
                    else if(finalI == LOGOUT_OPTION){
                        Variables.storeValues(getApplicationContext(),false,"","","");
                        Intent in = new Intent(MainActivity.this,LoginActivity.class);
                        startActivity(in);
                        finish();
                    }

                }
            });
        }
    }

    public void showExit(){
        new AlertDialog.Builder(this)
                .setTitle("Exit")
                .setMessage("Do you wish to exit ? ")
                .setPositiveButton(
                        "Yes",
                        new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dlg, int id) {
                                finish();
                            }
                        }
                )
                .setNegativeButton(
                        "No",
                        new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dlg, int id) {
                                //Toast.makeText(LoginActivity.this, "Feature Not Active", Toast.LENGTH_SHORT).show();

                            }
                        }
                ).show();
    }
    public void messageDialog(final String msg){
        new AlertDialog.Builder(this)
                .setTitle("Information !")
                .setMessage(msg)
                .setNeutralButton(
                        "Close",
                        new DialogInterface.OnClickListener() {
                            public void onClick(
                                    DialogInterface dlg, int id) {
                                //finish();
                            }
                        }
                ).show();


    }
    public void showPermissionLogout(){
        new AlertDialog.Builder(this)
                .setTitle("Permission Error")
                .setMessage("Permission needed. Do you wish to logout ? ")
                .setPositiveButton(
                        "Yes",
                        new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dlg, int id) {

                                Variables.fromLogin = false;
                                Intent in = new Intent(MainActivity.this,LoginActivity.class);
                                startActivity(in);
                                finish();
                            }
                        }
                )
                .setNegativeButton(
                        "No",
                        new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dlg, int id) {
                                //Toast.makeText(LoginActivity.this, "Feature Not Active", Toast.LENGTH_SHORT).show();
                                checkStoragePermission();
                            }
                        }
                ).show();
    }
    ///////////////////////////////////////////////////////////
    ////////////Check Permissions//////////////
    ///////////////////////////////
    public final int WRITE_STORAGE_PERMISSION=101;
    static boolean  WRITE_STORAGE_FLAG =false;



    public void checkStoragePermission(){
        // Here, thisActivity is the current activity
        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED) {

            // Permission is not granted
            // Should we show an explanation?
            if (ActivityCompat.shouldShowRequestPermissionRationale(MainActivity.this,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
                Toast.makeText(this, "Need this permission ", Toast.LENGTH_SHORT).show();
                ActivityCompat.requestPermissions(MainActivity.this,
                        new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},
                        WRITE_STORAGE_PERMISSION);
            } else {
                // No explanation needed; request the permission
                ActivityCompat.requestPermissions(MainActivity.this,
                        new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},
                        WRITE_STORAGE_PERMISSION);

            }
        } else {
            //Toast.makeText(this, "Permission granted", Toast.LENGTH_SHORT).show();
            WRITE_STORAGE_FLAG=true;
            ///createDIR(Variables.PIC_DIR);

        }

    }

    public void onRequestPermissionsResult(int requestCode,String[] permissions, int[] grantResults) {
        switch (requestCode) {

            case WRITE_STORAGE_PERMISSION: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    // permission was granted, yay! Do the
                    // contacts-related task you need to do.
                    Toast.makeText(this, "Storage Permission granted", Toast.LENGTH_SHORT).show();
                    WRITE_STORAGE_FLAG=true;
                    //createDIR(Variables.PIC_DIR);

                } else {
                    // permission denied, boo! Disable the
                    // functionality that depends on this permission.

                    showPermissionLogout();
                    WRITE_STORAGE_FLAG=false;
                }
                return;
            }

        }
    }
    public boolean checkNetwork(){

        ConnectivityManager cm = (ConnectivityManager) getApplicationContext().getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
        boolean status=activeNetwork != null&& activeNetwork.isConnectedOrConnecting();
        //Toast.makeText(this, "Network"+status, Toast.LENGTH_SHORT).show();
        return status;
    }
    ///////////////////////////////

}
