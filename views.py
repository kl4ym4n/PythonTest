from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.views import generic
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login
from django.core.context_processors import csrf
from .forms import *
from .models import *
import hashlib, datetime, random
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect


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
            # status =
            # Get user by username
            user = User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
            new_profile.save()

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

    # check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('polls/confirm_expired.html')
    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('polls/confirm.html')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


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


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


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


def add_link(request):
    args = {}
    args.update(csrf(request))
    # print('add_link() is called')
    if request.method == 'POST':
        form = LinkForm(request.POST)
        args['form'] = form
        current_user = request.user
        print (current_user.id)
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


def display_public_links(request):
    public_links = Link.objects.filter(private_flag=False)
    view_name = 'Public links'
    return render(request, 'polls/links_view.html', {'link': public_links, 'view_name': view_name})


def display_all_links(request):
    all_links = Link.objects.all()
    view_name = 'All links'
    return render(request, 'polls/links_view.html', {'link': all_links, 'view_name': view_name})


def display_user_list(request):
    users = User.objects.all()
    return render(request, 'polls/user_list_view.html', {'users': users})


def display_current_user_links(request):
    user_links = Link.objects.filter(user_id=request.user.id)
    view_name = 'My links'
    return render(request, 'polls/links_view.html', {'link': user_links, 'view_name': view_name})


def display_user_profile(request):
    fields = User._meta.get_fields()
    user_info = User.objects.filter(id=request.user.id)
    return render(request, 'polls/profile_view.html', {'fields': fields, 'profile': user_info})


def display_link_info(request, link_id):
    link = Link.objects.get(id=link_id)
    return render(request, 'polls/link_info_view.html', {'link': link})


def display_edit_link_info(request, link_id):
    link = Link.objects.get(id=link_id)
    instance = get_object_or_404(Link, id=link_id)
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/polls/linkInfo/' + link_id + '/')
    else:
        form = LinkForm(initial={'link': link.link, 'link_description': link.link_description, 'private_flag': link.private_flag})

    return render(request, 'polls/edit_link_info_view.html', {'form': form})


def display_edit_user_profile(request):
    profile = User.objects.get(id=request.user.id)
    instance = get_object_or_404(User, id=request.user.id)
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
        form = UserProfileForm(initial={'username': profile.username, 'first_name': profile.first_name, 'last_name': profile.last_name, 'email': profile.email, 'is_active': profile.is_active})

    fields = User._meta.get_fields()
    user_info = User.objects.filter(id=request.user.id)
    return render(request, 'polls/profile_edit_view.html', {'fields': fields, 'profile': user_info, 'form': form})


def logout_user(request):
    logout(request)
    return redirect('/polls/login')
