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

# -------------------------  ADMIN SIDE ----------------------------- #

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

def manage_house_maids(request):
    maids = House_Maid.objects.all()  # Fetch all house maids from the database
    return render(request, 'admin_temp/manage_house_maids.html', {'maids': maids})

def manage_home_nurses(request):
    nurses = Home_Nurse.objects.all()  # Fetch all home nurses from the database
    return render(request, 'admin_temp/manage_home_nurses.html', {'nurses': nurses})

def manage_plumbers(request):
    plumbers = Plumber.objects.all()  # Fetch all plumbers from the database
    return render(request, 'admin_temp/manage_plumbers.html', {'plumbers': plumbers})

def manage_electrician(request):
    electricians = Electrician.objects.all()  # Fetch all electricians from the database
    return render(request, 'admin_temp/manage_electricians.html', {'electricians': electricians})

def manage_carpenters(request):
    carpenters = Carpenter.objects.all()  # Fetch all carpenters from the database
    return render(request, 'admin_temp/manage_carpenters.html', {'carpenters': carpenters})

def edit_house_maid(request, maid_id):
    maid = get_object_or_404(House_Maid, pk=maid_id)
    user = get_object_or_404(Users, user_id=maid.user_id.user_id)

    if request.method == 'POST':
        # Retrieve data from the form
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        phone = request.POST.get('phone', '')
        experience = request.POST.get('experience', '')
        availability = request.POST.get('availability') == '1'  # Convert to boolean

        # Update House_Maid fields
        maid.firstname = firstname
        maid.lastname = lastname
        maid.phone = phone
        maid.experience = experience
        maid.availability = availability
        maid.save()

        # Update Users table fields
        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone
        user.availability = availability
        user.save()

        return redirect('manage_house_maids')

    return render(request, 'admin_temp/edit_house_maid.html', {'maid': maid})

def edit_home_nurse(request, nurse_id):
    nurse = get_object_or_404(Home_Nurse, pk=nurse_id)
    user = get_object_or_404(Users, user_id=nurse.user_id.user_id)

    if request.method == 'POST':
        # Retrieve data from the form
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        phone = request.POST.get('phone', '')
        experience = request.POST.get('experience', '')
        availability = request.POST.get('availability') == '1'  # Convert to boolean

        # Update Home_Nurse fields
        nurse.firstname = firstname
        nurse.lastname = lastname
        nurse.phone = phone
        nurse.experience = experience
        nurse.availability = availability
        nurse.save()

        # Update Users table fields
        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone
        user.availability = availability
        user.save()

        return redirect('manage_home_nurses')  # Redirect to the manage_home_nurses view

    return render(request, 'admin_temp/edit_home_nurses.html', {'nurse': nurse})

def edit_electrician(request, electrician_id):
    electrician = get_object_or_404(Electrician, pk=electrician_id)
    user = get_object_or_404(Users, user_id=electrician.user_id.user_id)

    if request.method == 'POST':
        # Retrieve data from the form
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        phone = request.POST.get('phone', '')
        experience = request.POST.get('experience', '')
        availability = request.POST.get('availability') == '1'  # Convert to boolean

        # Update Electrician fields
        electrician.firstname = firstname
        electrician.lastname = lastname
        electrician.phone = phone
        electrician.experience = experience
        electrician.availability = availability
        electrician.save()

        # Update Users table fields
        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone
        user.availability = availability
        user.save()

        return redirect('manage_electricians')  # Redirect to the manage_electricians view

    return render(request, 'admin_temp/edit_electricians.html', {'electrician': electrician})

def edit_plumber(request, plumber_id):
    plumber = get_object_or_404(Plumber, pk=plumber_id)
    user = get_object_or_404(Users, user_id=plumber.user_id.user_id)

    if request.method == 'POST':
        # Retrieve data from the form
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        phone = request.POST.get('phone', '')
        experience = request.POST.get('experience', '')
        availability = request.POST.get('availability') == '1'  # Convert to boolean

        # Update Plumber fields
        plumber.firstname = firstname
        plumber.lastname = lastname
        plumber.phone = phone
        plumber.experience = experience
        plumber.availability = availability
        plumber.save()

        # Update Users table fields
        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone
        user.availability=availability
        user.save()

        return redirect('manage_plumbers')  # Redirect to the manage_plumbers view

    return render(request, 'admin_temp/edit_plumbers.html', {'plumber': plumber})


