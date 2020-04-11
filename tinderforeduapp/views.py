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
# Create your views here.

@login_required
def home(request):#this function used when user get in home pahe
    return render(request, 'tinder/home.html')

def signup(request):#this function used when user signup
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():#check this form is valid
            user = form.save(commit=False)#get form  and setting
            user.is_active = False
            user.save()
            user.refresh_from_db()#refresh db for get new model
            #Collect a infomation user
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.college = form.cleaned_data.get('college')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.bio = form.cleaned_data.get('bio')
            #create a model for collect a information user
            newuser = UserInfo.objects.create(name=user.username,
                                              school=user.profile.college,
                                              schoolkey=stringforschool(user.profile.college),
                                              age=user.profile.age,
                                              firstname=user.profile.first_name,
                                              lastname=user.profile.last_name,
                                              bio =user.profile.bio)
            #Add profile picture in model with default.png
            Profile_Picture.objects.create(user=newuser, images='default.png')
            #save model
            newuser.save()
            user.save()
            #send email for comfirm signup
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

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
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
    profile_picture = Profile_Picture.objects.get(user=User)#get a profile picture
    if request.POST.get('subject_good'):#get request when user add good subject
        subject = Subject.objects.create(subject_name=request.POST['subject_good'],
                                         subject_keep=stringforsearch(request.POST['subject_good']))#create object subject
        U1=UserInfo.objects.get(name=request.user.username)
        U1.good_subject.add(subject)#add good subject to user model
        U1.save()
        #render a personal_profile.html templates
        return render(request,
                      'tinder/personal_profile.html',
                      {'comments': comments,
                       'pic':profile_picture,
                       'name': User,
                       'subject': UserInfo.objects.get(name=request.user.username).good_subject.all()})
    # render a personal_profile.html templates
    return render(request, 'tinder/personal_profile.html',
                  {'comments': comments,
                   'pic':profile_picture,
                   'user_infomation': User,
                   'subject': UserInfo.objects.get(name=request.user.username).good_subject.all()})
def successlogin(request):#this function is used to go to home templates when user can login
    if request.POST.get('login'):
        return render(request,
                      'tinder/home.html',
                      {'name': request.user.username })#render home templates
def another_profile(request,user_id):#this function is used to watch another user profile
    pic = Profile_Picture.objects.get(user=user_id)#get profile picture
    comments = Comment.objects.filter(post=request.user.id)#get comment
    modelget = get_object_or_404(UserInfo, id=user_id)#get model user if  this model cant get return 404
    Username = UserInfo.objects.get(name=request.user.username)#get model user
    match_guy = UserInfo.objects.get(id=user_id)#get model user that he want to see
    #create chat room url
    Url_list = [Username.name,match_guy.name]
    Url_list_sort=sorted(Url_list)
    Url_chat =Url_list_sort[0]+"_"+Url_list_sort[1]
    if request.POST.get('comment_input'):#check if he want to comment
        comment_text = Comment.objects.create(comment=request.POST['comment_input'])#create comment objects
        if not Comment.objects.filter(whocomment = Username,
                                      commentto= match_guy):#check if he never comment this guy create a new comment
            comment = Comment.objects.create(comment_value = comment_text,
                                             whocomment = Username,
                                             commentto= match_guy)#create a new comment
            comment.save()
        else:#
            comment = Comment.objects.get(whocomment = Username,
                                          commentto= match_guy)#edit same comment that he commented to this guy
            comment.comment_value = comment_text
            comment.save()
    if request.POST.get('star_input'):#check if he give a score
        # check condition like comment_input
        star_score = Comment.objects.create(comment=request.POST['star_input'])
        if not Comment.objects.filter(whocomment = Username, commentto= match_guy):
            comment = Comment.objects.create(comment_value = star_score, whocomment = Username, commentto= match_guy)
            comment.save()
        else:
            comment = Comment.objects.get(whocomment = Username, commentto= match_guy)
            comment.comment_value = star_score
            comment.save()
    if match_guy.request.filter(who_send=Username.name).exists():#check if this user matched with him can open chat room
        return render(request, 'tinder/profile.html', {'comments': comments,
                                                       'pic':pic,
                                                       'user_infomation': UserInfo.objects.get(name=request.user.username),
                                                       'subject': UserInfo.objects.get(id=user_id).good_subject.all(),

                                                       'profile': UserInfo.objects.get(id=user_id),
                                                       'check':1,  #if check == 1 template will show unmatch button
                                                       "chat_room_name":Url_chat})#render profile templates,check variable is used to check if this user matched with him he can chat
    return render(request,'tinder/profile.html',
                  {'comments': comments,
                   'pic':pic,
                   'profile': modelget,
                   'subject':modelget.good_subject.all(),
                   'user_infomation': UserInfo.objects.get(name =request.user.username),
                   "chat_room_name":Url_chat})


