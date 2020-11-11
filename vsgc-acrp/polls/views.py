from django.shortcuts import render
from django.forms import ModelForm
from .forms import ApplicantForm,SearchForm,FacultyForm,Recommendation_fields_Form,Status
from .models import Applicant,Faculty,Recommendation_fields,user_profile
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib import messages 
from collections import defaultdict
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db.models import Avg
from django.contrib.auth.decorators import permission_required
# Create your views here.
def index(request):
    form=ApplicantForm()
    if request.method == "POST":
        form=ApplicantForm(request.POST,request.FILES)
        email=FacultyForm(request.POST)
        if form.is_valid() and email.is_valid():
            cheque_no=request.POST.get('cheque_no')
            print(cheque_no)
            if Applicant.objects.filter(cheque_no=cheque_no).count() == 0:
                f=form.save()
                rqt = request.POST.keys()
                fDetails = {}
                for i in rqt:
                    fDetails[i] = request.POST[i]
                print('--> saving email...')
                #--- save ref1
                refDict = {}
                ref1Email = request.POST['Ref1_Email']
                ref2Email = request.POST['Ref2_Email']
                ref3Email = request.POST['Ref3_Email']
                refMail = Faculty(Ref1_Email=ref1Email, Ref2_Email=ref2Email, Ref3_Email=ref3Email, Applicant=f)
                refMail.save()
                if fDetails['stat'] == 'Evaluation Completed':
                    #send an email
                    for i in range(1,4):
                        msg_html =render_to_string('polls/error.html',{'details' : fDetails,'url':'http://127.0.0.1:8000/acrpsite/acrp/advisor/'+fDetails['cheque_no']+'/'+str(i)})
                        send_mail('django test mail','Hello '+fDetails['Ref'+str(i)+'_Name'],settings.EMAIL_HOST_USER,[fDetails['Ref'+str(i)+'_Email']],html_message=msg_html,fail_silently=False)    
                return render(request,'polls/Thankyou.html',{'f':f})
                return HttpResponseRedirect("/acrpsite/acrp/")
            else:
                messages.error(request,('Enter unique Nine character id '))
        else:
            print('----> Form Not Valid....')
            print('form.errors')
            print(form.errors)
            return render(request,'polls/errormsg.html',{'form':form})
    else:
        form = ApplicantForm()
        email=FacultyForm() # faculty
    return render(request, 'polls/index.html', {'form': form,'email':email})


def search(request):
    form = SearchForm()
    if request.method == "POST":
        passCode = request.POST.get('searchValue')
        print(passCode)
        x = Applicant.objects.get(cheque_no=passCode)
        print(x.Email)
        return render(request,'polls/searchbox.html',{'form' : form,'Applicant' : x})
    else:
        return render(request,'polls/searchbox.html',{'form' : form})


def saved_application(request,Applicant_id):
    saved=get_object_or_404(Applicant,pk=Applicant_id)
    saved_faculty = get_object_or_404(Faculty,Applicant_id = Applicant_id)
    if request.method == "POST":
        updated_form = ApplicantForm(request.POST,request.FILES, instance = saved)
        updated_faculty=FacultyForm(request.POST,instance=saved_faculty)
        print('--> Request ', request.POST)
        if updated_form.is_valid() and updated_faculty.is_valid():
            f = updated_form.save()
            rqt = request.POST.keys()
            fDetails = {}
            for i in rqt:
                fDetails[i] = request.POST[i]
            print('--> saving email...')
            print('Applicant data updated...')
            refDict = {}
            ref1Email = request.POST['Ref1_Email']
            ref2Email = request.POST['Ref2_Email']
            ref3Email = request.POST['Ref3_Email']
            Faculty.objects.filter(Applicant_id = Applicant_id).update(Ref1_Email=ref1Email, Ref2_Email=ref2Email, Ref3_Email=ref3Email)
            print('faculty data saved...')
            if fDetails['stat'] == 'Evaluation Completed':
                #send an email
                for i in range(1,4):
                    msg_html =render_to_string('polls/error.html',{'details' : fDetails,'url':'http://127.0.0.1:8000/acrpsite/acrp/advisor/'+fDetails['cheque_no']+'/'+str(i)})
                    send_mail('django test mail','Hello '+fDetails['Ref'+str(i)+'_Name'],settings.EMAIL_HOST_USER,[fDetails['Ref'+str(i)+'_Email']],html_message=msg_html,fail_silently=False)    
            return HttpResponseRedirect("/acrpsite/acrp/evaluator/search")
        else:
            print('----> Form Not Valid....')
            return render(request,'polls/errormsg.html',{'form':updated_form})
    else:
        f=ApplicantForm(instance = saved)
        faculty_form = FacultyForm(instance = saved_faculty)
        return render(request,'polls/saved_application.html',{'form' : saved,'f':f, 'faculty':faculty_form})


