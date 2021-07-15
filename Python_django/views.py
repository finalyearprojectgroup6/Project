from django.shortcuts import render
from .models import user_login,category_master,data_set_master,patient_details,patient_report
from django.db.models import Max
from django.core.files.storage import FileSystemStorage

from datetime import datetime
import os
# Create your views here.
def index(request):
    return render(request,'./myapp/index.html')

def about(request):
    return render(request,'./myapp/about.html')

def contact(request):
    return render(request,'./myapp/contact.html')

def admin_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, password=passwd)

        if len(ul) == 1:
            request.session['user_id'] = ul[0].uname
            context = {'uname': request.session['user_id']}
            return render(request, 'myapp/admin_home.html',context)
        else:
            context ={'msg':'Login Error'}
            return render(request, 'myapp/admin_login.html',context)
    else:
        return render(request, 'myapp/admin_login.html')

def admin_home(request):
    try:
        uname = request.session['user_id']
        print(uname)
    except:
        return admin_login(request)

    context = {'uname':request.session['user_id']}
    return render(request,'./myapp/admin_home.html',context)

def admin_settings(request):

    context = {'uname':request.session['user_id']}
    return render(request,'./myapp/admin_settings.html',context)

def admin_settings_404(request):

    context = {'uname':request.session['user_id']}
    return render(request,'./myapp/admin_settings_404.html',context)

def admin_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_id']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context ={'msg':"Password Changed Successfully"}
                return render(request, './myapp/admin_changepassword.html',context)
            else:
                context = {'msg': "Password Not Changed"}
                return render(request, './myapp/admin_changepassword.html',context)
        except user_login.DoesNotExist:
            context = {'msg': "Password Not Changed"}
            return render(request, './myapp/admin_changepassword.html',context)
    else:
        return render(request, './myapp/admin_changepassword.html')

def admin_category_master_add(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        cm = category_master(category_name=category_name)
        cm.save()
        return render(request, 'myapp/admin_category_master_add.html')

    else:
        return render(request, 'myapp/admin_category_master_add.html')

def admin_category_master_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    nm = category_master.objects.get(id=int(id))
    nm.delete()

    nm_l = category_master.objects.all()
    context ={'category_list':nm_l}
    return render(request,'myapp/admin_category_master_view.html',context)

def admin_category_master_view(request):
    nm_l = category_master.objects.all()
    context ={'category_list':nm_l}
    return render(request,'myapp/admin_category_master_view.html',context)


def admin_staff_user_add(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        utype = 'staff'

        ul = user_login(uname=uname,password=password,utype=utype)
        ul.save()
        return render(request, 'myapp/admin_staff_user_add.html')

    else:
        return render(request, 'myapp/admin_staff_user_add.html')

def admin_staff_user_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    nm = user_login.objects.get(id=int(id))
    nm.delete()

    nm_l = user_login.objects.filter(utype='staff')
    context ={'staff_list':nm_l}
    return render(request,'myapp/admin_staff_user_view.html',context)

def admin_staff_user_view(request):
    nm_l = user_login.objects.filter(utype='staff')
    context = {'staff_list': nm_l}
    return render(request, 'myapp/admin_staff_user_view.html', context)

def admin_data_set_master_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)
        category_id = int(request.POST.get('category_id'))
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status='ok'
        data_obj = data_set_master(pic_path=pic_path,category_id=category_id,dt=dt,tm=tm,status=status)
        data_obj.save()
        category_list = category_master.objects.all()
        context = {'category_list': category_list }
        return render(request, 'myapp/admin_data_set_master_add.html',context)
    else:
        category_list = category_master.objects.all()
        context = {'category_list': category_list}
        return render(request, 'myapp/admin_data_set_master_add.html',context)


def admin_data_set_master_delete(request):
    id = request.GET.get('id')
    print("id="+id)
    lm = data_set_master.objects.get(id=int(id))
    lm.delete()

    pp_l = data_set_master.objects.all()
    cm_l = category_master.objects.all()
    cmd = {}
    for nm in cm_l:
        cmd[nm.id] = nm.category_name
    context = {'pic_list':pp_l,'category_list':cmd}
    return render(request,'myapp/admin_data_set_master_view.html',context)

def admin_data_set_master_view(request):
    pp_l = data_set_master.objects.all()
    cm_l = category_master.objects.all()
    cmd = {}
    for nm in cm_l:
        cmd[nm.id] = nm.category_name
    context = {'pic_list': pp_l, 'category_list': cmd}
    return render(request, 'myapp/admin_data_set_master_view.html', context)

def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_user_view(request):
    ul_l = user_login.objects.filter(utype='patient')

    tm_l = []
    for u in ul_l:
        ud = patient_details.objects.get(user_id=u.id)
        tm_l.append(ud)

    context = {'user_list':tm_l,'type':'User Details'}
    return render(request, './myapp/admin_user_view.html',context)

def admin_user_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    nm = patient_details.objects.get(id=int(id))
    u_l = user_login.objects.get(id= nm.user_id)
    u_l.delete()
    patient_report.objects.filter(patient_id=nm.user_id).delete()
    doctor_prescription.objects.filter(user_id=nm.user_id).delete()
    user_doctor_query.objects.filter(user_id=nm.user_id).delete()
    nm.delete()

    ul_l = user_login.objects.filter(utype='patient')

    tm_l = []
    for u in ul_l:
        ud = patient_details.objects.get(user_id=u.id)
        tm_l.append(ud)

    context = {'user_list': tm_l, 'type': 'User Details','msg':'User Removed'}
    return render(request, './myapp/admin_user_view.html', context)

def admin_doctor_view(request):
    ul_l = user_login.objects.filter(utype='doctor')

    tm_l = []
    for u in ul_l:
        ud = doctor_master.objects.get(user_id=u.id)
        tm_l.append(ud)

    context = {'user_list':tm_l,'type':'Doctor Details'}
    return render(request, './myapp/admin_doctor_view.html',context)

def admin_doctor_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    nm = doctor_master.objects.get(id=int(id))
    u_l = user_login.objects.get(id= nm.user_id)
    u_l.delete()
    doctor_prescription.objects.filter(doctor_id=nm.user_id).delete()
    user_doctor_query.objects.filter(doctor_id=nm.user_id).delete()
    nm.delete()

    ul_l = user_login.objects.filter(utype='doctor')

    tm_l = []
    for u in ul_l:
        ud = doctor_master.objects.get(user_id=u.id)
        tm_l.append(ud)

    context = {'user_list': tm_l, 'type': 'Doctor Details','msg':'Doctor Removed'}
    return render(request, './myapp/admin_doctor_view.html', context)

######STAFF###########
def staff_login(request):

    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, password=passwd,utype='staff')

        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            return render(request, 'myapp/staff_home.html',
                          context)
        else:
            return render(request, 'myapp/staff_login.html')
    else:
        return render(request, 'myapp/staff_login.html')

