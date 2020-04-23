from django.urls import path

from . import views

from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView,PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.conf.urls import include
from django.views.generic import TemplateView

from . import views as core_views

app_name = 'tinder'
urlpatterns = [  #link between function and url when user connect to url function will run,name used in templates
    path('', views.home_page, name='home'),
    path('<int:user_id>/personal_profile/', views.personal_profile, name ='personal_profile'),
    path('<int:user_id>/select_delete/', views.select_delete_expertise_subject, name ='select_delete_expertise_subject'),
    path('login/', LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='/login'), name="logout"),
    url(r'^signup/$', core_views.signup, name='signup'),
    path('<int:user_id>/profile/',views.another_profile,name='another_profile'),
    path('chat/', include('chat.urls')),
    path('<int:user_id>/send_request/', views.send_request, name="send_request"),
    path('<int:user_id>/unsend_request/', views.unsend_request, name="unsend_request"),
    path('<int:user_id>/request_list/', views.request_list, name="request_list"),
    path('<int:user_id>/accept_or_decline_request/', views.accept_or_decline_request, name="accept_or_decline_request"),
    path('<int:user_id>/tutor_student_list/', views.tutor_student_list, name="tutor_student_list"),
    path('<int:user_id>/watch_profile',views.watch_profile,name="watch_profile"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.account_activate, name='activate'),
    url(r'^password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('privacypolicy/', TemplateView.as_view(template_name="tinder/privacy.html"), name='privacy'),
    path('faq/', TemplateView.as_view(template_name="tinder/faq.html"), name='faq'),
    path('aboutus/', TemplateView.as_view(template_name="tinder/aboutus.html"), name='aboutus'),
    path('adddata/', views.add_school_data, name ='adddata'),
    path('<int:user_id>/edit_profile/', views.edit_profile, name="edit_profile"),
]