def check_lost_information(request):#check if user did not give any information
    if request.method == "POST":
        form = AdditionalForm(request.POST)
        if form.is_valid():
            school = form.cleaned_data.get('school')
            adddata = UserInfo.objects.get(name=request.user.username)
            adddata.school = school
            adddata.schoolkey = stringforschool(school)
            adddata.save()
            return HttpResponseRedirect('/')
    else:
        form = AdditionalForm()
    return render(request, 'tinder/adddata.html', {'form': form})

def home_page(request):#this function contain all fucntion in home template
    """search here"""
    select_sub = []#this variable used to collect all tutor that user can find
    sendPOST = 0 # check if
    if (UserInfo.objects.filter(name=request.user.username).count() == 0):#check if user do not login
        return HttpResponseRedirect('/login')
    if UserInfo.objects.get(name=request.user.username).school == '':
        return HttpResponseRedirect('/adddata')
    if request.POST.get('tutor_find'):#check user find a tutor
        sendPOST = 1
        result_search = {}
        what_sub = stringforsearch(request.POST['tutor_find'])#convert string to easily to find
        #user use a filter to search a tutor
        if request.POST['bio'] != "" and request.POST['school'] !=" ":#user use filter only subject filter
            select_sub = UserInfo.objects.filter(good_subject__subject_keep=what_sub,
                                                 schoolkey=stringforschool(request.POST['school']),
                                                 bio=request.POST['bio'])#use method filter to find a tutor
            for key in select_sub:
                result_search[key] = Profile_Picture.objects.get(user=key)#get a information that user can find
        elif request.POST['bio'] != "":#user use bio filter
            select_sub = UserInfo.objects.filter(good_subject__subject_keep=what_sub, bio=request.POST['bio'])
            for key in select_sub:
                result_search[key] = Profile_Picture.objects.get(user=key)
        elif request.POST['school'] != "":#user use  school filter
            select_sub = UserInfo.objects.filter(good_subject__subject_keep=what_sub,
                                                 schoolkey=stringforschool(request.POST['school']))
            for key in select_sub:
                result_search[key] = Profile_Picture.objects.get(user=key)
        else:#user use school filter and bio filter
            select_sub = UserInfo.objects.filter(good_subject__subject_keep=what_sub)
            for key in select_sub:
                result_search[key] = Profile_Picture.objects.get(user=key)
        return render(request, 'tinder/home.html',
                      {'infoma':result_search,
                       'user_infomation':UserInfo.objects.get(name=request.user.username),
                       "search_result": select_sub,
                       "search_size": len(select_sub),
                       'sendPOST' : sendPOST,
                       "what_sub": request.POST['tutor_find']})#render home template and list tutor that user can find
    close_old_connections()#use to close all connection db
    db.connection.close()
    return render(request,
                  'tinder/home.html',
                  { 'user_infomation':UserInfo.objects.get(name=request.user.username),
                    "search_size": len(select_sub),
                    'sendPOST':sendPOST,
                    'all_request':UserInfo.objects.get(name=request.user.username).request.all()})#render home template
def select_delete_good_subject(request, user_id):#this function used when user remove good subject
    User1 = UserInfo.objects.get(id=user_id)#get information user
    modelget = get_object_or_404(UserInfo, id=user_id)#get information user
    num = request.POST.getlist("subject_list")#get all subject that user want to delete
    #delete it all
    if len(num) == 0:#check if user just press the button but user did not select a good subject
        pass
    else :#delete
        for i in num:
            select = modelget.good_subject.get(pk=i)
            select.delete()

    return HttpResponseRedirect(reverse('tinder:personal_profile.html', args=(User1.id,)))#redirect to personal_profile.html template
