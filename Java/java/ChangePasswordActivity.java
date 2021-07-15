package com.sarath.skinlesion;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.KeyEvent;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class ChangePasswordActivity extends AppCompatActivity {
    EditText opasswdET =null,npasswdET=null;
    Button okBT,cancelBT,adminBT;
    String current_password,new_password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_change_password);

        opasswdET = (EditText)findViewById(R.id.opasswdET);
        npasswdET = (EditText)findViewById(R.id.npasswdET);


        okBT = (Button)findViewById(R.id.okBT);

        okBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                current_password = opasswdET.getText().toString();
                new_password = npasswdET.getText().toString();


                if(new_password.length()==0 || current_password.length()==0){
                    Toast.makeText(ChangePasswordActivity.this, "Please fill details", Toast.LENGTH_LONG).show();
                    return;
                }
                else{

                    new Thread(){
                        public void run(){
                            try{
                                current_password = opasswdET.getText().toString();
                                new_password = npasswdET.getText().toString();

                                String url = Variables.mobile_changepassword+"?user_id="+Variables.user_id
                                        +"&new_password="+new_password
                                        +"&current_password="+current_password;
                                reply = MyWebClient.getDetailsToString(url);
                                cpHandler.sendMessage(cpHandler.obtainMessage());
                            }catch (Exception e){
                                Toast.makeText(ChangePasswordActivity.this, "Login Err>>"+Variables.mobile_login+e, Toast.LENGTH_SHORT).show();
                            }


                        }
                    }.start();

                }

                /*

                if(uname.equals(Variables.uname)&&passwd.equals(Variables.passwd)){
                    Variables.storeValues(getApplicationContext(),true,uname,passwd,"1");
                    Intent in = new Intent(LoginActivity.this,MainActivity.class);
                    startActivity(in);
                    finish();
                }
                else{
                    Toast.makeText(LoginActivity.this, "Sorry invalid credentials!", Toast.LENGTH_SHORT).show();
                    unameET.setText("");
                    passwdET.setText("");
                }
                */


            }
        });

        cancelBT = (Button)findViewById(R.id.cancelBT);

        cancelBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });





    }
    String reply="";
    Handler cpHandler = new Handler(){
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            //Toast.makeText(LoginActivity.this, reply, Toast.LENGTH_SHORT).show();
            handleCP(reply.trim());
        }
    };
    public void handleCP(String msg){

            if (msg.trim().equals("success")) {
                Variables.passwd = npasswdET.getText().toString();
                Variables.storeValues(getApplicationContext(),false,"","","");
                Variables.storeValues(getApplicationContext(),true,Variables.uname,Variables.passwd,Variables.user_id);
                //Toast.makeText(this, "Password Updated", Toast.LENGTH_SHORT).show();
                messageDialog("Password Updated");
            } else if (msg.trim().equals("failure")) {
                //Toast.makeText(this, "Sorry Invalid Credentials", Toast.LENGTH_SHORT).show();
                messageDialog("Password Update Failed");
            }

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
}
