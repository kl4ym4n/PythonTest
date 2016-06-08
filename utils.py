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
# from .models import *
from .split_models import *

REDIRECT_LOGIN_URL = '/polls/login/'


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
            return False

    return user_passes_test(in_groups, '/polls/403/')


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

