from .. utils import *


def display_public_links(request):
    public_links = Link.objects.filter(private_flag=False)
    view_name = 'Public links'
    links = pager(request, public_links, 5)
    return render(request, 'polls/links_view.html', {'link': links, 'view_name': view_name})


@login_required(login_url=REDIRECT_LOGIN_URL)
@group_required('Usual Users')
def add_link(request):
    args = {}
    args.update(csrf(request))
    # print('add_link() is called')
    if request.method == 'POST':
        form = LinkForm(request.POST)
        args['form'] = form
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


@login_required(login_url=REDIRECT_LOGIN_URL)
@group_required('Editor Users')
def display_all_links(request):
    all_links = Link.objects.all()
    view_name = 'All links'
    links = pager(request, all_links, 5)
    return render(request, 'polls/links_view.html', {'link': links, 'view_name': view_name})


@login_required(login_url=REDIRECT_LOGIN_URL)
@group_required('Usual Users')
def display_link_info(request, link_id):
    link = Link.objects.get(id=link_id)
    if request.user.id != link.user_id:
            is_mine = False
    else:
        is_mine = True

    return render(request, 'polls/link_info_view.html', {'link': link, 'mine': is_mine})


@login_required(login_url=REDIRECT_LOGIN_URL)
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


