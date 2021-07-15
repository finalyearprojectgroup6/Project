package com.sarath.skinlesion;

import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

public class MyWebClient {
    public static String getDetailsToString(String serverurl){
        String jData="";
        try {
            String serverURL=serverurl;
            System.out.println("HE"+serverURL);
            URL url = new URL(serverURL);
            URLConnection uc = url.openConnection();
            InputStream in = uc.getInputStream();
            int ch=0;
            while((ch=in.read())!=-1)
                jData+=(char)ch;
            in.close();
        }catch(Exception e){
            System.out.println("Errrrrrrrrrrr>>"+e);
            jData="Errrrrrrrrrrr>>"+serverurl+"\n"+e.getMessage();
        }
        return jData;
    }
}
