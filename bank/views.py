import random, string, re
from django.shortcuts import render, HttpResponse, redirect
from .models import Balance, PersonalDetails, Transactions_history
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def generate_unique_customer_id():
    # Generate a random 6-character alphanumeric customer_id
    while True:
        customer_id = ''.join(random.choices(
            string.ascii_letters + string.digits, k=6))
        if not User.objects.filter(username=customer_id).exists():
            return customer_id

def contains_alphanumeric_special(input_str):
    pattern = r'^[A-Za-z0-9@#$%^&+=]*$'
    return bool(re.match(pattern, input_str))

def check(s):
    for i in range(len(s)):
        if s[i] > '9' or s[i] < '0':
            return False
    return True

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def handleSignup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        father_name = request.POST['father_name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        country = request.POST['country']
        state = request.POST['state']
        pincode = request.POST['pincode']
        address = request.POST['address']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        customer_id = generate_unique_customer_id()
        account_number = str(1000000000 + Balance.objects.count())

        # checks
        if len(pass1) < 8:
            messages.error(
                request, "Password must be contain at least 8 characters.")
            return redirect('/')
        if pass1 != pass2:
            messages.error(request, "Password do not match.")
            return redirect('/')
        if len(mobile_number) != 10 or not check(mobile_number):
            messages.error(request, "Enter correct Mobile Number")
            return redirect('/')
        if not contains_alphanumeric_special(pass1):
            messages.error(
                request, "Password must contain numbers, alphabets and special characters.")
            return redirect('/')

        # Register the User
        myuser = User.objects.create_user(
            username=customer_id, email=email, password=pass1, first_name=first_name)
        myuser.save()
        myuser = Balance()
        myuser.account_number = account_number
        myuser.balance = 500
        myuser.save()
        myuser = Transactions_history()
        myuser.to_account_number = account_number
        myuser.from_account_number = 'CASH'
        myuser.typee = "CREDIT"
        myuser.amount = 500
        myuser.save()
        myuser = PersonalDetails()
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.father_name = father_name
        myuser.customer_id = customer_id
        myuser.mobile_number = mobile_number
        myuser.country = country
        myuser.state = state
        myuser.pin_code = pincode
        myuser.address = address
        myuser.account_number = account_number
        myuser.save()
        messages.success(
            request, "Your Account has been created successfullly. Please remember you customer id for login purpose.")
        messages.success(request, f'Customer ID: {customer_id}')
        return redirect('/')
    else:
        return HttpResponse("Invalid Access")


def handleLogin(request):
    if request.method == 'POST':
        username = request.POST['customer_id']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully")
        else:
            messages.error(request, "Invalid Credentials, Please try Again")
        return redirect('/')
    else:
        return HttpResponse("Invalid Access")


@login_required
def handleLogout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully.")
    return redirect('/')


@login_required
def profile(request):
    user = User.objects.get(username=request.user)
    details = PersonalDetails.objects.get(customer_id=user.username)
    bal = Balance.objects.get(account_number=details.account_number)
    context = {
        'customer_id': user.username,
        'name': details.first_name + ' ' + details.last_name,
        'father_name': details.father_name,
        'account_number': details.account_number,
        'balance': bal.balance,
        'email': user.email,
        'country': details.country,
        'state': details.state,
        'pincode': details.pin_code,
        'mobile_number': details.mobile_number,
        'address': details.address
    }
    return render(request, 'profile.html', context)


@login_required
def transfer(request):
    if request.method == 'POST':
        recipient_ac = request.POST['account_number']
        amount = request.POST['amount']
        recipient = Balance.objects.filter(account_number=recipient_ac)

        if not recipient.exists():
            messages.error(request, "Recipient does not exist.")
            return render(request, 'transfer.html')

        user = User.objects.get(username=request.user)
        user_details = PersonalDetails.objects.get(customer_id=user.username)
        user_bal = Balance.objects.get(account_number=user_details.account_number)
        recipient = Balance.objects.get(account_number=recipient_ac)

        if user_bal.balance < int(amount):
            messages.error(request, "Insufficient Balance.")
            return render(request, 'transfer.html')

        trans1 = Transactions_history()
        trans1.to_account_number = recipient.account_number
        trans1.from_account_number = user_bal.account_number
        trans1.amount = amount
        trans1.typee = "CREDIT"
        trans1.save()

        trans2 = Transactions_history()
        trans2.to_account_number = user_bal.account_number
        trans2.from_account_number = recipient.account_number
        trans2.amount = amount
        trans2.typee = "DEBIT"
        trans2.save()

        user_bal.balance = user_bal.balance - int(amount)
        user_bal.save()
        recipient = Balance.objects.get(account_number=recipient_ac)
        recipient.balance = recipient.balance + int(amount)
        recipient.save()

        messages.success(request, "Fund transferred successfully")
        return redirect('/history')

    else:
        return render(request, 'transfer.html')


@login_required
def history(request):
    user = User.objects.get(username=request.user)
    details = PersonalDetails.objects.get(customer_id=user.username)
    transactions = Transactions_history.objects.filter(
        to_account_number=details.account_number).order_by('datetime')
    return render(request, 'history.html', {'transactions': transactions, })

@login_required
def update(request):
    if request.method == 'POST':
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        country = request.POST['country']
        state = request.POST['state']
        pincode = request.POST['pincode']
        address = request.POST['address']
        customer_id = request.user

        # checks
        if len(mobile_number) != 10 or not check(mobile_number):
            messages.error(request, "Enter correct Mobile Number")
            return redirect('/profile')

        # Update the User
        myuser = User.objects.get(username=customer_id)
        myuser.email = email
        myuser.save()
        myuser = PersonalDetails.objects.get(customer_id=request.user)
        myuser.mobile_number = mobile_number
        myuser.country = country
        myuser.state = state
        myuser.pin_code = pincode
        myuser.address = address
        myuser.save()
        messages.success(request, "Your Account has been updated successfullly.")
        return redirect('/profile')
    else:
        return HttpResponse("Invalid Access")