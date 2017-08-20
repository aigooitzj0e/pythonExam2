from django.shortcuts import render, redirect
from .models import User, Item
from django.contrib import messages

#create views here
def index(request):
    return render(request, "PE2_app/index.html")

def reg_process(request):
    errors = User.objects.registration_validator(request.POST)
    if type(errors) == dict:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    request.session['user_id'] = errors
    return redirect('/dashboard')

def dashboard(request):
    try: #checks is user is logged in.
        request.session['user_id']
    except:
        return redirect('/')

    context = {
        "users": User.objects.all(),
        "wishes": Item.objects.all(),
        "welcome": User.objects.get(id = request.session['user_id']),
        "mywish": Item.objects.filter(users__id = request.session['user_id']),
        'allitems': Item.objects.filter(all_users__id=request.session['user_id']),
        }

    return render(request, "PE2_app/dashboard.html", context)

def login_process(request):
    errors = User.objects.login_validator(request.POST)
    if type(errors) == dict:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    request.session['user_id'] = errors
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')


def additem(request):
    return render(request, "PE2_app/additem.html")

def additem_process(request):
    errors = Item.objects.item_validation(request.POST, request.session['user_id'])
    if type(errors) == dict:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/additem')
    request.session['item_id'] = errors
    return redirect('/dashboard')

def delete(request, iid):
    delete = Item.objects.get(id = iid)
    delete.delete()

    return redirect('/dashboard')

def remove(request, iid):
    remove = Item.objects.remove_validation(request.POST, iid, request.session['user_id'])
    return redirect('/dashboard')

def show(request, iid):
    context = {
        "items": Item.objects.get(id = iid),
        "others": User.objects.filter(all_items__id = iid)
    }
    return render(request, "PE2_app/show.html", context)

def join(request, iid):
    errors = Item.objects.join_validation(request.POST, iid, request.session['user_id'])
    return redirect('/dashboard')