def staff_home(request):

    try:
        uname = request.session['user_id']
        print(uname)
    except:
        return staff_login(request)

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/staff_home.html',context)

def staff_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                return render(request, './myapp/staff_settings.html')
            else:
                return render(request, './myapp/staff_settings.html')
        except user_login.DoesNotExist:
            return render(request, './myapp/staff_changepassword.html')
    else:
        return render(request, './myapp/staff_changepassword.html')

def staff_settings(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/staff_settings.html',context)

def staff_patient_test_master_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()

        pic_path = fs.save(randomString(10)+uploaded_file.name, uploaded_file)
        print(pic_path)
        ##########################################################
        file_path = pic_path
        entity_dict = {0: 'benign', 1: 'malignant'}
        filename = f'./myapp/static/myapp/media/{file_path}'
        model = start_predicting_entity(BASE_DIR)
        result = predict_entity(filename, model)
        entity_result = entity_dict[result]
        print(entity_result)
        ####################################################

        #pic_list = data_set_master.objects.all()
        #selfile=''
        #selcat=0

        #print(selfile)
        #print(selcat)
        fname = request.POST.get('fname')
        #selfile = fname
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        pno = request.POST.get('pno')
        addr = request.POST.get('addr')
        pincode = request.POST.get('pincode')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = '1234'
        uname = email
        status = "new"
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        ul = user_login.objects.filter(uname=uname, password=password, utype='patient')
        print(len(ul))
        if len(ul) == 1:
            user_id = ul[0].id
        else:
            ul = user_login(uname=uname, password=password, utype='patient')
            ul.save()
            user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

            ud = patient_details(user_id=user_id, fname=fname, lname=lname, dob=dob,gender=gender, addr=addr, pincode=pincode, conatct=contact,
                          status=status, email=email,pno=pno,dt=dt,tm=tm)
            ud.save()

        cm = category_master.objects.get(id=1)

        result = entity_result#cm.category_name



        utm = patient_report(patient_id=user_id, file_path=pic_path, result=result, dt=dt, tm=tm,
                               status=status)
        utm.save()

        context = {'category_name': entity_result}
        return render(request, 'myapp/staff_patient_test_result.html',context)
    else:
        context = {}

        return render(request, 'myapp/staff_patient_test_master_add.html',context)


def staff_patient_test_master_view(request):
    pp_l = patient_report.objects.all()
    ud_l = patient_details.objects.all()
    cmd = {}
    for nm in ud_l:
        cmd[nm.user_id] = f'{nm.fname} {nm.lname}'
    context = {'test_list': pp_l, 'user_list': cmd}
    return render(request, 'myapp/staff_patient_test_master_view.html', context)

def staff_patient_search(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        ul = user_login.objects.get(uname=email)
        pp_l = patient_report.objects.filter(patient_id=ul.id)
        ud_l = patient_details.objects.all()
        cmd = {}
        for nm in ud_l:
            cmd[nm.user_id] = f'{nm.fname} {nm.lname}'
        context = {'test_list': pp_l, 'user_list': cmd}
        return render(request, 'myapp/staff_patient_test_master_view.html', context)
    else:
        return render(request, 'myapp/staff_patient_search.html')


def staff_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return staff_login(request)
    else:
        return staff_login(request)



###########################################
########USER#############
def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, password=passwd,utype='patient')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            return render(request, 'myapp/user_home.html',context)
        else:
            context={'msg':'Login Error'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return user_login_check(request)

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context = {'msg':'Password changed'}
                return render(request, './myapp/user_settings.html',context)
            else:
                context = {'msg': 'Password change error'}
                return render(request, './myapp/user_settings.html',context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password change error'}
            return render(request, './myapp/user_changepassword.html',context)
    else:
        return render(request, './myapp/user_changepassword.html')

def user_settings(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_settings.html',context)

def patient_patient_test_master_view(request):
    patient_id = int(request.session['user_id'])
    pp_l = patient_report.objects.filter(patient_id=patient_id)
    ud_l = patient_details.objects.all()
    cmd = {}
    for nm in ud_l:
        cmd[nm.user_id] = f'{nm.fname} {nm.lname}'
    context = {'test_list': pp_l, 'user_list': cmd}
    return render(request, 'myapp/patient_patient_test_master_view.html', context)



def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)

def user_details_add(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        pno = request.POST.get('pno')
        addr = request.POST.get('addr')
        pincode = request.POST.get('pincode')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        uname = email
        status = "new"
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        ul = user_login.objects.filter(uname=uname, password=password, utype='patient')
        print(len(ul))
        if len(ul) == 1:
            user_id = ul[0].id
        else:
            ul = user_login(uname=uname, password=password, utype='patient')
            ul.save()
            user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

            ud = patient_details(user_id=user_id, fname=fname, lname=lname, dob=dob,gender=gender, addr=addr, pincode=pincode, conatct=contact,
                          status=status, email=email,pno=pno,dt=dt,tm=tm)
            ud.save()



        context = {'msg': 'user registerted'}
        return render(request, 'myapp/user_login.html',context)
    else:
        context = {}

        return render(request, 'myapp/user_details_add.html',context)

from .Testing_Entity import start_predicting_entity,predict_entity
def user_patient_test_master_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()

        pic_path = fs.save(randomString(10)+uploaded_file.name, uploaded_file)
        print(pic_path)
        ##########################################################
        file_path = pic_path
        entity_dict = {0: 'benign', 1: 'malignant'}
        filename = f'./myapp/static/myapp/media/{file_path}'
        model = start_predicting_entity(BASE_DIR)
        result = predict_entity(filename, model)
        entity_result = entity_dict[result]
        print(entity_result)
        ####################################################
        #pic_list = data_set_master.objects.all()
        #cnt = 0
        #cnt1= 0
        #selfile=''
        #selcat=1

        #print(selfile)
        #print(selcat)
        status = "new"
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')


        #cm = category_master.objects.get(id=int(selcat))

        #staff_user_id = int(request.session['user_id'])
        result = entity_result#cm.category_name


        user_id = request.session['user_id']
        utm = patient_report(patient_id=int(user_id), file_path=pic_path, result=result, dt=dt, tm=tm,
                               status=status)
        utm.save()

        context = {'category_name': result}
        return render(request, 'myapp/user_patient_test_result.html',context)
    else:
        context = {}

        return render(request, 'myapp/user_patient_test_master_add.html',context)



from datetime import datetime
from .models import user_doctor_query
from .models import doctor_prescription

def user_doctor_query_add(request):
    if request.method == 'POST':

        doctor_id = request.POST.get('doctor_id')
        query = request.POST.get('query')

        reply = ' '
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        r_dt = ' '
        r_tm = ' '
        user_id = int(request.session['user_id'])
        prescription = ' '
        status='new'
        udq = user_doctor_query(doctor_id=int(doctor_id),query=query,reply=reply,dt=dt,
                                tm=tm,r_dt=r_dt,r_tm=r_tm,user_id=user_id,status=status )
        udq.save()

        query_id = user_doctor_query.objects.all().aggregate(Max('id'))['id__max']
        dp = doctor_prescription(prescription=prescription,status=str(query_id),doctor_id=doctor_id,user_id=user_id,dt=dt,tm=tm)
        dp.save()

        dm_l = doctor_master.objects.all()
        context = {'msg': 'Record Added','doctor_list':dm_l}
        return render(request, './myapp/user_doctor_query_add.html', context)
    else:
        dm_l = doctor_master.objects.all()
        context = { 'doctor_list': dm_l}
        return render(request, './myapp/user_doctor_query_add.html', context)


def user_doctor_query_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    udq = user_doctor_query.objects.get(id=int(id))
    dp = doctor_prescription.objects.get(status=id)
    dp.delete()
    udq.delete()
    msg = 'Record Deleted'
    user_id = int(request.session['user_id'])
    udq_l = user_doctor_query.objects.filter(user_id=user_id)
    dp_l = doctor_prescription.objects.all()
    dpl = {}
    for dp in dp_l:
        dpl[int(dp.status)] = dp.prescription
    dm_l = doctor_master.objects.all()
    context = {'query_list': udq_l,'doctor_list': dm_l,'prescription_list': dpl,'msg':msg}
    return render(request, './myapp/user_doctor_query_view.html',context)

def user_doctor_query_view(request):
    user_id = int(request.session['user_id'])
    udq_l = user_doctor_query.objects.filter(user_id=user_id)
    dp_l = doctor_prescription.objects.filter(user_id=user_id)
    dm_l = doctor_master.objects.all()
    dpl = {}
    for dp in dp_l:
        dpl[int(dp.status)] = dp.prescription

    context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
    return render(request, './myapp/user_doctor_query_view.html', context)

########################################################
##################MOBILE PART ###########################
from django.http import HttpResponse
def mobile_details_add(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        pno = '0000'#request.POST.get('pno')
        addr = request.POST.get('addr')
        pincode = request.POST.get('pincode')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        uname = email
        status = "new"
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        ul = user_login.objects.filter(uname=uname, password=password, utype='patient')
        print(len(ul))
        if len(ul) == 1:
            user_id = ul[0].id
        else:
            ul = user_login(uname=uname, password=password, utype='patient')
            ul.save()
            user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

            ud = patient_details(user_id=user_id, fname=fname, lname=lname, dob=dob,gender=gender, addr=addr, pincode=pincode, conatct=contact,
                          status=status, email=email,pno=pno,dt=dt,tm=tm)
            ud.save()



        context = {'msg': 'user registerted'}
        return render(request, 'myapp/mobile_details_add.html',context)
    else:
        context = {}

        return render(request, 'myapp/mobile_details_add.html',context)

def mobile_details_direct_add(request):
    fname = request.GET.get('fname')
    lname = request.GET.get('lname')
    dob = request.GET.get('dob')
    gender = request.GET.get('gender')
    pno = '0000'#request.POST.get('pno')
    addr = request.GET.get('addr')
    pincode = request.GET.get('pincode')
    email = request.GET.get('email')
    contact = request.GET.get('contact')
    password = request.GET.get('password')
    uname = email
    status = "new"
    dt = datetime.today().strftime('%Y-%m-%d')
    tm = datetime.today().strftime('%H:%M:%S')

    ul = user_login.objects.filter(uname=uname, password=password, utype='patient')
    print(len(ul))
    if len(ul) == 1:
        user_id = ul[0].id
    else:
        ul = user_login(uname=uname, password=password, utype='patient')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']
        ud = patient_details(user_id=user_id, fname=fname, lname=lname, dob=dob,gender=gender, addr=addr, pincode=pincode, conatct=contact,
            status=status, email=email,pno=pno,dt=dt,tm=tm)
        ud.save()
    msg = 'success'
    return HttpResponse(msg)

def mobile_login_check(request):
    uname = request.GET.get('uname')
    passwd = request.GET.get('passwd')
    ul = user_login.objects.filter(uname=uname, password=passwd,utype='patient')
    print(len(ul))
    if len(ul) == 1:
        #request.session['user_id'] = ul[0].id
        #request.session['user_name'] = ul[0].uname
        msg = f'success,{ul[0].id}'
        return HttpResponse(msg)
    else:
        msg = f'failure,{0}'
        return HttpResponse(msg)

def mobile_changepassword(request):
    user_id = request.GET.get('user_id')
    new_password = request.GET.get('new_password')
    current_password = request.GET.get('current_password')
    print("username:::" + user_id)
    print("current_password" + str(current_password))
    try:
        ul = user_login.objects.get(id=int(user_id), password=current_password)
        if ul is not None:
            ul.password = new_password  # change field
            ul.save()
            msg = 'success'
            return HttpResponse(msg)
        else:
            msg = 'failure'
            return HttpResponse(msg)
    except user_login.DoesNotExist:
        msg = 'failure'
        return HttpResponse(msg)


def mobile_patient_test_master_view(request):
    patient_id = int(request.GET.get('user_id'))
    pp_l = patient_report.objects.filter(patient_id=patient_id)
    ud_l = patient_details.objects.all()
    cmd = {}
    for nm in ud_l:
        cmd[nm.user_id] = f'{nm.fname} {nm.lname}'
    context = {'test_list': pp_l, 'user_list': cmd}
    return render(request, 'myapp/mobile_patient_test_master_view.html', context)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def mobile_patient_test_master_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['imagefile']
        fs = FileSystemStorage()

        pic_path = fs.save(randomString(10)+uploaded_file.name, uploaded_file)
        print(pic_path)
        ##########################################################
        file_path = pic_path
        entity_dict = {0: 'benign', 1: 'malignant'}
        filename = f'./myapp/static/myapp/media/{file_path}'
        model = start_predicting_entity(BASE_DIR)
        result = predict_entity(filename, model)
        entity_result = entity_dict[result]
        print(entity_result)
        ####################################################
        #pic_list = data_set_master.objects.all()
        #cnt = 0
        #cnt1= 0
        #selfile=''
        #selcat=1

        #print(selfile)
        #print(selcat)
        status = "new"
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')


        #cm = category_master.objects.get(id=int(selcat))

        #staff_user_id = int(request.session['user_id'])
        result = entity_result#cm.category_name


        user_id = request.POST.get('id')
        utm = patient_report(patient_id=int(user_id), file_path=pic_path, result=result, dt=dt, tm=tm,
                               status=status)
        utm.save()



        msg = f'Image Analysed . Result = ,{entity_result}'
        return HttpResponse(msg)
    else:
        context = {}

        return render(request, 'myapp/user_patient_test_master_add.html',context)




def mobile_doctor_query_view(request):
    user_id = int(request.GET.get('user_id'))
    udq_l = user_doctor_query.objects.filter(user_id=user_id)
    dp_l = doctor_prescription.objects.filter(user_id=user_id)
    dm_l = doctor_master.objects.all()
    dpl = {}
    for dp in dp_l:
        dpl[int(dp.status)] = dp.prescription

    context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl,'user_id':user_id}
    return render(request, './myapp/mobile_doctor_query_view.html', context)

def mobile_doctor_query_details_view(request):
    id = int(request.GET.get('id'))
    udq = user_doctor_query.objects.get(id=id)
    dp = doctor_prescription.objects.get(status=str(id))
    dm = doctor_master.objects.get(id=udq.doctor_id)

    context = {'query_list': udq, 'doctor_list': dm, 'prescription_list': dp}
    return render(request, './myapp/mobile_doctor_query_details_view.html', context)

def mobile_doctor_query_add(request):
    if request.method == 'POST':

        doctor_id = request.POST.get('doctor_id')
        query = request.POST.get('query')

        reply = ' '
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        r_dt = ' '
        r_tm = ' '
        user_id = int(request.POST.get('user_id'))
        prescription = ' '
        status='new'
        udq = user_doctor_query(doctor_id=int(doctor_id),query=query,reply=reply,dt=dt,
                                tm=tm,r_dt=r_dt,r_tm=r_tm,user_id=user_id,status=status )
        udq.save()

        query_id = user_doctor_query.objects.all().aggregate(Max('id'))['id__max']
        dp = doctor_prescription(prescription=prescription,status=str(query_id),doctor_id=doctor_id,user_id=user_id,dt=dt,tm=tm)
        dp.save()

        dm_l = doctor_master.objects.all()
        context = {'msg':'Record Added','doctor_list': dm_l, 'user_id': user_id}
        return render(request, './myapp/mobile_doctor_query_add.html', context)
    else:
        user_id = int(request.GET.get('user_id'))
        dm_l = doctor_master.objects.all()
        context = { 'doctor_list': dm_l,'user_id':user_id}
        return render(request, './myapp/mobile_doctor_query_add.html', context)



##############################################################
import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

################### Doctor Functions

from .models import doctor_master
def doctor_details_add(request):
    if request.method == 'POST':

        d_descp = request.POST.get('d_descp')
        d_qualification = request.POST.get('d_qualification')

        d_category = request.POST.get('d_category')
        #dt = datetime.today().strftime('%Y-%m-%d')
        #tm = datetime.today().strftime('%H:%M:%S')

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = '1234'
        uname=email
        status = "new"

        ul = user_login(uname=uname, password=password, utype='doctor')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        dm = doctor_master(d_descp=d_descp,d_qualification=d_qualification,d_category=d_category,user_id=user_id,fname=fname, lname=lname,  contact=contact,
                               status=status,email=email)
        dm.save()

        print(user_id)
        context = { 'msg': 'Record Added'}
        return render(request, 'myapp/doctor_login.html',context)

    else:
        return render(request, 'myapp/doctor_details_add.html')

def doctor_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, password=pwd, utype='doctor')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/doctor_home.html')
        else:
            msg = 'Invalid Uname or Password !!!'
            context ={ 'msg':msg }
            return render(request, './myapp/doctor_login.html',context)
    else:
        msg = ''
        context ={ 'msg':msg }
        return render(request, './myapp/doctor_login.html',context)


def doctor_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return doctor_login(request)
    else:
        return render(request,'./myapp/doctor_home.html')

def doctor_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return doctor_login(request)
    else:
        return doctor_login(request)

def doctor_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,password=opasswd,utype='doctor')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/doctor_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/doctor_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/doctor_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/doctor_changepassword.html', context)

from .models import symptom_master
def doctor_symptom_master_add(request):
    if request.method == 'POST':

        symptom_name = request.POST.get('symptom_name')

        sd = symptom_master(symptom_name=symptom_name)
        sd.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/doctor_symptom_master_add.html', context)
    else:
        return render(request, './myapp/doctor_symptom_master_add.html')

def doctor_symptom_master_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        symptom_name = request.POST.get('symptom_name')
        sd = symptom_master.objects.get(id=int(s_id))

        sd.symptom_name = symptom_name
        sd.save()
        msg = 'Record Updated'
        sd_l = symptom_master.objects.all()
        context = {'symptom_list': sd_l, 'msg': msg}
        return render(request, './myapp/doctor_symptom_master_view.html', context)
    else:
        id = request.GET.get('id')
        sd = symptom_master.objects.get(id=int(id))
        context = {'symptom_name':sd.symptom_name,'s_id':sd.id}
        return render(request, './myapp/admin_symptom_master_edit.html',context)

def doctor_symptom_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    sd = symptom_master.objects.get(id=int(id))
    sd.delete()
    msg = 'Record Deleted'
    sd_l = symptom_master.objects.all()
    context = {'symptom_list': sd_l,'msg':msg}
    return render(request, './myapp/doctor_symptom_master_view.html',context)

def doctor_symptom_master_view(request):

    sd_l = symptom_master.objects.all()
    context = {'symptom_list':sd_l}
    return render(request, './myapp/doctor_symptom_master_view.html',context)

from .models import disease_master
def doctor_disease_master_add(request):
    if request.method == 'POST':

        disease_name = request.POST.get('disease_name')
        disease_descp = request.POST.get('disease_descp')

        dm = disease_master(disease_name=disease_name,disease_descp=disease_descp)
        dm.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/doctor_disease_master_add.html', context)
    else:
        return render(request, './myapp/doctor_disease_master_add.html')

def doctor_disease_master_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        disease_name = request.POST.get('disease_name')
        disease_descp = request.POST.get('disease_descp')
        dm = disease_master.objects.get(id=int(s_id))
        dm.disease_name = disease_name
        dm.disease_descp = disease_descp
        dm.save()
        msg = 'Record Updated'
        dm_l = disease_master.objects.all()
        context = {'disease_list': dm_l, 'msg': msg}
        return render(request, './myapp/doctor_disease_master_view.html', context)
    else:
        id = request.GET.get('id')
        dm = disease_master.objects.get(id=int(id))
        context = {'disease_name':dm.disease_name,'disease_descp':dm.disease_descp,'s_id':dm.id}
        return render(request, './myapp/doctor_disease_master_edit.html',context)

def doctor_disease_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    dm = disease_master.objects.get(id=int(id))
    dm.delete()
    msg = 'Record Deleted'
    dm_l = disease_master.objects.all()
    context = {'disease_list': dm_l,'msg':msg}
    return render(request, './myapp/doctor_disease_master_view.html',context)

def doctor_disease_master_view(request):

    dm_l = disease_master.objects.all()
    context = {'disease_list':dm_l}
    return render(request, './myapp/doctor_disease_master_view.html',context)

from .models import drug_master
def doctor_drug_master_add(request):
    if request.method == 'POST':

        drug_name = request.POST.get('drug_name')
        drug_details = request.POST.get('drug_details')
        company_details = request.POST.get('company_details')
        dosage_details = request.POST.get('dosage_details')

        dm = drug_master(drug_name=drug_name,drug_details=drug_details,company_details=company_details,dosage_details=dosage_details)
        dm.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/doctor_drug_master_add.html', context)
    else:
        return render(request, './myapp/doctor_drug_master_add.html')

def doctor_drug_master_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        drug_name = request.POST.get('drug_name')
        drug_details = request.POST.get('drug_details')
        company_details = request.POST.get('company_details')
        dosage_details = request.POST.get('dosage_details')

        dm = drug_master.objects.get(id=int(s_id))
        dm.drug_name = drug_name
        dm.drug_details = drug_details
        dm.company_details = company_details
        dm.dosage_details = dosage_details
        dm.save()
        msg = 'Record Updated'
        dm_l = drug_master.objects.all()
        context = {'drug_list': dm_l, 'msg': msg}
        return render(request, './myapp/doctor_drug_master_view.html', context)
    else:
        id = request.GET.get('id')
        dm = drug_master.objects.get(id=int(id))
        context = {'drug_name':dm.drug_name,'drug_details':dm.drug_details,'company_details':dm.company_details,'dosage_details':dm.dosage_details,'s_id':dm.id}
        return render(request, './myapp/doctor_drug_master_edit.html',context)

def doctor_drug_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    dm = drug_master.objects.get(id=int(id))
    dm.delete()
    msg = 'Record Deleted'
    dm_l = drug_master.objects.all()
    context = {'drug_list': dm_l,'msg':msg}
    return render(request, './myapp/doctor_drug_master_view.html',context)

def doctor_drug_master_view(request):

    dm_l = drug_master.objects.all()
    context = {'drug_list':dm_l}
    return render(request, './myapp/doctor_drug_master_view.html',context)

from .models import disease_drug_map
def doctor_disease_drug_map_delete(request):
    id = request.GET.get('id')
    ddm =disease_drug_map.objects.get(id=int(id))
    ddm.delete()
    disease_id = request.GET.get('disease_id')
    ddm_l = disease_drug_map.objects.filter(disease_id=int(disease_id))
    dm_l = drug_master.objects.all()
    context = {'map_list': ddm_l, 'drug_list': dm_l, 'disease_id': disease_id}
    return render(request, './myapp/doctor_disease_drug_map_view.html', context)


def doctor_disease_drug_map_view(request):
    disease_id = request.GET.get('id')
    ddm_l = disease_drug_map.objects.filter(disease_id=int(disease_id))
    dm_l=drug_master.objects.all()
    context = {'map_list':ddm_l,'drug_list':dm_l,'disease_id':disease_id}
    return render(request, './myapp/doctor_disease_drug_map_view.html',context)

def doctor_disease_drug_view(request):
    disease_id = request.GET.get('disease_id')

    dm_l = drug_master.objects.all()
    context = {'drug_list':dm_l,'disease_id':disease_id}
    return render(request, './myapp/doctor_disease_drug_view.html',context)

def doctor_disease_drug_add(request):

    disease_id = int(request.GET.get('disease_id'))
    drug_id = int(request.GET.get('drug_id'))

    ddm = disease_drug_map(disease_id=disease_id,drug_id=drug_id)
    ddm.save()
    dm_l = disease_master.objects.all()
    context = {'disease_list': dm_l,'msg': 'Record Added'}
    return render(request, './myapp/doctor_disease_master_view.html', context)

from .models import disease_symptom_map

def doctor_disease_symptom_map_delete(request):
    id = request.GET.get('id')
    ddm =disease_symptom_map.objects.get(id=int(id))
    ddm.delete()
    disease_id = request.GET.get('disease_id')
    dsm_l = disease_symptom_map.objects.filter(disease_id=int(disease_id))
    sm_l = symptom_master.objects.all()
    context = {'map_list': dsm_l, 'symptom_list': sm_l, 'disease_id': disease_id}
    return render(request, './myapp/doctor_disease_symptom_map_view.html', context)


def doctor_disease_symptom_map_view(request):
    disease_id = request.GET.get('id')
    dsm_l = disease_symptom_map.objects.filter(disease_id=int(disease_id))
    sm_l=symptom_master.objects.all()
    context = {'map_list':dsm_l,'symptom_list':sm_l,'disease_id':disease_id}
    return render(request, './myapp/doctor_disease_symptom_map_view.html',context)

def doctor_disease_symptom_view(request):
    disease_id = request.GET.get('disease_id')

    sm_l = symptom_master.objects.all()
    context = {'symptom_list':sm_l,'disease_id':disease_id}
    return render(request, './myapp/doctor_disease_symptom_view.html',context)

def doctor_disease_symptom_add(request):

    disease_id = int(request.GET.get('disease_id'))
    symptom_id = int(request.GET.get('symptom_id'))

    dsm = disease_symptom_map(disease_id=disease_id,symptom_id=symptom_id)
    dsm.save()
    dm_l = disease_master.objects.all()
    context = {'disease_list': dm_l,'msg': 'Record Added'}
    return render(request, './myapp/doctor_disease_master_view.html', context)

import os
from project.settings import BASE_DIR

from .models import user_doctor_query
from .models import doctor_prescription
def doctor_doctor_query_view(request):
    user_id = int(request.session['user_id'])
    dm = doctor_master.objects.get(user_id=user_id)
    udq_l = user_doctor_query.objects.filter(doctor_id=dm.id)
    dp_l = doctor_prescription.objects.filter(doctor_id=dm.id)
    dm_l = doctor_master.objects.all()
    dpl = {}
    for dp in dp_l:
        dpl[int(dp.status)] = dp.prescription

    context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
    return render(request, './myapp/doctor_doctor_query_view.html', context)


def doctor_doctor_query_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        user_id = int(request.session['user_id'])
        dm = doctor_master.objects.get(user_id=user_id)
        udq_l = user_doctor_query.objects.filter(doctor_id=dm.id,query__contains=query)
        dp_l = doctor_prescription.objects.filter(doctor_id=dm.id)
        dm_l = doctor_master.objects.all()
        dpl = {}
        for dp in dp_l:
            dpl[int(dp.status)] = dp.prescription
        context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
        return render(request, './myapp/doctor_doctor_query_view.html', context)
    else:
        context = {}
        return render(request, './myapp/doctor_doctor_query_search.html', context)

def doctor_doctor_query_search2(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        user_id = int(request.session['user_id'])
        dm = doctor_master.objects.get(user_id=user_id)
        udq_l = user_doctor_query.objects.filter(doctor_id=dm.id,dt=query)
        dp_l = doctor_prescription.objects.filter(doctor_id=dm.id)
        dm_l = doctor_master.objects.all()
        dpl = {}
        for dp in dp_l:
            dpl[int(dp.status)] = dp.prescription
        context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
        return render(request, './myapp/doctor_doctor_query_view.html', context)
    else:
        context = {}
        return render(request, './myapp/doctor_doctor_query_search2.html', context)

def doctor_doctor_query_update(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')

        reply = request.POST.get('reply')
        r_dt = datetime.today().strftime('%Y-%m-%d')
        r_tm = datetime.today().strftime('%H:%M:%S')
        prescription = request.POST.get('prescription')
        udq = user_doctor_query.objects.get(id=int(s_id))
        udq.reply = reply
        udq.r_dt = r_dt
        udq.t_tm = r_tm
        udq.save()

        dp = doctor_prescription.objects.get(status=str(s_id))
        dp.prescription = prescription
        dp.save()

        user_id = int(request.session['user_id'])
        dm = doctor_master.objects.get(user_id=user_id)
        udq_l = user_doctor_query.objects.filter(doctor_id=dm.id)
        dp_l = doctor_prescription.objects.filter(doctor_id=dm.id)
        dm_l = doctor_master.objects.all()
        dpl = {}
        for dp in dp_l:
            dpl[int(dp.status)] = dp.prescription

        context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
        return render(request, './myapp/doctor_doctor_query_view.html', context)

    else:
        s_id = request.GET.get('id')

        context = { 's_id': s_id}
        return render(request, './myapp/doctor_doctor_query_update.html', context)

def doctor_user_view(request):
    ul_l = user_login.objects.filter(utype='patient')

    tm_l = []
    for u in ul_l:
        ud = patient_details.objects.get(user_id=u.id)
        tm_l.append(ud)

    context = {'user_list':tm_l,'type':'User Details'}
    return render(request, './myapp/doctor_user_view.html',context)

def doctor_doctor_view(request):
    ul_l = user_login.objects.filter(utype='doctor')

    tm_l = []
    for u in ul_l:
        ud = doctor_master.objects.get(user_id=u.id)
        tm_l.append(ud)

    context = {'user_list':tm_l,'type':'Doctor Details'}
    return render(request, './myapp/doctor_doctor_view.html',context)

def doctor_patient_test_master_view(request):
    user_id = request.GET.get('user_id')
    ul = user_login.objects.get(id=int(user_id))
    pp_l = patient_report.objects.filter(patient_id=ul.id)
    ud_l = patient_details.objects.all()
    cmd = {}
    for nm in ud_l:
        cmd[nm.user_id] = f'{nm.fname} {nm.lname}'
    context = {'test_list': pp_l, 'user_list': cmd}
    return render(request, 'myapp/doctor_patient_test_master_view.html', context)
