from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('createanak/', views.createAnak,name='create-anak'),
    path('delete/<str:pk>', views.deleteAnak,name='delete-anak'),
    path('update/<str:pk>', views.updateAnak,name='update-anak'),
    path('dalam_proses/detail>', views.detailAnak_pending,name='detail'),
    path('kosong/detail>', views.detailAnak_kosong,name='kosong'),
    path('selesai/detail>', views.detailAnak_selesai,name='selesai'),

    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/', views.logoutUser,name='logout'),
    path('user/', views.dashboard,name='user-page'),
]