def advisor(request,cheque_no, ref_num):
    if (ref_num>3 or ref_num<=0):
        return render(request,'polls/errormsg.html')
    else:
        saved=get_object_or_404(Applicant,cheque_no=cheque_no)
        if not submitted(saved.id,ref_num):
            saved_faculty = get_object_or_404(Faculty,Applicant_id = saved.id)
            rec=Recommendation_fields_Form()
            if request.method == "POST":
                rec=Recommendation_fields_Form(request.POST,request.FILES)
                if rec.is_valid():
                    ref1 = request.POST['In_what_capacity_do_you_know_the_applicant']
                    ref2 = request.POST['How_Long_have_you_known_the_applicant']
                    ref3 = request.POST['Knowledge_of_major_field']
                    ref4 = request.POST['Research_skills']
                    ref5 = request.POST['Problem_solving_skills']
                    ref6 = request.POST['Creativity']
                    ref7 = request.POST['Leadership']
                    ref8 = request.POST['Written_communication']
                    ref9 = request.POST['Oral_communication']
                    ref10 = request.POST['Comment_on_the_ability_of_the_applicant']
                    ref11 = request.POST['Add_other_comments_to_the_evaluation']
                    ref12 = request.FILES['Signed_letter_of_reference']
                    recom=Recommendation_fields(In_what_capacity_do_you_know_the_applicant=ref1,How_Long_have_you_known_the_applicant=ref2,
                        Knowledge_of_major_field=ref3,Research_skills=ref4,Problem_solving_skills=ref5,Creativity=ref6,Leadership=ref7,
                        Written_communication=ref8,Oral_communication=ref9,Comment_on_the_ability_of_the_applicant=ref10,
                        Add_other_comments_to_the_evaluation=ref11,Signed_letter_of_reference=ref12,Applicant=saved,faculty_num=ref_num)
                    recom.save()
                    return render(request,'polls/Thankyou.html') 
                print(' !!! Form Invalid !!!')
                return render(request,'polls/errormsg.html',{'form':rec})
            else:
                f=ApplicantForm(instance = saved)
                faculty_form = FacultyForm(instance = saved_faculty)
                rec=Recommendation_fields_Form()
                return render(request,'polls/advisor.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec ,'ref_num':str(ref_num)})
        else:
            return render(request,'polls/advisor_error.html')


 
def submitted(Applicant_id,ref_num):
    try:
        found=Recommendation_fields.objects.get(Applicant_id=Applicant_id,faculty_num=ref_num)
        print('--> Data Found')
        return True
    except:
        print('--> Data Not Found')
        return False

def submit(request):
    form = SearchForm()
    if request.method == "POST":
        passCode = request.POST.get('searchValue')
        print(passCode)
        x = Applicant.objects.get(cheque_no=passCode)
        print(x.Email)
        return render(request,'polls/submit.search.html',{'form' : form,'Applicant' : x})
    else:
        return render(request,'polls/submit.search.html',{'form' : form})



def submit_application(request,Applicant_id):
    saved=get_object_or_404(Applicant,pk=Applicant_id)
    saved_faculty = get_object_or_404(Faculty,Applicant_id = Applicant_id)
    if request.method == "POST":
        updated_form = ApplicantForm(request.POST,request.FILES, instance = saved)
        print('--> Request ', request.POST)
        if updated_form.is_valid():
            f = updated_form.save()
            print('Applicant data updated...')
            ref1Email = request.POST['Ref1_Email']
            ref2Email = request.POST['Ref2_Email']
            rfaEmail = request.POST['RFA_Email']
            Faculty.objects.filter(Applicant_id = Applicant_id).update(Ref1_Email=ref1Email, Ref2_Email=ref2Email, RFA_Email=rfaEmail)
            print('faculty data saved...')
            return render(request,'polls/Thankyou.html') 
        print(' !!! Form Invalid !!!')
        print(updated_form.errors)
        return render(request,'polls/errormsg.html',{'form':updated_form})
    else:
        f=ApplicantForm(instance = saved)
        faculty_form = FacultyForm(instance = saved_faculty)
        return render(request,'polls/submit_application.html',{'form' : saved,'f':f, 'faculty':faculty_form})


def user(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username = username , password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user=User.objects.get(username=username)
                print(user)
                return HttpResponseRedirect(reverse('support'))     
            
            else:
                return HttpResponse("ACCount not active!!")

        else:
            print("someone tried to login and falied!")
            print("Username : {} and Password : {}".format(username,password))
            return HttpResponse("Invalid credentials!")

    else:
        return render(request , 'registration/project2.html' , {})

@login_required(login_url='/acrpsite/acrp/elog/')
def support(request):
    return render(request,'polls/openpage.html')

def process(request):
    details={}
    saved=Applicant.objects.filter(stat="Evaluation Completed")
    for i in saved:
        vals=list(Recommendation_fields.objects.filter(Applicant_id=i.id).values_list('faculty_num', flat=True))
        tmp = []
        for f in range(0,3):
            if str(f+1) in vals:
                tmp.append(str(f+1))
            else:
                tmp.append(0)
        details[i.id] = tmp
    print(details)
    return render(request,'polls/process.html',{'saved':saved, 'rec': details})


def process_detail(request,Applicant_id):
    saved=get_object_or_404(Applicant,pk=Applicant_id)
    refRec = []
    saved_faculty = get_object_or_404(Faculty,Applicant_id = Applicant_id)
    if request.method == "POST":
        saved.stat=request.POST["stat"]
        saved.save()
        permissions = Permission.objects.get(id=50)
        users = User.objects.filter(user_permissions=permissions)
        if saved.stat=="Approved":
            for user in users:
                up=user_profile(eval_id=user,Applicant=saved,stat="Pending")
                up.save()
                print("profile created for ",user.id)
        # return HttpResponseRedirect("/process/")
        return render(request,'polls/Thankyou.html')
    else:
        f=ApplicantForm(instance = saved)
        faculty_form = FacultyForm(instance = saved_faculty)
        try:
            rec=Recommendation_fields.objects.order_by('faculty_num')
            rec = rec.filter(Applicant_id=saved.id)
            numRec=Recommendation_fields.objects.filter(Applicant_id=saved.id).count()
            print('--> num of records : ', numRec)
            print('--> Retrieved Records :',rec)
            for i in rec:
                print('----> ',i.faculty_num)
                refRec.append(int(i.faculty_num))
            print(refRec)
            # rec=Recommendation_fields_Form(instance=rec)
        except:
            rec = 'Not Submitted'
        return render(request,'polls/process_detail.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec,'refRec':refRec,'final':[1,2,3]})

def processed(request):
    saved=Applicant.objects.filter(stat__in=("Approved","Rejected"))
    print(saved)
    return render(request,'polls/processed.html',{'saved':saved})


def processed_detail(request,Applicant_id):
    saved=get_object_or_404(Applicant,pk=Applicant_id)
    refRec = []
    saved_faculty = get_object_or_404(Faculty,Applicant_id = Applicant_id)
    f=ApplicantForm(instance = saved)
    faculty_form = FacultyForm(instance = saved_faculty)
    try:
        rec=Recommendation_fields.objects.order_by('faculty_num')
        rec = rec.filter(Applicant_id=saved.id)
        numRec=Recommendation_fields.objects.filter(Applicant_id=saved.id).count()
        print('--> num of records : ', numRec)
        print('--> Retrieved Records :',rec)
        for i in rec:
            refRec.append(int(i.faculty_num))
    except:
        rec = 'Not Submitted'
    return render(request,'polls/processed_detail.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec,'refRec':refRec,'final':[1,2,3]})

def getrecommendations(request,cheque_no,ref_num):
    saved=get_object_or_404(Applicant,cheque_no=cheque_no)
    saved_faculty = get_object_or_404(Faculty,Applicant_id = saved.id)
    rec=get_object_or_404(Recommendation_fields,Applicant_id=saved.id,faculty_num=ref_num)
    f=ApplicantForm(instance = saved)
    faculty_form = FacultyForm(instance = saved_faculty)
    rec=Recommendation_fields_Form(instance=rec)
    return render(request,'polls/getrecommendations.html',{'form' : saved,'f':f, 'faculty':faculty_form,'rec':rec ,'ref_num':str(ref_num)})

def RecommendationsAllInternal(request):
    saved=Applicant.objects.filter(stat=("Approved"))
    print(saved)
    return render(request,'polls/RecommendationsAllInternal.html',{'saved':saved})


@login_required(login_url='/acrpsite/acrp/log/')
def evaluators(request):
    permission = Permission.objects.get(name='view Completed Submissions')
    if request.user.groups.filter(name='polls_evaluators_completed_submissions').exists():
        print('User belongs to the group')
    if 'polls.view_polls_completed_submissions' in request.user.get_group_permissions():
        perm = True
        print('User has permission to view completed submissions')
    else:
        perm = False
        print('User has NO permission to view completed submissions')
    return render(request,'polls/evaluators.html', context = {"perm":perm})



def EvaluateSubmissions(request):
    daDb = {}
    d_eval=user_profile.objects.filter(eval_id_id=request.user.id,stat__in=('Pending','Evaluation Saved'))
    for i in range(d_eval.count()):
        applicantId = d_eval[i].Applicant_id
        stat=user_profile.objects.get(Applicant_id=applicantId,eval_id_id=request.user.id).stat
        student=Applicant.objects.get(id = int(applicantId))
        if str(applicantId) not in daDb:
            daDb[str(applicantId)]={}
        daDb[str(applicantId)]["stat"] =stat
        daDb[str(applicantId)]["student"] =student 
    print('daDb',daDb)
    return render(request,'polls/EvaluateSubmissions.html',{'dApps' : daDb})




def compute_average(request):
    d_eval = user_profile.objects.filter(stat='Evaluation Completed')
    applicantNew1={}
    applicantNew={}
    # from the valid items iterate and populate the two data structures
    for i in range(d_eval.count()):
        applicantId = d_eval[i].Applicant_id
        evaluatorId = d_eval[i].eval_id_id
        score = d_eval[i].ranking
        print("score",score)
        name =Applicant.objects.get(id = int(applicantId)).App_FirstName
        profile=User.objects.get(id = int(evaluatorId)).username
        if str(applicantId) not in applicantNew1:
            applicantNew1[str(applicantId)] = {}
            applicantNew[str(applicantId)] = {}
        applicantNew1[str(applicantId)]["name"] = name
        applicantNew1[str(applicantId)][evaluatorId] = {profile:score}
        print("old",applicantNew1)
        # applicantNew1[str(applicantId)]["score"] = score
    # applicantNew = applicantNew1
    for k,l in applicantNew1.items():
        e=0
        count=0
        for p,m in l.items():
            if type(m) is dict:   
                for q,w in m.items():
                    count = count+1
                    e = e+int(w)
                    e = e/count
                    applicantNew[k]["total"] = e
                    print('applicantNew',applicantNew)
    for r,t in applicantNew.items():
        applicantNew1[r]["average"] = t
    print("new",applicantNew1)
    return render(request,'polls/compute_average.html',{'applicantNew':applicantNew1})
    

def compute_average_detail(request,a_id):
    applicant={}
    applicantNew1={}
    applicant_info=get_object_or_404(Applicant,pk=a_id)
    d_eval=user_profile.objects.filter(Applicant_id=a_id)
    for i in range(d_eval.count()):
        evaluatorId = d_eval[i].eval_id_id
        score = d_eval[i].ranking
        profile=User.objects.get(id = int(evaluatorId)).username
        if str(a_id) not in applicantNew1:
            applicantNew1[str(a_id)] = {}
        applicantNew1[str(a_id)][evaluatorId] = {profile:score}
        print("dict2",applicantNew1) 
    return render(request,'polls/compute_average_detail.html',{'applicant':applicant_info,'eval':d_eval,'applicantNew':applicantNew1})




def EvaluateSubmissions_detail(request,Applicant_id):
    user_data=user_profile.objects.get(Applicant_id=Applicant_id,eval_id_id=request.user.id)
    stat=Status()
    applicant=Applicant.objects.get(pk=Applicant_id)
    applicant_info=get_object_or_404(Applicant,pk=Applicant_id)
    profile=User.objects.get(id=user_data.eval_id_id).username
    print(profile)
    if(user_data.stat=="Evaluation Completed"):
        return HttpResponseRedirect("/evaluators/")
    else:    
        if request.method == "POST":
            user_data.stat = request.POST["stat"]
            print(user_data.stat)
            user_data.ranking = request.POST["ranking"]
            user_data.save()
            return HttpResponseRedirect("/acrpsite/acrp/EvaluateSubmissions")
        else:
            stat=Status()
            f=ApplicantForm(instance = applicant_info)
        return render(request,'polls/EvaluateSubmissions_detail.html',{'f':f,'applicant':applicant,'form':applicant_info,'user':user_data,'stat':stat,'profile':profile})

def EvaluateSubmissionsSaved_detail(request,Applicant_id):
    user_data=user_profile.objects.get(Applicant_id=Applicant_id,eval_id_id=request.user.id)
    stat=Status()
    applicant=Applicant.objects.get(pk=Applicant_id)
    applicant_info=get_object_or_404(Applicant,pk=Applicant_id)
    profile=User.objects.get(id=user_data.eval_id_id).username
    print(profile)
    if(user_data.stat=="Evaluation Completed"):
        return HttpResponseRedirect("/evaluators/")
    else:    
        if request.method == "POST":
            user_data.stat = request.POST["stat"]
            print(user_data.stat)
            user_data.ranking = request.POST["ranking"]
            user_data.save()
            return HttpResponseRedirect("/acrpsite/acrp/EvaluateSubmissions")
        else:
            stat=Status(instance=user_data)
            f=ApplicantForm(instance = applicant_info)
        return render(request,'polls/EvaluateSubmissionsSaved_detail.html',{'f':f,'applicant':applicant,'form':applicant_info,'user':user_data,'stat':stat,'profile':profile})




def user_prof(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username = username , password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user=User.objects.get(username=username)
                print(user)
                return HttpResponseRedirect(reverse('evaluators'))     
            
            else:
                return HttpResponse("ACCount not active!!")

        else:
            print("someone tried to login and falied!")
            print("Username : {} and Password : {}".format(username,password))
            return HttpResponse("Invalid credentials!")

    else:
        return render(request , 'registration/project2.html' , {})


def CompletedSubmissions(request):
    d_eval = user_profile.objects.filter(stat='Evaluation Completed')
    applicantNew1={}
    applicantNew={}
    # from the valid items iterate and populate the two data structures
    for i in range(d_eval.count()):
        applicantId = d_eval[i].Applicant_id
        evaluatorId = d_eval[i].eval_id_id
        score = d_eval[i].ranking
        print("score",score)
        name =Applicant.objects.get(id = int(applicantId)).App_FirstName
        profile=User.objects.get(id = int(evaluatorId)).username
        if str(applicantId) not in applicantNew1:
            applicantNew1[str(applicantId)] = {}
            applicantNew[str(applicantId)] = {}
        applicantNew1[str(applicantId)]["name"] = name
        applicantNew1[str(applicantId)][evaluatorId] = {profile:score}
        print("old",applicantNew1)
        # applicantNew1[str(applicantId)]["score"] = score
    # applicantNew = applicantNew1
    for k,l in applicantNew1.items():
        e=0
        count=0
        for p,m in l.items():
            if type(m) is dict:   
                for q,w in m.items():
                    count = count+1
                    e = e+int(w)
                    e = e/count
                    applicantNew[k]["total"] = e
                    print('applicantNew',applicantNew)
    for r,t in applicantNew.items():
        applicantNew1[r]["average"] = t
    print("new",applicantNew1)
    return render(request,'polls/CompletedSubmissions.html',{'applicantNew':applicantNew1})



def enableCompleteSubmissions(request):
    if User.objects.get(id = request.user.id).is_superuser == 1:
        # Enable the permissions to all users in group 'polls_evaluators_completed_submissions'
        eval_group = Group.objects.get(name = 'polls_evaluators_completed_submissions')
        eval_permission = Permission.objects.get(name='view Completed Submissions')
        eval_group.permissions.add(eval_permission)
        messages.error(request,('permission Enabled '))
        print('permission Enabled')
        # notify user with permission
    else:
        # no permission to access this feature
        messages.error(request,('User has no permission '))
        print('User has no permission')
    return redirect('/acrpsite/acrp/support')


