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
    path('manage_customers/', views.Manage_Customers, name='manage_customers'),
    path('change_status/<int:user_id>/', views.change_status, name='change_status'),
    path('manage_house_maids/', views.manage_house_maids, name='manage_house_maids'),
    path('edit_house_maid/<int:maid_id>/', views.edit_house_maid, name='edit_house_maid'),
    path('manage_home_nurses/', views.manage_home_nurses, name='manage_home_nurses'),
    path('edit_home_nurse/<int:nurse_id>/', views.edit_home_nurse, name='edit_home_nurse'),
    path('manage_carpenters/', views.manage_carpenters, name='manage_carpenters'),
    path('edit_carpenter/<int:carpenter_id>/', views.edit_carpenter, name='edit_carpenter'),
    path('manage_plumbers/', views.manage_plumbers, name='manage_plumbers'),
    path('edit_plumber/<int:plumber_id>/', views.edit_plumber, name='edit_plumber'),
    path('manage_electricians/', views.manage_electrician, name='manage_electricians'),
    path('edit_electrician/<int:electrician_id>/', views.edit_electrician, name='edit_electrician'),
    path('new-bookings/', views.new_bookings, name='new_bookings'),
    path('change-booking-status/<int:booking_id>/', views.change_booking_status, name='change_booking_status'),
    path('add_plumber/', views.add_plumber, name='add_plumber'),
    path('add_carpenter/', views.add_carpenter, name='add_carpenter'),
    path('add_electrician/', views.add_electrician, name='add_electrician'),
    path('add_home_nurse/', views.add_home_nurse, name='add_home_nurse'),
    path('add_house_maid/', views.add_house_maid, name='add_house_maid'),

    

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