def edit_carpenter(request, carpenter_id):
    carpenter = get_object_or_404(Carpenter, pk=carpenter_id)
    user = get_object_or_404(Users, user_id=carpenter.user_id.user_id)

    if request.method == 'POST':
        # Retrieve data from the form
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        phone = request.POST.get('phone', '')
        experience = request.POST.get('experience', '')
        availability = request.POST.get('availability') == '1'  # Convert to boolean

        # Update Carpenter fields
        carpenter.firstname = firstname
        carpenter.lastname = lastname
        carpenter.phone = phone
        carpenter.experience = experience
        carpenter.availability = availability
        carpenter.save()

        # Update Users table fields
        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone
        user.availability = availability
        user.save()

        return redirect('manage_carpenters')  # Redirect to the manage_carpenters view

    return render(request, 'admin_temp/edit_carpenters.html', {'carpenter': carpenter})

def change_status(request, user_id):
    customer = get_object_or_404(Users, user_id=user_id, usertype='customer')
    # Toggle the availability status
    customer.availability = not customer.availability
    customer.save()
    return redirect('manage_customers')

def change_booking_status(request, booking_id):
    # Get the booking instance by id
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Define the status order you want to cycle through
    status_order = ['Pending', 'Confirmed', 'Completed', 'Cancelled']
    
    # Find the current status index and determine the next status
    current_index = status_order.index(booking.status)
    next_index = (current_index + 1) % len(status_order)
    
    # Update the booking status
    booking.status = status_order[next_index]
    booking.save()
    
    # Redirect back to the page displaying the bookings
    return redirect('new_bookings')  # Change 'new_bookings' to the correct view name



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Plumber, Users, Skill
from django.core.files.storage import default_storage

def add_plumber(request):
    if request.method == 'POST':
        print("Received POST request")

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')
        availability = request.POST.get('availability')
        place = request.POST.get('place')
        district = request.POST.get('district')
        address = request.POST.get('address')
        profilepic = request.FILES.get('profilepic')
        skill_id = request.POST.get('skill_id')

        print(f"Form data received: firstname={firstname}, lastname={lastname}, email={email}, phone={phone}, experience={experience}, availability={availability}, place={place}, district={district}, address={address}, skill_id={skill_id}, profilepic={profilepic}")

        # Basic validation
        if not (firstname and lastname and email and phone and experience and availability and skill_id):
            print("Validation failed: Missing required fields")
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'admin_temp/add_plumber.html', {'skills': Skill.objects.all()})

        if len(phone) != 10 or not phone.isdigit():
            print("Validation failed: Invalid phone number")
            messages.error(request, 'Phone number must be exactly 10 digits.')
            return render(request, 'admin_temp/add_plumber.html', {'skills': Skill.objects.all()})

        if not (1 <= int(experience) <= 35):
            print("Validation failed: Experience out of range")
            messages.error(request, 'Experience must be between 1 and 35 years.')
            return render(request, 'admin_temp/add_plumber.html', {'skills': Skill.objects.all()})

        # Create a new user
        try:
            print("Creating new user")
            user = Users.objects.create(
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                district=district,
                place=place,
                address=address,
                password='defaultpassword',  # Use a default password or handle this securely
                usertype='plumber'  # Set appropriate usertype
            )
            print(f"User created with user_id={user.user_id}")
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, 'An error occurred while creating the user.')
            return render(request, 'admin_temp/add_plumber.html', {'skills': Skill.objects.all()})

        try:
            skill = Skill.objects.get(skill_id=skill_id)
            print(f"Skill fetched: {skill}")
        except Skill.DoesNotExist:
            print("Validation failed: Skill does not exist")
            messages.error(request, 'Invalid skill selected.')
            return render(request, 'admin_temp/add_plumber.html', {'skills': Skill.objects.all()})

        # Save the new plumber with the created user's user_id as a foreign key
        try:
            print("Creating new plumber entry")
            Plumber.objects.create(
                user_id=user,
                skill_id=skill,
                experience=experience,
                availability=availability,
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                place=place,
                district=district,
                address=address,
                profilepic=profilepic
            )
            print("Plumber created successfully")
        except Exception as e:
            print(f"Error creating plumber: {e}")
            messages.error(request, 'An error occurred while creating the plumber.')
            return render(request, 'admin_temp/add_plumber.html', {'skills': Skill.objects.all()})

        messages.success(request, 'Plumber added successfully!')
        return redirect('manage_plumbers')  # Redirect to a relevant page

    else:
        print("Received GET request")
        skills = Skill.objects.all()
        print(f"Skills fetched: {skills}")
        return render(request, 'admin_temp/add_plumber.html', {'skills': skills})

