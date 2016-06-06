from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import *
# Execute once
# anonymous_users = Group(name='Anonymous Users')
# anonymous_users.save()
usual_users = Group(name='Usual Users')
# usual_users.save()
# editor_users = Group(name='Editor Users')
# editor_users.save()
# admin_users = Group(name='Admin Users')
# admin_users.save()

content_type_user = ContentType.objects.get_for_model(User)
can_add_link = Permission(name='Can Add Link',
                          codename='can_add_link',
                          content_type=content_type_user)
can_add_link.save()
usual_users.permissions.add(can_add_link)
can_edit_link = Permission(name='Can Edit Link',
                           codename='can_edit_link',
                           content_type=content_type_user)
can_edit_link.save()
usual_users.permissions.add(can_edit_link)
can_view_public_links = Permission(name='Can View Public Links',
                                   codename='can_view_public_links',
                                   content_type=content_type_user)
can_view_public_links.save()
usual_users.permissions.add(can_view_public_links)
