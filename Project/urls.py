from django.contrib import admin
from Home_app import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('admin/', admin.site.urls),
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('index/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('custom_password_reset/', views.custom_password_reset, name='custom_password_reset'),
    path('custom_password_reset_done/', views.custom_password_reset_done, name='custom_password_reset_done'),
    path('custom_password_reset_confirm/<uidb64>/<token>/', views.custom_password_reset_confirm, name='custom_password_reset_confirm'),
    path('social-auth/', include('social_django.urls', namespace='social')),

# admin side start

    path('dashboard/', views.DashboardPage, name='dashboard'),
    path('full_users/', views.Full_usersPage, name='full_users'),
    path('full_customers/', views.Full_customersPage, name='full_customers'),
    path('full_workers/', views.Full_workersPage, name='full_workers'),


# admin side end
    path('update_profile/', views.update_profile, name='update_profile'),
    path('view_maids/', views.view_maids, name='view_maids'),
    path('view_plumbers/', views.view_plumbers, name='view_plumbers'),
    path('view_carpenters/', views.view_carpenters, name='view_carpenters'),
    path('view_electricians/', views.view_electricians, name='view_electricians'),
    path('view_nurses/', views.view_nurses, name='view_nurses'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('book_service/<int:maid_id>/', views.book_service, name='book_service'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)