def add_electrician(request):
    if request.method == 'POST':
        print("Received POST request")

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')
        availability = request.POST.get('availability')
        place = request.POST.get('place')
        district = request.POST.get('district')
        address = request.POST.get('address')
        profilepic = request.FILES.get('profilepic')
        skill_id = request.POST.get('skill_id')

        print(f"Form data received: firstname={firstname}, lastname={lastname}, email={email}, phone={phone}, experience={experience}, availability={availability}, place={place}, district={district}, address={address}, skill_id={skill_id}, profilepic={profilepic}")

        # Basic validation
        if not (firstname and lastname and email and phone and experience and availability and skill_id):
            print("Validation failed: Missing required fields")
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'admin_temp/add_electrician.html', {'skills': Skill.objects.all()})

        if len(phone) != 10 or not phone.isdigit():
            print("Validation failed: Invalid phone number")
            messages.error(request, 'Phone number must be exactly 10 digits.')
            return render(request, 'admin_temp/add_electrician.html', {'skills': Skill.objects.all()})

        if not (1 <= int(experience) <= 35):
            print("Validation failed: Experience out of range")
            messages.error(request, 'Experience must be between 1 and 35 years.')
            return render(request, 'admin_temp/add_electrician.html', {'skills': Skill.objects.all()})

        # Create a new user
        try:
            print("Creating new user")
            user = Users.objects.create(
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                district=district,
                place=place,
                address=address,
                password='defaultpassword',  # Use a default password or handle this securely
                usertype='electrician'  # Set appropriate usertype
            )
            print(f"User created with user_id={user.user_id}")
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, 'An error occurred while creating the user.')
            return render(request, 'admin_temp/add_electrician.html', {'skills': Skill.objects.all()})

        try:
            skill = Skill.objects.get(skill_id=skill_id)
            print(f"Skill fetched: {skill}")
        except Skill.DoesNotExist:
            print("Validation failed: Skill does not exist")
            messages.error(request, 'Invalid skill selected.')
            return render(request, 'admin_temp/add_electrician.html', {'skills': Skill.objects.all()})

        # Save the new electrician with the created user's user_id as a foreign key
        try:
            print("Creating new electrician entry")
            Electrician.objects.create(
                user_id=user,
                skill_id=skill,
                experience=experience,
                availability=availability,
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                place=place,
                district=district,
                address=address,
                profilepic=profilepic
            )
            print("Electrician created successfully")
        except Exception as e:
            print(f"Error creating electrician: {e}")
            messages.error(request, 'An error occurred while creating the electrician.')
            return render(request, 'admin_temp/add_electrician.html', {'skills': Skill.objects.all()})

        messages.success(request, 'Electrician added successfully!')
        return redirect('manage_electricians')  # Redirect to a relevant page

    else:
        print("Received GET request")
        skills = Skill.objects.all()
        print(f"Skills fetched: {skills}")
        return render(request, 'admin_temp/add_electrician.html', {'skills': skills})

