package com.sarath.skinlesion;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.webkit.WebView;

public class TestHistoryActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test_history);

        WebView mywebview = (WebView) findViewById(R.id.webView);
        mywebview.loadUrl(Variables.mobile_patient_test_master_view+"?user_id="+Variables.user_id);
    }
}