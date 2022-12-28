from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
    path('phone_register/<str:uidb64>/<str:token>/', views.PhoneRegister.as_view(), name='phone_register'),
    path('register/email_active/<str:uidb64>/<str:token>/', views.Register.as_view(), name='email_active'),
    path('user_profile_update/', views.user_profile_update, name='user_profile_update'),
    path('ticket_send/', views.ticket_send, name='ticket_send'),
    # mobile verify
    # path('send_code/', views.SendCode.as_view(), name='send_code'),
    path('send_code/', views.send_code, name='send_code'),
    path('verify_code/', views.VerifyCode.as_view(), name='verify_code'),
    # upload_document_url
    path('id_card_upload/', views.id_card_upload, name='id_card_upload'),
    path('bank_card_upload/', views.bank_card_upload, name='bank_card_upload'),
    path('profile_image_upload/', views.profile_image_upload, name='profile_image_upload'),
    # reset password
    path('password_reset_1/', views.ResetPassword.as_view(), name='password_reset_1'),
    path('password_reset_2/<str:uidb64>/<str:token>/', views.ResetPasswordConfirm.as_view(), name='password_reset_2'),
    # notify read
    path('notification_read/', views.ReadNotification.as_view()),

    path('get_admin_inform/', views.admin_page_information)
]