def match_request_list(request, user_id):#show all users that what to match with this user
    match_list_id  = UserInfo.objects.get(name=request.user.username).request.all()#get all users
    list_match = []#Collect all users for create a link to watch profile
    UserInfo.objects.get(name=request.user.username).read()  # when user get in this page notify should be 0
    for i in match_list_id:
        list_match.append(UserInfo.objects.get(name=i.who_send))#get all users information
    return render(request,
                  'tinder/match_request.html',
                  {'user_infomation':UserInfo.objects.get(name=request.user.username),
                   'match_request':UserInfo.objects.get(name=request.user.username).request.all(),
                   'list_match':list_match})#render match request template
def match(request,user_id):#this function used when user want to send request to another user
    #load all user data and another users data
    Username = UserInfo.objects.get(name=request.user.username)
    pic = Profile_Picture.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    match_guy = UserInfo.objects.get(id=user_id)
    #just create chat url link if he already match
    Url_list = [Username.name, match_guy.name]
    Url_list_sort = sorted(Url_list)
    Url_chat = Url_list_sort[0] + "_"+Url_list_sort[1]
    already_request = 0 #use to check if he did not match this variable = 0
    if request.method == "POST":
        if match_guy.request.filter(who_send=Username.name,who_recive=match_guy.name) or Username.request.filter(who_send=match_guy.name,who_recive=Username.name) :#check if this user matched
            already_request=1
            return render(request, 'tinder/profile.html',
                          {'already_match': already_request, 'comments': comments, 'pic': pic,
                           'user_infomation': UserInfo.objects.get(name=request.user.username),
                           'subject': UserInfo.objects.get(id=user_id).good_subject.all(),
                           'check': 1,  #this user already send request
                           'profile': UserInfo.objects.get(id=user_id), 'chat_room_name': Url_chat})
        else:
            user_name = Request_Class.objects.create(who_send=Username.name,
                                                     request_message=request.POST['text_request'],
                                                     who_recive=match_guy.name) #create a model request
            match_guy.request.add(user_name)#send request to that user
            UserInfo.objects.get(id=user_id).notify()#send notify
            UserInfo.objects.get(id=user_id).save()#save model
            return render(request,
                          'tinder/profile.html',
                          {'already_match':already_request,
                           'comments': comments,
                           'pic': pic,
                           'user_infomation': UserInfo.objects.get(name=request.user.username),
                           'subject': UserInfo.objects.get(id=user_id).good_subject.all(),
                           'check':1,
                           'profile':UserInfo.objects.get(id=user_id),
                           'chat_room_name':Url_chat})#render profile template
def Unmatched(request,user_id): #this function used when user want to unmatched to another user
    # load all user data and another users data
    Username = UserInfo.objects.get(name=request.user.username)
    pic = Profile_Picture.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    match_guy = UserInfo.objects.get(id=user_id)
    # just create chat url link if he already match
    Url_list = [Username.name, match_guy.name]
    Url_list_sort = sorted(Url_list)
    Url_chat = Url_list_sort[0] + "_"+Url_list_sort[1]
    if request.POST.get('Unmatched'):#when user change his mind to not match this user
        # load all user data and another users data
        Username = UserInfo.objects.get(name=request.user.username)
        match_guy = UserInfo.objects.get(id=user_id)
        remove_match = match_guy.request.get(who_send=Username.name,who_recive=match_guy.name)#get request model that used send to
        match_guy.request.remove(remove_match)#remove request model
        UserInfo.objects.get(id=user_id).denotify()#remove notify
        UserInfo.objects.get(id=user_id).save()#save db
        return render(request, 'tinder/profile.html', {'comments': comments,'pic': pic,'name': UserInfo.objects.get(name=request.user.username),
                                                       'subject': UserInfo.objects.get(id=user_id).good_subject.all(),

                                                       'profile': UserInfo.objects.get(id=user_id),
                                                       'chat_room_name':Url_chat})#render profile template
    return render(request, 'tinder/profile.html', {'comments': comments,
                                                   'pic': pic,
                                                   'name': UserInfo.objects.get(name=request.user.username),
                                                   'subject': UserInfo.objects.get(id=user_id).good_subject.all(),
                                                    'profile': UserInfo.objects.get(id=user_id),
                                                   'chat_room_name':Url_chat})#render profile template
