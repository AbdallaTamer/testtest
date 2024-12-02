from django.shortcuts import render , redirect
from django.urls import reverse
from supabase import create_client, Client
from django.contrib.auth.hashers import make_password,check_password
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from functools import wraps


url: str = "https://sodghnhticinsggmbber.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvZGdobmh0aWNpbnNnZ21iYmVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIyODY5MzMsImV4cCI6MjA0Nzg2MjkzM30.dCfS98X9PFoZpBohhf0UdgSvvcwByOlAPki7-BPlExg"
supabase: Client = create_client(url, key)
#for admin
def get_Memberships():
    return supabase.table("memberships").select("*").execute().data

#for admin
def get_Profiles():
    return supabase.table("profiles").select("*").execute().data

def get_Users():
    return supabase.table("users").select("*").execute().data


def logout_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect('profiles')  
        return view_func(request, *args, **kwargs)
    return wrapper

@logout_required
def signup(request):
    print('I AM IN THE SIGN UPUPUPUP')
    print(json.loads(request.body))
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            phone_number = data.get('phoneNumber')
            account_type = data.get('type')
            password = data.get('password')

            user_data = {
                'name': name,
                'email': email,
                'phone_number': phone_number,
                'account_type': account_type,
                'password': make_password(password)
            }
            print('User data: ', user_data)
            
            supabase.table('users').insert(user_data).execute()

            return JsonResponse({'message': 'User registered successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@logout_required
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Check user in Supabase
            response = supabase.table('users').select('*').eq('email', email).execute()
            if response.data:
                user_data = response.data[0]
                print(user_data)
                stored_password = user_data['password']

                if check_password(password, stored_password):
                    request.session['user_id'] = user_data['user_id']
                    print('User ID inside login function: ', user_data['user_id'])
                    # Create or retrieve the Django user object
                    user, created = User.objects.get_or_create(username=user_data['email'])
                    if created:
                        user.set_unusable_password()
                        user.save()

                    # Specify the backend explicitly
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    
                    # Log the user in
                    auth_login(request, user)
                    
                    print('I LOGGED IN')

                    return JsonResponse({'success': True, 'redirect_url': reverse('profiles')})
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            print(f"Error during login: {e}")
            return JsonResponse({'success': False, 'error': 'An error occurred'}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    

def get_user(userid):
    response = supabase.table("countries").select("id, name, cities(name)").\
    join("cities", "countries.id", "cities.country_id").execute()

@login_required
def profile_view(request):
    print('I AM IN PROOFIFLEE  VIEW')
    print(request.session.items())
    user_id = request.session.get('user_id')
    print('User ID: ', user_id)
    if user_id:
        print('User ID: ', user_id)
        return render(request, 'profile/information.html')  
    else:
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')


def change_Password(request):
    id = request.session.get('user_id')  
    response = supabase.table('users').select('*').eq('user_id', id).execute()
    
    if request.method == 'POST':
        data = json.loads(request.body)
        old = data.get('password')
        new = data.get('new_password')
        
        if response.data:
            user = response.data[0]
            stored_password = user['password']

            print(stored_password)
            print(old)
            if check_password(old, stored_password):
                hashed_new_password = make_password(new)
                update_response = supabase.table('users').update({'password': hashed_new_password}).eq('user_id', id).execute()

                if update_response.status_code == 200:
                    return JsonResponse({'success': True })
                else:
                    return JsonResponse({'success': False, 'error': 'cant update password'}, status=500)
            else:
                return JsonResponse({'success': False, 'error': 'Old password isnt correct'}, status=500)
        else:
            return JsonResponse({'success': False, 'error': 'User not found.'}, status=500)
def change_data(request):
    id = request.session.get('user_id')
    data = json.loads(request.body)
    response = supabase.table('users').select('*').eq('user_id', id).execute()
    user_data = response.data[0]

    if request.method == 'POST':
        if response.data:
            userName = data.get('username', user_data["name"])
            contactInfo = data.get('contactinfo', user_data["phone_number"])
            email = data.get('email', user_data["email"]) 
            update_response = supabase.table('users').update({'username':userName ,'contactinfo':contactInfo,'email':email}).eq('user_id', id).execute()
            if update_response.status_code == 200:
                return JsonResponse({'success': True })
        else:
            return JsonResponse({'success': False, 'error': 'User not found.'}, status=500)
        

@login_required 
def logout_view(request):
    request.session.flush()
    print("User logged out")
    return redirect('login')