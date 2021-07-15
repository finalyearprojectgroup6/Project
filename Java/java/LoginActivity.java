package com.sarath.skinlesion;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class LoginActivity extends AppCompatActivity {
    EditText unameET =null,passwdET=null,ipET =null;
    Button okBT,cancelBT,adminBT;
    String uname,passwd,ip;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        unameET = (EditText)findViewById(R.id.unameET);
        passwdET = (EditText)findViewById(R.id.passwdET);

        okBT = (Button)findViewById(R.id.okBT);

        okBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                uname = unameET.getText().toString();
                passwd = passwdET.getText().toString();
                ip = Variables.ip;//ipET.getText().toString();

                if(uname.length()==0 || passwd.length()==0 || ip.length()==0){
                    Toast.makeText(LoginActivity.this, "Please fill login details", Toast.LENGTH_LONG).show();
                    return;
                }
                else{

                    new Thread(){
                        public void run(){
                            try{
                                uname = unameET.getText().toString();
                                passwd = passwdET.getText().toString();
                                Variables.ip = ip;
                                String url = Variables.mobile_login+"?uname="+uname+"&passwd="+passwd;
                                reply = MyWebClient.getDetailsToString(url);
                                loginHandler.sendMessage(loginHandler.obtainMessage());
                            }catch (Exception e){
                                Toast.makeText(LoginActivity.this, "Login Err>>"+Variables.mobile_login+e, Toast.LENGTH_SHORT).show();
                            }


                        }
                    }.start();

                }



              if(uname.equals(Variables.uname)&&passwd.equals(Variables.passwd)){
                    Variables.storeValues(getApplicationContext(),true,uname,passwd,"1");
                    Intent in = new Intent(LoginActivity.this,MainActivity.class);
                    startActivity(in);
                    finish();
                }
                else{
                    Toast.makeText(LoginActivity.this, "", Toast.LENGTH_SHORT).show();
                    unameET.setText("");
                    passwdET.setText("");
                }


            }
        });

        cancelBT = (Button)findViewById(R.id.cancelBT);

        cancelBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        adminBT = (Button)findViewById(R.id.regBT);

        adminBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent in = new Intent(LoginActivity.this,Register2Activity.class);
                startActivity(in);
                finish();
            }
        });



    }
    String reply="";
    Handler loginHandler = new Handler(){
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            //Toast.makeText(LoginActivity.this, reply, Toast.LENGTH_SHORT).show();
            handleLogin(reply.trim());
        }
    };
    public void handleLogin(String msg){

        String ss[]= msg.split(",");
        if(ss.length==2) {
            if (ss[0].equals("success")) {
                //Variables.uname = unameET.getText().toString();
                Variables.user_id = ss[1];
                Variables.storeValues(getApplicationContext(),true,uname,passwd,Variables.user_id);
                Toast.makeText(this, "Login Success .", Toast.LENGTH_LONG).show();

                Intent in = new Intent(LoginActivity.this,MainActivity.class);
                startActivity(in);

                finish();


            } else if (ss[0].equals("failure")) {
                Toast.makeText(this, "Sorry Invalid Credentials", Toast.LENGTH_SHORT).show();
                unameET.setText(null);
                passwdET.setText(null);
            }
        }
        else{
            Toast.makeText(this, msg, Toast.LENGTH_SHORT).show();
            unameET.setText(null);
            passwdET.setText(null);

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
                                                            }
                        }
                ).show();


    }
}
