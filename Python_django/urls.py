"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_settings', views.admin_settings, name='admin_settings'),
    path('admin_settings_404', views.admin_settings_404, name='admin_settings_404'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),

    path('admin_category_master_add', views.admin_category_master_add, name='admin_category_master_add'),
    path('admin_category_master_view', views.admin_category_master_view, name='admin_category_master_view'),
    path('admin_category_master_delete', views.admin_category_master_delete, name='admin_category_master_delete'),

    path('admin_data_set_master_add', views.admin_data_set_master_add, name='admin_data_set_master_add'),
    path('admin_data_set_master_view', views.admin_data_set_master_view, name='admin_data_set_master_view'),
    path('admin_data_set_master_delete', views.admin_data_set_master_delete, name='admin_data_set_master_delete'),

    path('admin_staff_user_add', views.admin_staff_user_add, name='admin_staff_user_add'),
    path('admin_staff_user_view', views.admin_staff_user_view, name='admin_staff_user_view'),
    path('admin_staff_user_delete', views.admin_staff_user_delete, name='admin_staff_user_delete'),

    path('admin_user_view', views.admin_user_view, name='admin_user_view'),
    path('admin_user_delete', views.admin_user_delete, name='admin_user_delete'),

    path('admin_doctor_view', views.admin_doctor_view, name='admin_doctor_view'),
    path('admin_doctor_delete', views.admin_doctor_delete, name='admin_doctor_delete'),

    path('staff_login', views.staff_login, name='staff_login'),
    path('staff_logout', views.staff_logout, name='staff_logout'),
    path('staff_home', views.staff_home, name='staff_home'),
    path('staff_settings', views.staff_settings, name='staff_settings'),
    path('staff_changepassword', views.staff_changepassword, name='staff_changepassword'),
    path('staff_patient_test_master_add', views.staff_patient_test_master_add, name='staff_patient_test_master_add'),
    path('staff_patient_test_master_view', views.staff_patient_test_master_view, name='staff_patient_test_master_view'),
    path('staff_patient_search', views.staff_patient_search, name='staff_patient_search'),

    path('user_login', views.user_login_check, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_details_add',views.user_details_add,name='user_details_add'),
    path('user_home', views.user_home, name='user_home'),
    path('user_settings', views.user_settings, name='user_settings'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

    path('patient_patient_test_master_view', views.patient_patient_test_master_view, name='patient_patient_test_master_view'),
    path('user_patient_test_master_add', views.user_patient_test_master_add, name='user_patient_test_master_add'),

    path('user_doctor_query_view', views.user_doctor_query_view, name='user_doctor_query_view'),
    path('user_doctor_query_delete', views.user_doctor_query_delete, name='user_doctor_query_delete'),
    path('user_doctor_query_add', views.user_doctor_query_add, name='user_doctor_query_add'),

    path('doctor_login', views.doctor_login, name='doctor_login'),
    path('doctor_changepassword', views.doctor_changepassword, name='doctor_changepassword'),
    path('doctor_logout', views.doctor_logout, name='doctor_logout'),
    path('doctor_home', views.doctor_home, name='doctor_home'),
    path('doctor_details_add', views.doctor_details_add, name='doctor_details_add'),

    path('doctor_symptom_master_add', views.doctor_symptom_master_add, name='doctor_symptom_master_add'),
    path('doctor_symptom_master_edit', views.doctor_symptom_master_edit, name='doctor_symptom_master_edit'),
    path('doctor_symptom_master_view', views.doctor_symptom_master_view, name='doctor_symptom_master_view'),
    path('doctor_symptom_master_delete', views.doctor_symptom_master_delete, name='doctor_symptom_master_delete'),

    path('doctor_disease_master_add', views.doctor_disease_master_add, name='doctor_disease_master_add'),
    path('doctor_disease_master_edit', views.doctor_disease_master_edit, name='doctor_disease_master_edit'),
    path('doctor_disease_master_view', views.doctor_disease_master_view, name='doctor_disease_master_view'),
    path('doctor_disease_master_delete', views.doctor_disease_master_delete, name='doctor_disease_master_delete'),

    path('doctor_drug_master_add', views.doctor_drug_master_add, name='doctor_drug_master_add'),
    path('doctor_drug_master_edit', views.doctor_drug_master_edit, name='doctor_drug_master_edit'),
    path('doctor_drug_master_view', views.doctor_drug_master_view, name='doctor_drug_master_view'),
    path('doctor_drug_master_delete', views.doctor_drug_master_delete, name='doctor_drug_master_delete'),

    path('doctor_disease_drug_map_view', views.doctor_disease_drug_map_view, name='doctor_disease_drug_map_view'),
    path('doctor_disease_drug_view', views.doctor_disease_drug_view, name='doctor_disease_drug_view'),
    path('doctor_disease_drug_map_delete', views.doctor_disease_drug_map_delete, name='doctor_disease_drug_map_delete'),
    path('doctor_disease_drug_add', views.doctor_disease_drug_add, name='doctor_disease_drug_add'),

    path('doctor_disease_symptom_map_view', views.doctor_disease_symptom_map_view, name='doctor_disease_symptom_map_view'),
    path('doctor_disease_symptom_view', views.doctor_disease_symptom_view, name='doctor_disease_symptom_view'),
    path('doctor_disease_symptom_map_delete', views.doctor_disease_symptom_map_delete, name='doctor_disease_symptom_map_delete'),
    path('doctor_disease_symptom_add', views.doctor_disease_symptom_add, name='doctor_disease_symptom_add'),

    path('doctor_doctor_query_view', views.doctor_doctor_query_view, name='doctor_doctor_query_view'),
    path('doctor_doctor_query_update', views.doctor_doctor_query_update, name='doctor_doctor_query_update'),
    path('doctor_doctor_query_search',views.doctor_doctor_query_search,name='doctor_doctor_query_search'),
    path('doctor_doctor_query_search2',views.doctor_doctor_query_search2,name='doctor_doctor_query_search2'),

    path('doctor_user_view', views.doctor_user_view, name='doctor_user_view'),
    path('doctor_doctor_view', views.doctor_doctor_view, name='doctor_doctor_view'),
    path('doctor_patient_test_master_view', views.doctor_patient_test_master_view, name='doctor_patient_test_master_view'),

    path('mobile_details_direct_add', views.mobile_details_direct_add, name='mobile_details_direct_add'),
    path('mobile_details_add', views.mobile_details_add, name='mobile_details_add'),
    path('mobile_login', views.mobile_login_check, name='mobile_login'),

    path('mobile_patient_test_master_view', views.mobile_patient_test_master_view,name='mobile_patient_test_master_view'),
    path('mobile_patient_test_master_add', views.mobile_patient_test_master_add, name='mobile_patient_test_master_add'),

    path('mobile_doctor_query_view', views.mobile_doctor_query_view, name='mobile_doctor_query_view'),
    path('mobile_doctor_query_add', views.mobile_doctor_query_add, name='mobile_doctor_query_add'),
    path('mobile_doctor_query_details_view', views.mobile_doctor_query_details_view, name='mobile_doctor_query_details_view'),
    path('mobile_changepassword', views.mobile_changepassword, name='mobile_changepassword'),

]