def add_house_maid(request):
    if request.method == 'POST':
        print("Received POST request")

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')
        availability = request.POST.get('availability')
        place = request.POST.get('place')
        district = request.POST.get('district')
        address = request.POST.get('address')
        profilepic = request.FILES.get('profilepic')
        skill_id = request.POST.get('skill_id')

        print(f"Form data received: firstname={firstname}, lastname={lastname}, email={email}, phone={phone}, experience={experience}, availability={availability}, place={place}, district={district}, address={address}, skill_id={skill_id}, profilepic={profilepic}")

        # Basic validation
        if not (firstname and lastname and email and phone and experience and availability and skill_id):
            print("Validation failed: Missing required fields")
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'admin_temp/add_house_maid.html', {'skills': Skill.objects.all()})

        if len(phone) != 10 or not phone.isdigit():
            print("Validation failed: Invalid phone number")
            messages.error(request, 'Phone number must be exactly 10 digits.')
            return render(request, 'admin_temp/add_house_maid.html', {'skills': Skill.objects.all()})

        if not (1 <= int(experience) <= 35):
            print("Validation failed: Experience out of range")
            messages.error(request, 'Experience must be between 1 and 35 years.')
            return render(request, 'admin_temp/add_house_maid.html', {'skills': Skill.objects.all()})

        # Create a new user
        try:
            print("Creating new user")
            user = Users.objects.create(
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                district=district,
                place=place,
                address=address,
                password='defaultpassword',  # Use a default password or handle this securely
                usertype='house_maid'  # Set appropriate usertype
            )
            print(f"User created with user_id={user.user_id}")
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, 'An error occurred while creating the user.')
            return render(request, 'admin_temp/add_house_maid.html', {'skills': Skill.objects.all()})

        # Fetch the skill object using the skill_id
        try:
            skill_id = int(skill_id)  # Ensure skill_id is an integer
            print(f"Skill ID to be fetched: {skill_id}")
            skill = Skill.objects.get(skill_id=skill_id)
            print(f"Skill fetched: {skill}")
        except Skill.DoesNotExist:
            print("Validation failed: Skill does not exist")
            messages.error(request, 'Invalid skill selected.')
            return render(request, 'admin_temp/add_house_maid.html', {'skills': Skill.objects.all()})
        except ValueError:
            print("Validation failed: Invalid skill_id format")
            messages.error(request, 'Invalid skill ID format.')
            return render(request, 'admin_temp/add_house_maid.html', {'skills': Skill.objects.all()})

        # Save the new house maid with the created user's user_id as a foreign key
        try:
            print("Creating new house maid entry")
            House_Maid.objects.create(
                user_id=user,
                skill_id=skill,  # Pass the Skill object
                experience=experience,
                availability=availability,
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                place=place,
                district=district,
                address=address,
                profilepic=profilepic
            )
            print("House Maid created successfully")
        except Exception as e:
            print(f"Error creating house maid: {e}")
            messages.error(request, 'An error occurred while creating the house maid.')
            return render(request, 'admin_temp/add_house_maid.html', {'skills': Skill.objects.all()})

        messages.success(request, 'House Maid added successfully!')
        return redirect('manage_house_maids')  # Redirect to a relevant page

    else:
        print("Received GET request")
        skills = Skill.objects.all()
        print(f"Skills fetched: {skills}")
        return render(request, 'admin_temp/add_house_maid.html', {'skills': skills})


def add_home_nurse(request):
    if request.method == 'POST':
        print("Received POST request")

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')
        availability = request.POST.get('availability')
        place = request.POST.get('place')
        district = request.POST.get('district')
        address = request.POST.get('address')
        profilepic = request.FILES.get('profilepic')
        skill_id = request.POST.get('skill_id')

        print(f"Form data received: firstname={firstname}, lastname={lastname}, email={email}, phone={phone}, experience={experience}, availability={availability}, place={place}, district={district}, address={address}, skill_id={skill_id}, profilepic={profilepic}")

        # Basic validation
        if not (firstname and lastname and email and phone and experience and availability and skill_id):
            print("Validation failed: Missing required fields")
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'admin_temp/add_home_nurse.html', {'skills': Skill.objects.all()})

        if len(phone) != 10 or not phone.isdigit():
            print("Validation failed: Invalid phone number")
            messages.error(request, 'Phone number must be exactly 10 digits.')
            return render(request, 'admin_temp/add_home_nurse.html', {'skills': Skill.objects.all()})

        if not (1 <= int(experience) <= 35):
            print("Validation failed: Experience out of range")
            messages.error(request, 'Experience must be between 1 and 35 years.')
            return render(request, 'admin_temp/add_home_nurse.html', {'skills': Skill.objects.all()})

        # Create a new user
        try:
            print("Creating new user")
            user = Users.objects.create(
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                district=district,
                place=place,
                address=address,
                password='defaultpassword',  # Use a default password or handle this securely
                usertype='home_nurse'  # Set appropriate usertype
            )
            print(f"User created with user_id={user.user_id}")
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, 'An error occurred while creating the user.')
            return render(request, 'admin_temp/add_home_nurse.html', {'skills': Skill.objects.all()})

        try:
            skill = Skill.objects.get(skill_id=skill_id)
            print(f"Skill fetched: {skill}")
        except Skill.DoesNotExist:
            print("Validation failed: Skill does not exist")
            messages.error(request, 'Invalid skill selected.')
            return render(request, 'admin_temp/add_home_nurse.html', {'skills': Skill.objects.all()})

        # Save the new home nurse with the created user's user_id as a foreign key
        try:
            print("Creating new home nurse entry")
            Home_Nurse.objects.create(
                user_id=user,
                skill_id=skill,
                experience=experience,
                availability=availability,
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                place=place,
                district=district,
                address=address,
                profilepic=profilepic
            )
            print("Home nurse created successfully")
        except Exception as e:
            print(f"Error creating home nurse: {e}")
            messages.error(request, 'An error occurred while creating the home nurse.')
            return render(request, 'admin_temp/add_home_nurse.html', {'skills': Skill.objects.all()})

        messages.success(request, 'Home nurse added successfully!')
        return redirect('manage_home_nurses')  # Redirect to a relevant page

    else:
        print("Received GET request")
        skills = Skill.objects.all()
        print(f"Skills fetched: {skills}")
        return render(request, 'admin_temp/add_home_nurse.html', {'skills': skills})

