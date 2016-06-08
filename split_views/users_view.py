from .. utils import *


@login_required(login_url=REDIRECT_LOGIN_URL)
@group_required('Admin Users')
def display_user_list(request):
    users = User.objects.all()
    user_list = pager(request, users, 5)
    return render(request, 'polls/user_list_view.html', {'users': user_list})


@login_required(login_url=REDIRECT_LOGIN_URL)
@group_required('Usual Users')
def display_current_user_links(request):
    user_links = Link.objects.filter(user_id=request.user.id)
    view_name = 'My links'
    links = pager(request, user_links, 5)
    return render(request, 'polls/links_view.html', {'link': links, 'view_name': view_name})


@login_required(login_url=REDIRECT_LOGIN_URL)
@group_required('Usual Users')
def display_user_profile(request):
    fields = User._meta.get_fields()
    user_info = User.objects.get(id=request.user.id)
    return render(request, 'polls/profile_view.html', {'fields': fields, 'profile': user_info})


@login_required(login_url=REDIRECT_LOGIN_URL)
@group_required('Usual Users')
def display_edit_user_profile(request, user_id):
    profile = User.objects.get(id=user_id)
    instance = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.cleaned_data
            password = data['password']
            profile.set_password(password)
            form.save()
            profile.save()
            return HttpResponseRedirect('/polls/login')
    else:
        form = UserProfileForm(
            initial={'username': profile.username, 'first_name': profile.first_name, 'last_name': profile.last_name,
                     'email': profile.email, 'is_active': profile.is_active})

    fields = User._meta.get_fields()
    user_info = User.objects.filter(id=request.user.id)
    return render(request, 'polls/profile_edit_view.html', {'fields': fields, 'profile': user_info, 'form': form})
