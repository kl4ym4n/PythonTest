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

can_view_all_links = Permission(name='Can View All Links',
                                codename='can_view_all_links',
                                content_type=content_type_user)
can_view_all_links.save()
can_edit_all_links = Permission(name='Can Edit All Links',
                                codename='can_edit_all_links',
                                content_type=content_type_user)
can_edit_all_links.save()
can_delete_all_links = Permission(name='Can Delete All Links',
                                  codename='can_delete_all_links',
                                  content_type=content_type_user)
can_delete_all_links.save()
can_view_all_users = Permission(name='Can View All Users',
                                codename='can_view_all_users',
                                content_type=content_type_user)
can_view_all_users.save()
can_edit_all_users = Permission(name='Can Edit All Users',
                                codename='can_edit_all_users',
                                content_type=content_type_user)
can_edit_all_users.save()
can_delete_all_users = Permission(name='Can Delete All Users',
                                  codename='can_delete_all_users',
                                  content_type=content_type_user)
can_delete_all_users.save()
