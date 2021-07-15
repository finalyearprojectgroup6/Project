from django.contrib import admin
from .models import user_login,category_master,data_set_master,patient_details,patient_report,doctor_prescription
# Register your models here.
admin.site.register(user_login)
admin.site.register(category_master)
admin.site.register(data_set_master)
admin.site.register(patient_details)
admin.site.register(patient_report)
admin.site.register(doctor_prescription)
