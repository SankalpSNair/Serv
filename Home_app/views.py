from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logouts

# from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .forms import CustomPasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from .models import Users,House_Maid,Skill,Carpenter,Electrician,Plumber,Home_Nurse,Booking
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
# register, login and logout starts here



# @login_required(login_url='login')
# @login_required(login_url='login')
def DashboardPage(request):
    total_users = Users.objects.count()  # Total number of users
    total_customers = Users.objects.filter(usertype='customer').count()  # Total number of customers
    total_workers = Users.objects.exclude(usertype='customer').count()  # Total number of workers
    total_bookings = Booking.objects.count()  # Total number of bookings
    
    context = {
        'total_users': total_users,
        'total_customers': total_customers,
        'total_workers': total_workers,
        'total_bookings': total_bookings
    }
    
    return render(request, 'admin_temp/dashboard.html', context)

def Manage_Customers(request):
    customers = Users.objects.filter(usertype='customer')  
    return render(request, 'admin_temp/manage_customers.html',{'customers':customers})

def change_status(request, user_id):
    customer = get_object_or_404(Users, user_id=user_id, usertype='customer')
    # Toggle the availability status
    customer.availability = not customer.availability
    customer.save()
    return redirect('manage_customers')

def Full_usersPage(request):
    users = Users.objects.all() 
    return render(request, 'admin_temp/full_users.html', {'users': users})

def Full_customersPage(request):
    customers = Users.objects.filter(usertype='customer')  
    return render(request, 'admin_temp/full_customers.html', {'customers': customers})

def Full_workersPage(request):
    workers = Users.objects.exclude(usertype='customer') 
    return render(request, 'admin_temp/full_workers.html', {'workers': workers})

@never_cache
def HomePage(request):
    user_id = request.session.get('user_id')

    if request.method == 'POST':
        if user_id:
            user = Users.objects.get(user_id=user_id)
            
            # Update user information from the form data
            user.firstname = request.POST.get('first_name')
            user.lastname = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.address = request.POST.get('address')
            
            # Handle profile picture update
            if 'profile_pic' in request.FILES:
                user.image = request.FILES['profile_pic']
            
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('home')

    if user_id:
        try:
            user = Users.objects.get(user_id=user_id)
            context = {
                'first_name': user.firstname,
                'last_name': user.lastname,
                'email': user.email,
                'phone': user.phone,
                'address': user.address,
                'profile_picture_url': user.image.url if user.image else '/media/default_profile_pic.png',
            }
            return render(request, 'index.html', context)
        except Users.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login')
    else:
        messages.warning(request, 'You need to log in first.')
        return redirect('login')





def SignupPage(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_pass = request.POST.get('re_pass')

        if password != re_pass:
            return HttpResponse('Passwords do not match')
        else:
            # Hash the password before saving
            hashed_password = make_password(password)
            
            # Create a new User instance with the provided data
            my_user = Users(
                firstname=fname,
                lastname=lname,
                email=email,
                password=hashed_password,
                usertype='customer'  # Set the default usertype (this can be adjusted as needed)
            )
            my_user.save()
            return redirect('login')
        
    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.user_id
                request.session['user_email'] = user.email
                messages.success(request, 'Login successful')
                print(f"User ID set in session: {request.session.get('user_id')}")
                return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid Credentials')
        
    return render(request, 'login.html')


from django.contrib import messages

def LogoutPage(request):
    logouts(request)
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# register, login and logout ends here

def update_profile(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        try:
            user = Users.objects.get(user_id=user_id)
            user.firstname = request.POST.get('firstname')
            user.lastname = request.POST.get('lastname')
            user.phone = request.POST.get('phone')
            user.address = request.POST.get('address')
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('home')
        except Users.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login')
    else:
        messages.error(request, 'Invalid request.')
        return redirect('home')
# password reset code starts here 

def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                current_site = get_current_site(request)
                mail_subject = 'Reset your password'
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = reverse('custom_password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                reset_url = f"http://{current_site.domain}{reset_link}"
                message = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uidb64': uidb64,
                    'token': token,
                    'reset_url': reset_url
                })
                email_message = EmailMessage(mail_subject, message, 'webmaster@localhost', [email])
                email_message.content_subtype = 'html'
                email_message.send()
                messages.success(request, 'A link to reset your password has been sent to your email.')
                return redirect('custom_password_reset_done')
            except User.DoesNotExist:
                messages.error(request, 'No user is associated with this email address.')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})


def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been set. You can now log in with the new password.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('custom_password_reset')


def custom_password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')



# password reset code ends here



# def view_maids(request):
#     # You can pass any necessary context to the template here
#     return render(request, 'view_maids.html')


def view_maids(request):
    user_id = request.session.get('user_id')

    if user_id:
        # Fetch all House_Maid objects
        maids = House_Maid.objects.all()
        return render(request, 'view_maids.html', {'maids': maids})
    else:
        messages.warning(request, 'You need to log in first.')
        return redirect('login')


def view_plumbers(request):
    user_id = request.session.get('user_id')

    if user_id:
        # Fetch all Plumber objects
        plumbers = Plumber.objects.all()
        return render(request, 'view_plumbers.html', {'plumbers': plumbers})
    else:
        messages.warning(request, 'You need to log in first.')
        return redirect('login')
    
def view_electricians(request):
    user_id = request.session.get('user_id')

    if user_id:
        # Fetch all Electrician objects
        electricians = Electrician.objects.all()
        return render(request, 'view_electricians.html', {'electricians': electricians})
    else:
        messages.warning(request, 'You need to log in first.')
        return redirect('login')

def view_nurses(request):
    user_id = request.session.get('user_id')

    if user_id:
        # Fetch all Home_Nurse objects
        nurses = Home_Nurse.objects.all()
        return render(request, 'view_nurses.html', {'nurses': nurses})
    else:
        messages.warning(request, 'You need to log in first.')
        return redirect('login')

def view_carpenters(request):
    user_id = request.session.get('user_id')

    if user_id:
        # Fetch all Carpenter objects
        carpenters = Carpenter.objects.all()
        return render(request, 'view_carpenters.html', {'carpenters': carpenters})
    else:
        messages.warning(request, 'You need to log in first.')
        return redirect('login')





def view_bookings(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.warning(request, 'You need to log in first.')
        return redirect('login')

    # Fetch all bookings made by the logged-in user
    bookings = Booking.objects.filter(customer_id=user_id)

    context = {
        'bookings': bookings
    }
    return render(request, 'view_booking.html', context)





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Booking, Users

def book_service(request, maid_id):
    user_id = request.session.get('user_id')
    
    # Fetch the maid or return a 404 error if not found
    maid = get_object_or_404(House_Maid, maid_id=maid_id)
    
    # Check if the user is logged in
    if not user_id:
        messages.warning(request, 'You need to log in first.')
        return redirect('login')
    
    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        address = request.POST.get('address')
        
        # Fetch the customer (logged-in user) or return an error if not found
        try:
            customer = Users.objects.get(user_id=user_id)
            
            # Create and save the booking
            booking = Booking(
                worker_id=maid.user_id,  # Use maid's user_id as the worker
                worker_type='House Maid',  # Correct worker type
                customer_id=customer,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                address=address,
                status='Pending'  # Default status
            )
            booking.save()
            
            messages.success(request, 'Booking successfully created!')
            return redirect('view_bookings')
        
        except Users.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('view_maids')
    
    # Provide the maid object to the template for displaying details
    context = {
        'maid': maid
    }
    return render(request, 'registration/book_service.html', context)