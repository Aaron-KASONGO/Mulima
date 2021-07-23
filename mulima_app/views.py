from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Message, Profile
from .forms import PersonForm, LoginForm


def home(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if 'new_message' in request.POST and request.POST['new_message'] != '':
            newMessage = Message(author=logged_user, content=request.POST['new_message'])
            newMessage.save()
        messages = Message.objects.all().order_by('publication_date')
        return render(request, 'mulima_app/home.html',
                      {'logged_user': logged_user, 'all_messages': messages})
    else:
        return redirect('login')


def validate_username(request):
    """Check username availability"""
    username = request.POST.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_username = form.cleaned_data['username']
            logged_user = User.objects.get(username=user_username)
            request.session['logged_user_id'] = logged_user.id
            return redirect('home')
        else:
            return render(request, 'mulima_app/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'mulima_app/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        personForm = PersonForm(request.POST)
        if personForm.is_valid():
            print("ça marche!")
            personForm.save()
            logged_user = User.objects.get(username=personForm.cleaned_data.get('username'))
            request.session['logged_user_id'] = logged_user.id
            return redirect('home')
        else:
            return render(request, 'mulima_app/register.html', {'form': personForm})
        # Le formulaire envoyé n'est pas valide
    personForm = PersonForm()
    return render(request, 'mulima_app/register.html', {'form': personForm})


def get_logged_user_from_request(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']

        if len(User.objects.filter(id=logged_user_id)) == 1:
            return User.objects.get(id=logged_user_id)
        else:
            return None
    else:
        return None


def friends(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        users = User.objects.exclude(username=logged_user.username)
        return render(request, 'mulima_app/friends.html', {'logged_user': logged_user, 'users': users})
    else:
        return redirect('/login')


def add_friends(request, id):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        friend = get_object_or_404(Profile, user=User.objects.get(pk=id))
        # Test if the form is shared
        logged_user.profile.friends.add(friend)
        logged_user.save()
        return redirect('friends')

    else:
        return redirect('/login')


def remove_friends(request, id):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        friend = get_object_or_404(Profile, user=User.objects.get(pk=id))
        # Test if the form is shared
        logged_user.profile.friends.remove(friend)
        logged_user.save()
        return redirect('friends')

    else:
        return redirect('/login')


"""def show_profile(request, userToShow):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        # Test if the parameter is passed
        if 'userToShow' in request.GET and request.GET['userToShow'] != '':
            user_to_show_id = int(request.GET['userToShow'])
            results = Person.objects.filter(id=user_to_show_id)
            if len(results) == 1:
                if Student.objects.filter(id=user_to_show_id):
                    user_to_show = Student.objects.get(id=user_to_show_id)
                else:
                    user_to_show = Employee.objects.get(id=user_to_show_id)
                return render(request, 'show_profile.html', {'user_to_show': user_to_show})
            else:
                return render(request, 'show_profiel.html', {'user_to_show': logged_user})
        # Parameter is not find
        else:
            return render(request, 'show_profile.html', {'user_to_show': logged_user})
    else:
        return redirect('/login')


def modify_profile(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if len(request.POST) > 0:
            if type(logged_user) == Student:
                form = StudentProfileForm(request.POST, instance=logged_user)
            else:
                form = EmployeeProfileForm(request.POST, instance=logged_user)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                return render(request, 'modify_profile.html', {'form': form})
        else:
            if type(logged_user) == Student:
                form = StudentProfileForm(instance=logged_user)
            else:
                form = EmployeeProfileForm(instance=logged_user)
            return render(request, 'modify_profile.html', {'form': form})
    else:
        return redirect('/login')"""
