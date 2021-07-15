from django.db import models

# Create your models here.
class user_login(models.Model):
    uname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    utype = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.uname}-{self.id}"


class patient_details(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    pno = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    addr = models.CharField(max_length=500)
    pincode = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    conatct = models.CharField(max_length=50)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.fname

class patient_report(models.Model):
    patient_id = models.IntegerField()
    file_path = models.CharField(max_length=500)
    result = models.CharField(max_length=150)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)



class category_master(models.Model):
    category_name = models.CharField(max_length=150)

    def __str__(self):
        return self.category_name

class data_set_master(models.Model):
    category_id = models.IntegerField()
    pic_path = models.CharField(max_length=500)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.pic_path


class doctor_master(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    d_descp = models.CharField(max_length=500)
    d_qualification = models.CharField(max_length=500)
    d_category = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.fname

class symptom_master(models.Model):
    symptom_name = models.CharField(max_length=350)

    def __str__(self):
        return self.symptom_name

class disease_master(models.Model):
    disease_name = models.CharField(max_length=200)
    disease_descp = models.CharField(max_length=1500)

    def __str__(self):
        return self.disease_name

class disease_symptom_map(models.Model):
    disease_id = models.IntegerField()
    symptom_id = models.IntegerField()

class disease_drug_map(models.Model):
    disease_id = models.IntegerField()
    drug_id = models.IntegerField()

class disease_treatment(models.Model):
    disease_id = models.IntegerField()
    treatment_plan = models.CharField(max_length=1500)

class drug_master(models.Model):
    drug_name = models.CharField(max_length=150)
    drug_details = models.CharField(max_length=500)
    company_details = models.CharField(max_length=500)
    dosage_details = models.CharField(max_length=500)

    def __str__(self):
        return self.drug_name

class doctor_prescription(models.Model):
    doctor_id = models.IntegerField()
    user_id = models.IntegerField()
    prescription = models.CharField(max_length=1500)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

class user_doctor_query(models.Model):
    user_id = models.IntegerField()
    doctor_id = models.IntegerField()
    query = models.CharField(max_length=1500)
    reply = models.CharField(max_length=1500)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    r_dt = models.CharField(max_length=50)
    r_tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)