def profile_accept_or_decline(request, user_id):
    #contain user and another user data
    Username = UserInfo.objects.get(name=request.user.username)
    pic = Profile_Picture.objects.get(user=user_id)
    match_guy = UserInfo.objects.get(id=user_id)
    #url chat
    Url_list = [Username.name, match_guy.name]
    Url_list_sort = sorted(Url_list)
    comments = Comment.objects.filter(post=user_id)
    chat_room_name = Url_list_sort[0] + "_"+Url_list_sort[1]
    if request.POST.get('accept'):#if user accept this profile
        match_obj = Match_Class.objects.create(another_user=match_guy.name, myself=Username.name)#create match model
        Username.match.add(match_obj)#add model to this user
        request_obj = Username.request.get(who_send=match_guy.name,who_recive=Username.name)#remove request model
        Username.request.remove(request_obj)
        match_obj2 = Match_Class.objects.create(another_user=Username.name, myself=match_guy.name)#create match model to another user to easaily to display
        match_guy.match.add(match_obj2)#add model to another user
        return HttpResponseRedirect(reverse('tinder:match_request', args=(Username.id,)))#redirect match_request template
    if request.POST.get('decline'):#user do not accept
        request_obj = Username.request.get(who_send=match_guy.name,who_recive=Username.name)#remove request model
        Username.request.remove(request_obj)
        return HttpResponseRedirect(reverse('tinder:match_request', args=(Username.id,)))#redirect match_request template
    return render(request,
                  'tinder/profile_accept_or_decline.html',
                  {'comments':comments, 'pic':pic,
                   'user_infomation': UserInfo.objects.get(name=request.user.username),
                   'chat_room_name':chat_room_name,
                   'profile': UserInfo.objects.get(id=user_id),
                   'subject': UserInfo.objects.get(id=user_id).good_subject.all(),
                   'request': Username.request.get(who_send=match_guy.name)})#render template
def tutor_student_list(request, user_id):#this function used to display tutor or student list
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
                   'tutor_list':UserInfo.objects.get(id=user_id).match.all(),
                   'list_match':list_match})#render tutor student template
def watch_profile(request,user_id):#this function used when user watch another profile
    #contain user that he want to see
    match_guy = UserInfo.objects.get(id=user_id)
    post = get_object_or_404(UserInfo, name=match_guy.name)
    pic = Profile_Picture.objects.get(user=user_id)
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
        unmatch_obj= Username.match.get(another_user=match_guy.name,myself=Username.name)
        Username.match.remove(unmatch_obj)
        unmatch_obj2= match_guy.match.get(another_user=Username.name,myself=match_guy.name)
        match_guy.match.remove(unmatch_obj2)
        return HttpResponseRedirect(reverse('tinder:students_list', args=(Username.id,)))#redirect to tutor_student_list
    return render(request,'tinder/watch_profile.html',
                  {'pic':pic,
                   'user_information':UserInfo.objects.get(name=request.user.username),
                   'profile':UserInfo.objects.get(id=user_id),
                   'post': post, 'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})#render watch proflie template

def edit_profile(request,user_id):#this function used when user edit his/her profile
    User = UserInfo.objects.get(name=request.user.username)#get user data
    Pic = Profile_Picture.objects.get(user= User)#get user Profile picture
    if request.method == "POST":#if user submit edit profile
        form = Editprofileform(request.POST,instance=User)#form infomation user
        formpic = profilepicture(request.POST,request.FILES,instance=Pic)#form user Profile picture
        if form.is_valid() and formpic.is_valid():#check form is valid
            form.save()#save data
            formpic.save()#save data
            return HttpResponseRedirect(reverse('tinder:your_subject', args=(user_id,)))#redirect

    else: #user do not submit to edit profile
        form = Editprofileform(instance=User)
        formpic = profilepicture(instance=Pic)
    return render(request,'tinder/edit_profile.html',{"pic":Pic,'form':form,'formpic':formpic})
#convert string function to easily to search
def stringforsearch(keyword):
    keyword = keyword.lower()
    keyword = keyword.replace(' ', '')
    return keyword
def stringforschool(keyword):
    keyword = keyword.upper()
    keyword = keyword.replace(' ','')
    return keyword