from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Users, Items, Wishlists
from django.contrib.auth import logout
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'wishlist/index.html')

def register(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        hired=request.POST['hired']
        print email
        errors = Users.objects.validation(email, password, conf_password, first_name, last_name, username)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/')
        else:
            print ('should be creating a user now...')
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            Users.objects.create(email=email, pw_hash=pw_hash, first_name=first_name, last_name=last_name, username=username, hired=hired)
            messages.success(request, 'You have registered successfully!')
            return redirect('/')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        result = Users.objects.login(username, password)
        if type(result) == list:
            print ('returned result is not object')
            for error in result:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['logged_user'] = result.id
            return redirect('/profile')

def log_out(request):
    current_user = Users.objects.get(id=request.session['logged_user'])
    logout(request)
    return redirect('/')

def profile(request):
    user = Users.objects.filter(id=request.session['logged_user'])
    other_items = Items.objects.exclude(user=user)
    my_items = Wishlists.objects.filter(user=user)
    context={'users':user, 'others':other_items, 'mine':my_items}
    return render(request, 'wishlist/profile.html', context)

def create_item(request):
    return render(request, 'wishlist/create.html')

def create(request):
    if request.method == "POST":
        product = request.POST['product']
        specs=[]
        if len(product) < 3:
            print ('error found')
            specs.append('Please enter item')
            for spec in specs:
                messages.error(request, spec)
            return redirect('/create_item')
        else:
            print ('creating item')
            user = Users.objects.get(id=request.session['logged_user'])
            my_item=Items.objects.create(product=product, user=user)
            print my_item.id
            list_item=Wishlists.objects.create(item=my_item, user=user)
            return redirect('/profile')

# def show_profile(request):
#     user = Users.objects.filter(id=request.session['logged_user'])
#     context={'users':user}
#     my_list=Wishlists.objects.filter(id=id)
#     all_my_items = Wishlists.objects.all()
#     my_items = Items.objects.filter(id=id)
#     context={'my_lists':my_list, 'my_items':my_items, 'all':all_my_items}
#     print my_items
#     return redirect('/profile')

def remove(request, id):
    Wishlists.objects.get(id=id).clear()
    return redirect('/profile')

def delete(request, id):
    Wishlists.objects.filter(id=id).delete()
    return redirect('/profile')

def add_wl(request, id):
    user = Users.objects.get(id=request.session['logged_user'])
    item_id = Items.objects.get(id=id)
    print item_id
    print id
    add_item = Wishlists.objects.create(item=item_id, user=user)
    return redirect('/profile')

def show_item(request, id):
    item = Items.objects.get(id=id)
    context = {'items':item}

    return redirect('/profile', context)








# Create your views here.
