from django.shortcuts import render, redirect
from .models import Person, Message
from .forms import PersonForm, LoginForm


def home(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        print(request.POST)
        if 'new_message' in request.POST and request.POST['new_message'] != '':
            newMessage = Message(author=logged_user, content=request.POST['new_message'])
            newMessage.save()
        friendMessages = Message.objects.filter(author__friends=logged_user)
        messages = Message.objects.all().order_by('publication_date')
        return render(request, 'mulima_app/home.html', {'logged_user': logged_user, 'friendMessages': friendMessages, 'all_messages': messages})
    else:
        return redirect('login')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_username = form.cleaned_data['username']
            logged_user = Person.objects.get(username=user_username)
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
            personForm.save()
            logged_user = Person.objects.get(username=personForm.cleaned_data.get('username'))
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

        if len(Person.objects.filter(id=logged_user_id)) == 1:
            return Person.objects.get(id=logged_user_id)
        else:
            return None
    else:
        return None


"""def add_friend(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        # Test if the form is shared
        if len(request.POST) > 0:
            form = AddFriendForm(request.POST)
            if form.is_valid():
                new_friend_email = form.cleaned_data['email']
                newFriend = Person.objects.get(email=new_friend_email)
                logged_user.friends.add(newFriend)
                logged_user.save()
                return redirect('/')
            else:
                return render(request, 'add_friend.html', {'form': form})
        # Le formulaire n'a pas été envoyé
        else:
            form = AddFriendForm()
            return render(request, 'add_friend.html', {'form': form})
    else:
        return redirect('/login')


def show_profile(request, userToShow):
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
