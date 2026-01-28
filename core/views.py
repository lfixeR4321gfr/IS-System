

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
from .models import Tour, Booking


# -----------------------------
# HOME PAGE
# -----------------------------
def home(request):
    tours = Tour.objects.all()
    return render(request, 'core/home.html', {'tours': tours})


# -----------------------------
# REGISTER (Create user)
# -----------------------------
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # IMPORTANT: tumia email kama username
            user.username = user.email
            user.set_password(form.cleaned_data['password'])

            user.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'core/register.html', {'form': form})


# -----------------------------
# LOGIN (EMAIL + PASSWORD)
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Password sio sahihi')

        except User.DoesNotExist:
            messages.error(request, 'Email haijasajiliwa')

    return render(request, 'core/login.html')


# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect('home')


# -----------------------------
# BOOK TOUR
# -----------------------------
@login_required
def booking_view(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        Booking.objects.create(
            user=request.user,
            tour=tour
        )
        messages.success(request, 'Booking successful!')
        return redirect('dashboard')

    return render(request, 'core/booking.html', {'tour': tour})


# -----------------------------
# CLIENT DASHBOARD
# -----------------------------
@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'core/dashboard.html', {'bookings': bookings})











"""



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


######################

username = request.POST['username']



###################

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # au dashboard ya client
            else:
                messages.error(request, 'Password sio sahihi')

        except User.DoesNotExist:
            messages.error(request, 'Email haijasajiliwa')

    return render(request, 'core/login.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Tour, Booking



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('check_profile')
    return render(request, 'core/login.html')






# -----------------------------
# Home view
# -----------------------------
def home(request):
    tours = Tour.objects.all()  # show all available tours
    return render(request, 'core/home.html', {'tours': tours})

# -----------------------------
# User Registration
# -----------------------------
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set the password properly
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

# -----------------------------
# User Login
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')

# -----------------------------
# User Logout
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect('home')

# -----------------------------
# Booking view
# -----------------------------
@login_required
def booking_view(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        Booking.objects.create(
            user=request.user,
            tour=tour
        )
        messages.success(request, f'Booking confirmed for {tour.name}!')
        return redirect('home')

    return render(request, 'core/booking.html', {'tour': tour})

# -----------------------------
# Optional: User dashboard
# -----------------------------
@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'core/dashboard.html', {'bookings': bookings})



"""