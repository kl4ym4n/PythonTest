import hashlib
import random
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views import generic
from django.views.generic.edit import FormView

from .forms import *
from .models import *

# content_type_user = ContentType.objects.get_for_model(User)
# can_view_public_links = Permission(name='Can View Public Links',
#                                    codename='can_view_public_links',
#                                    content_type=content_type)
# can_view_public_links.save()


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            activation_key = hashlib.sha1((salt + email).encode('utf-8')).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            # Get user by username
            user = User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
            new_profile.save()
            default_group = Group.objects.get(name='Usual Users')
            user.groups.add(default_group)
            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48 hours http://33.33.33.10:8000/polls/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',
                      [email], fail_silently=False)

            return HttpResponseRedirect('/polls/login')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('polls/register.html', args, context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/polls/index')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # check if the activation key has expired, if it has then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('polls/confirm_expired.html')
    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('polls/confirm.html')


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
            return False

    return user_passes_test(in_groups, '/polls/403/')


def index_view(request):
    # print(request.user.groups.all())
    return render(request, 'polls/index.html')


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    # assert False
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/polls/login/"
    template_name = "polls/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "polls/login.html"

    success_url = "/polls"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


@login_required(login_url='/polls/login/')
@group_required('Usual Users')
def add_link(request):
    args = {}
    args.update(csrf(request))
    # print('add_link() is called')
    if request.method == 'POST':
        form = LinkForm(request.POST)
        args['form'] = form
        current_user = request.user
        # print(current_user.id)
        if form.is_valid():
            # form.save()  # save user to database if form is valid
            link = form.save(commit=False)
            link.user_id = request.user.id
            link.save()
            return HttpResponseRedirect('/polls/addLink/')
    else:
        form = LinkForm()

    # return render_to_response('polls/add_link_view.html', args, context_instance=RequestContext(request))
    return render(request, 'polls/add_link_view.html', {'form': form})


def pager(request, queries, num_on_page):
    paginator = Paginator(queries, num_on_page)
    page = request.GET.get('page')
    try:
        num_of_entity = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        num_of_entity = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        num_of_entity = paginator.page(paginator.num_pages)
    return num_of_entity


def display_public_links(request):
    public_links = Link.objects.filter(private_flag=False)
    view_name = 'Public links'
    links = pager(request, public_links, 5)
    return render(request, 'polls/links_view.html', {'link': links, 'view_name': view_name})


@login_required(login_url='/polls/login/')
@group_required('Editor Users')
def display_all_links(request):
    all_links = Link.objects.all()
    view_name = 'All links'
    links = pager(request, all_links, 5)
    return render(request, 'polls/links_view.html', {'link': links, 'view_name': view_name})


@login_required(login_url='/polls/login/')
@group_required('Admin Users')
def display_user_list(request):
    users = User.objects.all()
    user_list = pager(request, users, 5)
    return render(request, 'polls/user_list_view.html', {'users': user_list})


@login_required(login_url='/polls/login/')
@group_required('Usual Users')
def display_current_user_links(request):
    user_links = Link.objects.filter(user_id=request.user.id)
    view_name = 'My links'
    links = pager(request, user_links, 5)
    return render(request, 'polls/links_view.html', {'link': links, 'view_name': view_name})


@login_required(login_url='/polls/login/')
@group_required('Usual Users')
def display_user_profile(request):
    fields = User._meta.get_fields()
    user_info = User.objects.get(id=request.user.id)
    return render(request, 'polls/profile_view.html', {'fields': fields, 'profile': user_info})


@login_required(login_url='/polls/login/')
@group_required('Usual Users')
def display_link_info(request, link_id):
    link = Link.objects.get(id=link_id)
    if request.user.id != link.user_id:
            is_mine = False
    else:
        is_mine = True

    return render(request, 'polls/link_info_view.html', {'link': link, 'mine': is_mine})


@login_required(login_url='/polls/login/')
@group_required('Usual Users')
def display_edit_link_info(request, link_id):
    link = Link.objects.get(id=link_id)
    instance = get_object_or_404(Link, id=link_id)
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/polls/linkInfo/' + link_id + '/')
    else:
        form = LinkForm(
            initial={'link': link.link, 'link_description': link.link_description, 'private_flag': link.private_flag})

    return render(request, 'polls/edit_link_info_view.html', {'form': form})


@login_required(login_url='/polls/login/')
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


@login_required(login_url='/polls/login/')
@group_required('Usual Users')
def delete_link(request, link_id):
    link = Link.objects.get(id=link_id)
    if request.user.id != link.user_id:
        is_mine = False
    else:
        is_mine = True
    if is_mine or request.user.has_perm('polls.can_delete_all_links'):
        link.delete()
        return HttpResponseRedirect('/polls/publicLinks')
    else:
        return redirect('/polls/403/')


@login_required(login_url='/polls/login/')
@group_required('Admin Users')
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    links = Link.objects.filter(user_id=user_id)
    if request.user.has_perm('polls.can_delete_all_users'):
        links.delete()
        user.delete()
        return HttpResponseRedirect('/polls/userList')
    else:
        return redirect('/polls/403/')


@login_required(login_url='/polls/login/')
def logout_user(request):
    logout(request)
    return redirect('/polls/login')


def display_403_page(request):
    return render_to_response('polls/403_view.html')
