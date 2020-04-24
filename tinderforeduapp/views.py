from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import SignUpForm, CommentForm, AdditionalForm, Editprofileform,profilepicture
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django import db
from django.db import close_old_connections


datetime_now = datetime.now()#collect a current time


def home(request):#this function is used when user get in home pahe
    return render(request, 'tinder/home.html')

def signup(request):#this function is used when user signup
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():#check this form is valid
            user = form.save(commit=False)#get form and setting we did not commit yet because user must confirm the registration in email
            user.is_active = False
            user.save()
            user.refresh_from_db()#refresh db for get new model
            #Collect a infomation user
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.college = form.cleaned_data.get('college')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.birthday = form.cleaned_data.get('birthday')
            #create a model for collect a information user
            new_user = UserInfo.objects.create(name=user.username,
                                              school=user.profile.college,
                                              school_keyword=change_school_to_keyword(user.profile.college),
                                              age=user.profile.age,
                                              firstname=user.profile.first_name,
                                              lastname=user.profile.last_name,
                                              gender =user.profile.gender,
                                              birthday=user.profile.birthday)
            #Add profile picture in model with default.png
            Profilepicture.objects.create(user=new_user, images='default.png')
            #save model
            new_user.save()
            user.save()
            #send email for confirm signup
            current_site = get_current_site(request)
            mail_subject = 'Please verify your email address.'
            message = render_to_string('tinder/acc_active_email.html', {
                                        'user': user,
                                        'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user), })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            db.connection.close()
            return render(request,'tinder/email_sent.html')#render send email templates

    else:
        #form is not valid
        form = SignUpForm()
    return render(request, 'tinder/signup.html', {'form': form})#render Signup form

def account_activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'): #this function is used for confirm your signup in email
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request,'tinder/Activation_success.html')
    else:
        return HttpResponse('''Activation link is invalid! <META HTTP-EQUIV="Refresh" CONTENT="5;URL=/login">''')

def personal_profile(request, user_id):#this function is used to watch personal profile
    User = UserInfo.objects.get(name=request.user.username)#get a data user to display on browser
    comments = Comment.objects.filter(post=request.user.id)#get comment that another user commend
    profile_picture = Profilepicture.objects.get(user=User)#get a profile picture
    User.check_birthday(datetime_now)#check birthday user
    all_expertise_subject = UserInfo.objects.get(name=request.user.username).expertise.all()
    if request.POST.get('subject_good'):#get request when user add good subject
        subject = Subject.objects.create(subject_name=request.POST['subject_good'],
                                         keyword_subject=change_subject_to_keyword(request.POST['subject_good']))#create object subject
        User=UserInfo.objects.get(name=request.user.username)
        User.expertise.add(subject)#add good subject to user model
        User.save()
        #render a personal_profile.html templates
        return render(request,
                      'tinder/personal_profile.html',
                      {'comments': comments,
                       'pic':profile_picture,
                       'user_infomation': User,
                       'subject': all_expertise_subject})
    # render a personal_profile.html templates
    return render(request, 'tinder/personal_profile.html',
                  {'comments': comments,
                   'pic':profile_picture,
                   'user_infomation': User,
                   'subject': all_expertise_subject})
def successlogin(request):#this function is used to go to home templates when user can login
    if request.POST.get('login'):
        return render(request,
                      'tinder/home.html',
                      {'user_infomation': request.user.username })#render home templates
def another_profile(request,user_id):#this function is used to watch another user profile
    another_people = UserInfo.objects.get(id=user_id)  # get model user that he want to see
    another_people.check_birthday(datetime_now)  # check birthday user
    picture = Profilepicture.objects.get(user=user_id)#get profile picture
    comments = Comment.objects.filter(post=request.user.id)#get comment

    Username = UserInfo.objects.get(name=request.user.username)#get model user
    #create chat room url
    Url_list = [Username.name,another_people.name]
    Url_list_sort=sorted(Url_list)
    Url_chat =Url_list_sort[0]+"_"+Url_list_sort[1]

    if another_people.request.filter(who_send=Username.name).exists():#check if this user matched with him can open chat room
        return render(request, 'tinder/profile.html', {'comments': comments,
                                                       'pic':picture,
                                                       'user_infomation': UserInfo.objects.get(name=request.user.username),
                                                       'subject': UserInfo.objects.get(id=user_id).expertise.all(),
                                                       'profile': UserInfo.objects.get(id=user_id),
                                                       'check':1,  #if check == 1 template will show unmatch button
                                                       "chat_room_name":Url_chat})#render profile templates,check variable is used to check if this user matched with him he can chat
    return render(request,'tinder/profile.html',
                  {'comments': comments,
                   'pic':picture,
                   'profile': another_people,
                   'subject':another_people.expertise.all(),
                   'user_infomation': UserInfo.objects.get(name =request.user.username),
                   "chat_room_name":Url_chat})


def add_school_data(request):#check if users signup with facebook then they do not have school data
    if request.method == "POST":
        form = AdditionalForm(request.POST)
        if form.is_valid():#check form is valid so add school name in userinformation model
            school = form.cleaned_data.get('school')
            facebook_user = UserInfo.objects.get(name=request.user.username)
            facebook_user.school = school
            facebook_user.school_keyword = change_school_to_keyword(school)
            facebook_user.save()
            return HttpResponseRedirect('/')
    else:
        form = AdditionalForm()
    return render(request, 'tinder/adddata.html', {'form': form})

def home_page(request):#this function contain all fucntion in home template
    """search here"""
    search_tutor = [] #this variable used to collect all tutor that user can find
    sendPOST = 0 # check if

    if (UserInfo.objects.filter(name=request.user.username).count() == 0):#check if user do not login
        return HttpResponseRedirect('/login')
    if UserInfo.objects.get(name=request.user.username).school == '':
        return HttpResponseRedirect('/adddata')
    User = UserInfo.objects.get(name=request.user.username)
    User.check_birthday(datetime_now)#check birthday user
    if request.POST.get('tutor_find'):#check user is find a tutor
        sendPOST = 1
        what_sub = change_subject_to_keyword(request.POST['tutor_find'])#convert string to easily search
        #user is use a filter to search a tutor
        result_search = {}
        if request.POST['gender'] != "" and request.POST['school'] !=" ":#user is use filter only subject filter
            search_tutor = UserInfo.objects.filter(expertise__keyword_subject=what_sub,
                                                   school_keyword=change_school_to_keyword(request.POST['school']),
                                                   gender=request.POST['gender'])#use method filter to find a tutor
            for key in search_tutor:
                result_search[key] = Profilepicture.objects.get(user=key)#get a information that user can find
        elif request.POST['gender'] != "":#user is using gender filter
            search_tutor = UserInfo.objects.filter(expertise__keyword_subject=what_sub, gender=request.POST['gender'])
            for key in search_tutor:
                result_search[key] = Profilepicture.objects.get(user=key)
        elif request.POST['school'] != "":#user is using school filter
            search_tutor = UserInfo.objects.filter(expertise__keyword_subject=what_sub,
                                                   school_keyword=change_school_to_keyword(request.POST['school']))
            for key in search_tutor:
                result_search[key] = Profilepicture.objects.get(user=key)
        else:#user is using school filter and gender filter
            search_tutor = UserInfo.objects.filter(expertise__keyword_subject=what_sub)
            for key in search_tutor:
                result_search[key] = Profilepicture.objects.get(user=key)
        return render(request, 'tinder/home.html',
                      {'infoma':result_search,
                       'user_infomation':UserInfo.objects.get(name=request.user.username),
                       "search_result": search_tutor,
                       "search_size": len(search_tutor),
                       'sendPOST' : sendPOST,
                       "what_sub": request.POST['tutor_find']})#render home template and list tutor that user can find

    return render(request,
                  'tinder/home.html',
                  { 'user_infomation':UserInfo.objects.get(name=request.user.username),
                    "search_size": len(search_tutor),
                    'sendPOST':sendPOST,
                    'all_request':UserInfo.objects.get(name=request.user.username).request.all()})#render home template
def select_delete_expertise_subject(request, user_id):#this function is used when user remove good subject
    User = UserInfo.objects.get(id=user_id)#get information user
    modelget = get_object_or_404(UserInfo, id=user_id)#get information user
    select_subject = request.POST.getlist("subject_list")#get all subject that user want to delete
    #delete it all
    if len(select_subject) == 0:#check if user just press the button but user did not select a good subject
        pass
    else :#delete
        for i in select_subject:
            select = modelget.expertise.get(pk=i)
            select.delete()

    return HttpResponseRedirect(reverse('tinder:personal_profile', args=(User.id,)))#redirect to personal_profile.html template
def request_list(request, user_id):#show all users that what to match with this user
    match_list_id  = UserInfo.objects.get(name=request.user.username).request.all()#get all users
    list_match = []#Collect all users for create a link to watch their profile
    UserInfo.objects.get(name=request.user.username).read()  # when user get in this page notify should be 0
    for i in match_list_id:
        list_match.append(UserInfo.objects.get(name=i.who_send))#get all users information
    return render(request,
                  'tinder/request_list.html',
                  {'user_infomation':UserInfo.objects.get(name=request.user.username),
                   'match_request':UserInfo.objects.get(name=request.user.username).request.all(),
                   'list_match':list_match})#render match request template
def send_request(request, user_id):#this function is used when user want to send request to another user
    #load all user data and another users data
    Username = UserInfo.objects.get(name=request.user.username)
    picture = Profilepicture.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    another_people = UserInfo.objects.get(id=user_id)
    #just create chat url link if he already match
    Url_list = [Username.name, another_people.name]
    Url_list_sort = sorted(Url_list)
    Url_chat = Url_list_sort[0] + "_"+Url_list_sort[1]
    already_match = 0 #use to check if he do not match this variable = 0
    if request.method == "POST":
        if another_people.request.filter(who_send=Username.name,who_recive=another_people.name) or Username.request.filter(who_send=another_people.name,who_recive=Username.name) :#check if this user matched
            already_match=1
            return render(request, 'tinder/profile.html',
                          {'already_match': already_match, 'comments': comments, 'pic': picture,
                           'user_infomation': UserInfo.objects.get(name=request.user.username),
                           'subject': UserInfo.objects.get(id=user_id).expertise.all(),
                           'profile': UserInfo.objects.get(id=user_id),
                           'chat_room_name': Url_chat})
        else:
            user_name = Requestmodel.objects.create(who_send=Username.name,
                                                    request_message=request.POST['text_request'],
                                                    who_recive=another_people.name) #create a model request
            another_people.request.add(user_name)#send request to that user
            UserInfo.objects.get(id=user_id).notify()#send notify
            UserInfo.objects.get(id=user_id).save()#save model
            return render(request,
                          'tinder/profile.html',
                          {'already_match':already_match,
                           'comments': comments,
                           'pic': picture,
                           'user_infomation': UserInfo.objects.get(name=request.user.username),
                           'subject': UserInfo.objects.get(id=user_id).expertise.all(),
                           'check': 1,  # this user already send request to him/her
                           'profile':UserInfo.objects.get(id=user_id),
                           'chat_room_name':Url_chat})#render profile template
def unsend_request(request, user_id): #this function is used when user want to unmatched to another user
    # load all user data and another users data
    Username = UserInfo.objects.get(name=request.user.username)
    picture = Profilepicture.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    another_people = UserInfo.objects.get(id=user_id)
    # just create chat url link if he already matched
    Url_list = [Username.name, another_people.name]
    Url_list_sort = sorted(Url_list)
    Url_chat = Url_list_sort[0] + "_"+Url_list_sort[1]
    if request.POST.get('Unmatched'):#when user change his mind to not match this user
        # load all user data and another users data
        Username = UserInfo.objects.get(name=request.user.username)
        another_people = UserInfo.objects.get(id=user_id)
        remove_match = another_people.request.get(who_send=Username.name,who_recive=another_people.name)#get request model that is used send to
        another_people.request.remove(remove_match)#remove request model in userinfo
        Requestmodel.delete(remove_match)#remove request model
        UserInfo.objects.get(id=user_id).denotify()#remove notify
        UserInfo.objects.get(id=user_id).save()#save db
        return render(request,'tinder/profile.html',{'subject': UserInfo.objects.get(id=user_id).expertise.all(),
                                                     'pic': picture,
                                                     'user_infomation': UserInfo.objects.get(
                                                         name=request.user.username),
                                                       'profile': UserInfo.objects.get(id=user_id),
                                                       'chat_room_name':Url_chat})#render profile template
    return render(request, 'tinder/profile.html', {'comments': comments,
                                                   'pic': picture,
                                                   'user_infomation': UserInfo.objects.get(name=request.user.username),
                                                   'subject': UserInfo.objects.get(id=user_id).expertise.all(),
                                                    'profile': UserInfo.objects.get(id=user_id),
                                                   'chat_room_name':Url_chat})#render profile template
def accept_or_decline_request(request, user_id):#this function is used when you are accept or decline to people that request to you
    #contain user and another user data
    Username = UserInfo.objects.get(name=request.user.username)
    picture = Profilepicture.objects.get(user=user_id)
    another_people = UserInfo.objects.get(id=user_id)
    #url chat
    Url_list = [Username.name, another_people.name]
    Url_list_sort = sorted(Url_list)
    comments = Comment.objects.filter(post=user_id)
    chat_room_name = Url_list_sort[0] + "_"+Url_list_sort[1]
    if request.POST.get('accept'):#if user accept this profile
        match_obj = Matchmodel.objects.create(another_user=another_people.name, myself=Username.name)#create match model
        Username.match.add(match_obj)#add model to this user
        request_obj = Username.request.get(who_send=another_people.name,who_recive=Username.name)#remove request model
        Username.request.remove(request_obj)
        Requestmodel.delete(request_obj)
        match_obj2 = Matchmodel.objects.create(another_user=Username.name, myself=another_people.name)#create match model to another user to easaily to display
        another_people.match.add(match_obj2)#add model to another user
        return HttpResponseRedirect(reverse('tinder:request_list', args=(Username.id,)))#redirect match_request template
    if request.POST.get('decline'):#user do not accept
        request_obj = Username.request.get(who_send=another_people.name,who_recive=Username.name)#remove request model
        Username.request.remove(request_obj)
        Requestmodel.delete(request_obj)
        return HttpResponseRedirect(reverse('tinder:request_list', args=(Username.id,)))#redirect match_request template
    return render(request,
                  'tinder/profile_accept_or_decline.html',
                  {'comments':comments, 'pic':picture,
                   'user_infomation': UserInfo.objects.get(name=request.user.username),
                   'chat_room_name':chat_room_name,
                   'profile': UserInfo.objects.get(id=user_id),
                   'subject': UserInfo.objects.get(id=user_id).expertise.all(),
                   'request': Username.request.get(who_send=another_people.name)})#render template
def tutor_student_list(request, user_id):#this function is used to display tutor or student list
    match_list_id = UserInfo.objects.get(name=request.user.username).match.all()#get all people that match with user
    list_match = {}#keep in dict to display

    for i in match_list_id:
        list_sort = []
        key = UserInfo.objects.get(name=i.myself)#get people in key
        #sorted for create url chat
        list_sort = sorted([UserInfo.objects.get(name=request.user.username).name, UserInfo.objects.get(name=i.myself).name])
        value = list_sort[0]+"_"+list_sort[1]
        list_match[key]=value #let value be a url chat and key be a user model
    return render(request, 'tinder/tutor_students_list.html',
                  {"user_infomation":UserInfo.objects.get(name=request.user.username),
                   'tutor_list':UserInfo.objects.get(id=user_id).request.all(),
                   'list_match':list_match})#render tutor student template
def watch_profile(request,user_id):#this function is used when user watch another profile
    #contain user that he want to see
    another_people = UserInfo.objects.get(id=user_id)
    another_people.check_birthday(datetime_now)#check birthday user
    post = get_object_or_404(UserInfo, name=another_people.name)
    picture = Profilepicture.objects.get(user=user_id)
    comments = post.comments.filter(active=True)
    new_comment = None #set default if this user do not comment yet
    if request.method == 'POST':#if user comment
        comment_form = CommentForm(data=request.POST)#get form
        if comment_form.is_valid():#check form is valid

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.name = request.user.username
            # Save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForm()#display form
    if request.POST.get('unmatch'):#user want to unmatch (its like unfriend in facebook)
        Username = UserInfo.objects.get(name=request.user.username)#Collect this user data
        #remove match class
        unmatch_obj= Username.match.get(another_user=another_people.name, myself=Username.name)
        Username.match.remove(unmatch_obj)
        Matchmodel.delete(unmatch_obj)
        unmatch_obj2= another_people.match.get(another_user=Username.name, myself=another_people.name)
        another_people.match.remove(unmatch_obj2)
        Matchmodel.delete(unmatch_obj2)
        return HttpResponseRedirect(reverse('tinder:tutor_student_list', args=(Username.id,)))#redirect to tutor_student_list
    return render(request,'tinder/watch_profile.html',
                  {'pic':picture,
                   'user_information':UserInfo.objects.get(name=request.user.username),
                   'profile':UserInfo.objects.get(id=user_id),
                   'post': post, 'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})#render watch proflie template

def edit_profile(request,user_id):#this function is used when user edit his/her profile
    User = UserInfo.objects.get(name=request.user.username)#get user data
    picture = Profilepicture.objects.get(user= User)#get user Profile picture
    if request.method == "POST":#if user submit edit profile
        form = Editprofileform(request.POST,instance=User)#form infomation user
        formpic = profilepicture(request.POST,request.FILES,instance=picture)#form user Profile picture
        if form.is_valid() and formpic.is_valid():#check form is valid
            form.save()#save data
            formpic.save()#save data
            return HttpResponseRedirect(reverse('tinder:personal_profile', args=(user_id,)))#redirect

    else: #user do not submit to edit profile
        form = Editprofileform(instance=User)
        formpic = profilepicture(instance=picture)
    return render(request,'tinder/edit_profile.html',{"pic":picture,'form':form,'formpic':formpic})
#convert string function to easily search
def change_subject_to_keyword(keyword):
    keyword = keyword.lower()
    keyword = keyword.replace(' ', '')
    return keyword
def change_school_to_keyword(keyword):
    keyword = keyword.upper()
    keyword = keyword.replace(' ','')
    return keyword