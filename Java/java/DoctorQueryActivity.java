package com.sarath.skinlesion;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class DoctorQueryActivity extends AppCompatActivity {
    private WebView webView = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_doctor_query);
        webView = (WebView) findViewById(R.id.webView);
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        DoctorQueryActivity.WebViewClientImpl webViewClient = new DoctorQueryActivity.WebViewClientImpl(this);
        webView.setWebViewClient(webViewClient);
        webView.loadUrl(Variables.mobile_doctor_query_add+"?user_id="+Variables.user_id);
    }
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if ((keyCode == KeyEvent.KEYCODE_BACK) && this.webView.canGoBack()) {
            this.webView.goBack();
            return true;
        }

        return super.onKeyDown(keyCode, event);
    }

    public class WebViewClientImpl extends WebViewClient {

        private Activity activity = null;

        public WebViewClientImpl(Activity activity) {
            this.activity = activity;
        }
        public boolean shouldOverrideUrlLoading(WebView webView, String url) {
            return false;
        }
        /*
        @Override
        public boolean shouldOverrideUrlLoading(WebView webView, String url) {
            //if(url.indexOf(Variables.site_url) > -1 ) return false;

            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
            activity.startActivity(intent);
            return true;
        }*/

    }
}
