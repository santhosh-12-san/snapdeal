# apps/users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import PhoneOTP, Address
from .utils import generate_and_send_otp 

User = get_user_model()

# --- 1. LOGIN VIEW ---
def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('mobile_or_username')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type') 
        
        # If user clicked "Login with OTP"
        if login_type == 'otp':
            return verify_otp_login(request)
        
        # Standard Password Login
        target_user = None
        
        # Check Mobile Number
        if not target_user:
            try:
                user_obj = User.objects.get(mobile_number=identifier)
                if user_obj.check_password(password): target_user = user_obj
            except User.DoesNotExist:
                pass

        # Check Secondary Mobile (if you have this field)
        if not target_user:
            try:
                user_obj = User.objects.get(mobile=identifier)
                if user_obj.check_password(password): target_user = user_obj
            except User.DoesNotExist:
                pass
        
        # Check Username
        if not target_user:
            try:
                user_obj = User.objects.get(username=identifier)
                if user_obj.check_password(password): target_user = user_obj
            except User.DoesNotExist:
                pass

        if target_user:
            login(request, target_user)
            messages.success(request, f"Welcome back!")
            return redirect('core:home')
        else:
            messages.error(request, "Invalid Credentials.")

    return render(request, 'users/login.html')


# --- 2. SEND OTP ---
@csrf_exempt 
def send_otp_view(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        if not mobile:
            return JsonResponse({'status': False, 'message': 'Mobile number required'})
        
        try:
            generate_and_send_otp(mobile)
            return JsonResponse({'status': True, 'message': 'OTP Sent Successfully!'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})

    return JsonResponse({'status': False, 'message': 'Invalid Request'})


# --- 3. VERIFY OTP ---
def verify_otp_login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile_or_username')
        otp_input = request.POST.get('otp_code')
        
        try:
            otp_obj = PhoneOTP.objects.get(mobile_number=mobile, otp=otp_input)
            
            try:
                user = User.objects.get(mobile_number=mobile)
                login(request, user)
                
                otp_obj.validated = True
                otp_obj.save()
                
                messages.success(request, "Logged in via OTP!")
                return redirect('core:home')
                
            except User.DoesNotExist:
                messages.error(request, "No account found. Please Register.")
                return redirect('users:register')
                
        except PhoneOTP.DoesNotExist:
            messages.error(request, "Invalid OTP.")
            
    return redirect('users:login')


# --- 4. REGISTER ---
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(mobile_number=mobile).exists():
            messages.error(request, "Mobile Number already registered.")
            return redirect('users:login')

        try:
            # FIX: Pass mobile_number correctly during creation
            new_user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                mobile_number=mobile 
            )
            login(request, new_user)
            messages.success(request, "Account Created!")
            return redirect('core:home')
            
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect('users:register')

    return render(request, 'users/register.html')


# --- 5. LOGOUT ---
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect('core:home')


# --- 6. ADD ADDRESS ---
@login_required
def add_address(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            mobile=request.POST.get('mobile'),
            pincode=request.POST.get('pincode'),
            locality=request.POST.get('locality'),
            address_line = request.POST.get('address_line'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            address_type=request.POST.get('address_type', 'Home')
        )
        
        messages.success(request, "Address Added!")
        
        # If user came from Checkout, send them back to selection
        next_page = request.GET.get('next')
        if next_page:
            return redirect(next_page)
            
        return redirect('users:address_book')
        
    return render(request, 'users/add_address.html')


# --- 7. ADDRESS BOOK ---
@login_required
def address_book(request):
    user_addresses = Address.objects.filter(user=request.user)
    return render(request, 'users/address_book.html', {'addresses': user_addresses})


# --- 8. CHECK USER EXISTS (AJAX) ---
def check_user_exists(request):
    mobile = request.GET.get('mobile')
    if not mobile:
        return JsonResponse({'exists': False})
    
    exists = User.objects.filter(mobile_number=mobile).exists()
    return JsonResponse({'exists': exists})


# --- 9. EDIT ADDRESS ---
@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        address.name = request.POST.get('name')
        address.mobile = request.POST.get('mobile')
        address.pincode = request.POST.get('pincode')
        address.locality = request.POST.get('locality')
        address.address_line = request.POST.get('address_line') or request.POST.get('address')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.address_type = request.POST.get('address_type')
        
        address.save()
        return redirect('orders:checkout')

    return render(request, 'users/add_address.html', {'address': address})


# --- 10. SELECT ADDRESS (Checkout Step 2) ---
@login_required
def select_address(request):
    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # 1. Try to get selected ID
        selected_address_id = request.POST.get('selected_address')

        # 2. AUTO-SELECT FIX: If user didn't select, pick the first one
        if not selected_address_id and addresses.exists():
            selected_address_id = addresses.first().id

        # 3. If we have a valid ID, Save & Redirect
        if selected_address_id:
            request.session['shipping_address_id'] = selected_address_id
            return redirect('orders:payment')
        else:
            messages.error(request, "Please add an address first.")
            return redirect('users:add_address')

    return render(request, 'users/select_address.html', {'addresses': addresses})