def add_carpenter(request):
    if request.method == 'POST':
        print("Received POST request")

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')
        availability = request.POST.get('availability')
        place = request.POST.get('place')
        district = request.POST.get('district')
        address = request.POST.get('address')
        profilepic = request.FILES.get('profilepic')
        skill_id = request.POST.get('skill_id')

        print(f"Form data received: firstname={firstname}, lastname={lastname}, email={email}, phone={phone}, experience={experience}, availability={availability}, place={place}, district={district}, address={address}, skill_id={skill_id}, profilepic={profilepic}")

        # Basic validation
        if not (firstname and lastname and email and phone and experience and availability and skill_id):
            print("Validation failed: Missing required fields")
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'admin_temp/add_carpenter.html', {'skills': Skill.objects.all()})

        if len(phone) != 10 or not phone.isdigit():
            print("Validation failed: Invalid phone number")
            messages.error(request, 'Phone number must be exactly 10 digits.')
            return render(request, 'admin_temp/add_carpenter.html', {'skills': Skill.objects.all()})

        if not (1 <= int(experience) <= 35):
            print("Validation failed: Experience out of range")
            messages.error(request, 'Experience must be between 1 and 35 years.')
            return render(request, 'admin_temp/add_carpenter.html', {'skills': Skill.objects.all()})

        # Create a new user
        try:
            print("Creating new user")
            user = Users.objects.create(
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                district=district,
                place=place,
                address=address,
                password='defaultpassword',  # Use a default password or handle this securely
                usertype='carpenter'  # Set appropriate usertype
            )
            print(f"User created with user_id={user.user_id}")
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, 'An error occurred while creating the user.')
            return render(request, 'admin_temp/add_carpenter.html', {'skills': Skill.objects.all()})

        try:
            skill = Skill.objects.get(skill_id=skill_id)
            print(f"Skill fetched: {skill}")
        except Skill.DoesNotExist:
            print("Validation failed: Skill does not exist")
            messages.error(request, 'Invalid skill selected.')
            return render(request, 'admin_temp/add_carpenter.html', {'skills': Skill.objects.all()})

        # Save the new carpenter with the created user's user_id as a foreign key
        try:
            print("Creating new carpenter entry")
            Carpenter.objects.create(
                user_id=user,
                skill_id=skill,
                experience=experience,
                availability=availability,
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                place=place,
                district=district,
                address=address,
                profilepic=profilepic
            )
            print("Carpenter created successfully")
        except Exception as e:
            print(f"Error creating carpenter: {e}")
            messages.error(request, 'An error occurred while creating the carpenter.')
            return render(request, 'admin_temp/add_carpenter.html', {'skills': Skill.objects.all()})

        messages.success(request, 'Carpenter added successfully!')
        return redirect('manage_carpenters')  # Redirect to a relevant page

    else:
        print("Received GET request")
        skills = Skill.objects.all()
        print(f"Skills fetched: {skills}")
        return render(request, 'admin_temp/add_carpenter.html', {'skills': skills})

def Full_usersPage(request):
    users = Users.objects.all() 
    return render(request, 'admin_temp/full_users.html', {'users': users})

def Full_customersPage(request):
    customers = Users.objects.filter(usertype='customer')  
    return render(request, 'admin_temp/full_customers.html', {'customers': customers})

def Full_workersPage(request):
    workers = Users.objects.exclude(usertype='customer') 
    return render(request, 'admin_temp/full_workers.html', {'workers': workers})

def new_bookings(request):
    # Retrieve all bookings
    bookings = Booking.objects.all()
    
    # Pass the bookings to the template
    context = {
        'bookings': bookings
    }
    
    return render(request, 'admin_temp/new_bookings.html', context)


# -------------------------  CUSTOMER SIDE ----------------------------- #

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