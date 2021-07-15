package com.sarath.skinlesion;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.text.InputType;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.DatePicker;
import android.widget.RadioGroup;
import android.widget.Toast;

import java.util.Calendar;

public class Register2Activity extends AppCompatActivity {

    DatePickerDialog picker;
    EditText fnameET,lnameET,unameET,addrET,contactET,dobET,passwdET,pinET;
    RadioGroup genderRG;
    Button okBT,cancelBT;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register2);
        fnameET=(EditText) findViewById(R.id.fnameET);
        lnameET=(EditText) findViewById(R.id.lnameET);
        unameET=(EditText) findViewById(R.id.unameET);
        addrET=(EditText) findViewById(R.id.addrET);
        contactET=(EditText) findViewById(R.id.contactET);
        passwdET=(EditText) findViewById(R.id.passwdET);
        pinET=(EditText) findViewById(R.id.pinET);
        genderRG=(RadioGroup) findViewById(R.id.genderRG);




        dobET=(EditText) findViewById(R.id.dobET);
        dobET.setInputType(InputType.TYPE_NULL);
        dobET.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final Calendar cldr = Calendar.getInstance();
                int day = cldr.get(Calendar.DAY_OF_MONTH);
                int month = cldr.get(Calendar.MONTH);
                int year = cldr.get(Calendar.YEAR);
                // date picker dialog
                picker = new DatePickerDialog(Register2Activity.this,
                        new DatePickerDialog.OnDateSetListener() {
                            @Override
                            public void onDateSet(DatePicker view, int year, int monthOfYear, int dayOfMonth) {
                                dobET.setText(year+"-"+(monthOfYear + 1)+"-"+dayOfMonth );
                            }
                        }, year, month, day);
                picker.show();
            }
        });
        cancelBT=(Button)findViewById(R.id.cancelBT);
        cancelBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent in = new Intent(Register2Activity.this,LoginActivity.class);
                startActivity(in);
                finish();
            }});
        okBT=(Button)findViewById(R.id.okBT);
        okBT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int checkedId = genderRG.getCheckedRadioButtonId();
                String gender1 = "";
                if (checkedId == R.id.r1) {
                    gender1 = "Male";
                } else if (checkedId == R.id.r2) {
                    gender1 = "Female";
                }
                final String gender = gender1;
                final String fname = fnameET.getText().toString();
                final String lname = lnameET.getText().toString();
                final String dob = dobET.getText().toString();
                //gender = request.POST.get('gender')

                final String addr = addrET.getText().toString();
                final String pincode = pinET.getText().toString();
                final String email = unameET.getText().toString();
                final String contact = contactET.getText().toString();
                final String password = passwdET.getText().toString();

/*
                messageDialog(fname + "\n" +
                        lname + "\n" +
                        dob + "\n" +
                        gender + "\n" +
                        addr + "\n" +
                        pincode + "\n" +
                        email + "\n" +
                        contact + "\n" +
                        password);
*/
                if (fname.length() == 0 || lname.length() == 0 || dob.length() == 0
                        || addr.length() == 0 || pincode.length() == 0
                        || email.length() == 0 || contact.length() == 0
                        || password.length() == 0) {
                    Toast.makeText(Register2Activity.this, "Please fill all details", Toast.LENGTH_LONG).show();
                    return;
                } else {

                    new Thread() {
                        public void run() {
                            try {


                                String url = Variables.mobile_details_direct_add + "?fname=" + fname
                                        + "&lname=" + lname
                                        + "&dob=" + dob
                                        + "&gender=" + gender
                                        + "&addr=" + addr
                                        + "&pincode=" + pincode
                                        + "&email=" + email
                                        + "&contact=" + contact
                                        + "&password=" + password;
                                reply = MyWebClient.getDetailsToString(url);
                                registerHandler.sendMessage(registerHandler.obtainMessage());
                            } catch (Exception e) {
                                Toast.makeText(Register2Activity.this, "Login Err>>" + e, Toast.LENGTH_SHORT).show();
                            }


                        }
                    }.start();

                }
            }

        });
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
    String reply="";
    Handler registerHandler = new Handler(){
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            //Toast.makeText(LoginActivity.this, reply, Toast.LENGTH_SHORT).show();
            handleRegister(reply.trim());
        }
    };
    public void handleRegister(String msg){


        if (msg.trim().equals("success")) {
            Toast.makeText(this, "Registration Success !!!", Toast.LENGTH_SHORT).show();
            Intent in = new Intent(Register2Activity.this,LoginActivity.class);
            startActivity(in);

            finish();
        } else  {
            Toast.makeText(this, "Sorry Registration Error Try Again !!!", Toast.LENGTH_SHORT).show();
        }

    }
}
