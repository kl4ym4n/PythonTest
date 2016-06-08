from . utils import *


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
        # args['form'] = RegistrationForm()

        form = RegistrationForm()

    # return render_to_response('polls/register.html', args, context_instance=RequestContext(request))
    return render(request, 'polls/register.html', {'form': form})


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


@login_required(login_url=REDIRECT_LOGIN_URL)
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


@login_required(login_url=REDIRECT_LOGIN_URL)
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


@login_required(login_url=REDIRECT_LOGIN_URL)
def logout_user(request):
    logout(request)
    return redirect('/polls/login')


def display_403_page(request):
    return render_to_response('polls/403_view.html')
