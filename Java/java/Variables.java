package com.sarath.skinlesion;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.ArraySet;



import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class Variables {

    public static boolean isLoggedIn=false;
    public static boolean isOffline=false;
    public static boolean isNewSite=false;
    public static boolean fromLogin = false;

    public static String uname="u1@g.com";
    public static String passwd="1234";
    public static String user_id="1";

    public static String ip="192.168.85.28";
    //http://192.168.1.12:8000/myapp/user_login
    public static String site_url = "http://"+ip+":8000/myapp";
    public static String mobile_login = site_url+"/mobile_login";
    public static String mobile_details_add = site_url+"/mobile_details_add";
    public static String mobile_details_direct_add = site_url+"/mobile_details_direct_add";
    public static String mobile_patient_test_master_view = site_url+"/mobile_patient_test_master_view";
    public static String mobile_doctor_query_view = site_url+"/mobile_doctor_query_view";
    public static String mobile_doctor_query_add = site_url+"/mobile_doctor_query_add";
    public static String mobile_changepassword = site_url+"/mobile_changepassword";


    public static String mobile_patient_test_master_add = site_url+"/mobile_patient_test_master_add";

    public static boolean FROM_CAMERA=false;
    public static int PIC_SCALE=100;
    public static String PIC_DIR="PICS";

    public static void storeValues(Context ctx, boolean loggedin, String uname,
                                   String passwd,String user_id){


        SharedPreferences pref = ctx.getSharedPreferences("SKIN", 0); // 0 - for private mode
        SharedPreferences.Editor editor = pref.edit();

        editor.putBoolean("loggedin", loggedin);
        editor.putString("uname", uname);
        editor.putString("passwd", passwd);
        editor.putString("user_id", user_id);
        editor.putString("ip", ip);

        editor.commit();



    }
    public static ArrayList<Object> getValues(Context ctx){

        ArrayList<Object> valList = new ArrayList<>();
        SharedPreferences pref = ctx.getSharedPreferences("SKIN", 0); // 0 - for private mode

        boolean loggedin=pref.getBoolean("loggedin", false);
        String uname=pref.getString("uname", "invalid");
        String passwd=pref.getString("passwd", "invalid");
        String user_id=pref.getString("user_id", "invalid");
        valList.add(loggedin);
        valList.add(uname);
        valList.add(passwd);
        valList.add(user_id);
        return valList;

    }
}
