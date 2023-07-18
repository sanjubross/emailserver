from django.contrib import admin
from django.urls import path, include
# froala editor
from froala_editor import views
# home views
from mailhome import views

# static root urls
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('froala_editor/',include('froala_editor.urls')),
    path('', views.mail_home, name="mailhome"),
    path('sent-mail', views.sent_mail, name="sentmail"),

    # credentials url
    path('s/login', views.login_attempt, name="login"),
    path('signout', views.signout, name="signout"),

    # send mail url
    path('external', views.mail_send, name="mail_send"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
