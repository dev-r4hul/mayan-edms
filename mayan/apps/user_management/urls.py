from django.conf.urls import url

from .api_views import (
    APICurrentUserView, APIGroupDetailView, APIGroupListView,
    APIGroupUserAddView, APIGroupUserListView, APIGroupUserRemoveView,
    APIUserDetailView, APIUserGroupListView, APIUserListView
)
from .views.group_views import (
    GroupCreateView, GroupDeleteView, GroupDetailView, GroupEditView,
    GroupListView, GroupUserAddRemoveView
)
from .views.user_views import (
    UserCreateView, UserDeleteView, UserDetailView,
    UserEditView, UserGroupAddRemoveView, UserListView, UserOptionsEditView
)

from rahul.views import introduce

urlpatterns_groups = [
    url(
        regex=r'^rahul/$', name='rahul', view=introduce
    ),
    url(
        regex=r'^groups/$', name='group_list', view=GroupListView.as_view()
    ),
    url(
        regex=r'^groups/create/$', name='group_create',
        view=GroupCreateView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>\d+)/delete/$',
        name='group_single_delete', view=GroupDeleteView.as_view()
    ),
    url(
        regex=r'^groups/multiple/delete/$', name='group_multiple_delete',
        view=GroupDeleteView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>\d+)/$', name='group_detail',
        view=GroupDetailView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>\d+)/edit/$', name='group_edit',
        view=GroupEditView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>\d+)/users/$', name='group_members',
        view=GroupUserAddRemoveView.as_view()
    )
]

urlpatterns_users = [
    url(
        regex=r'^users/$', name='user_list', view=UserListView.as_view()
    ),
    url(
        regex=r'^users/create/$', name='user_create',
        view=UserCreateView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/delete/$', name='user_single_delete',
        view=UserDeleteView.as_view()
    ),
    url(
        regex=r'^users/multiple/delete/$', name='user_multiple_delete',
        view=UserDeleteView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/$', name='user_details',
        view=UserDetailView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/edit/$', name='user_edit',
        view=UserEditView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/groups/$', name='user_groups',
        view=UserGroupAddRemoveView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/options/$', name='user_options',
        view=UserOptionsEditView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_groups)
urlpatterns.extend(urlpatterns_users)

api_urls = [
    url(
        regex=r'^groups/$', name='group-list',
        view=APIGroupListView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>[0-9]+)/$', name='group-detail',
        view=APIGroupDetailView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>[0-9]+)/users/$',
        name='group-user-list', view=APIGroupUserListView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>[0-9]+)/users/add/$',
        name='group-user-add', view=APIGroupUserAddView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>[0-9]+)/users/remove/$',
        name='group-user-remove', view=APIGroupUserRemoveView.as_view()
    ),
    url(
        regex=r'^users/$', name='user-list', view=APIUserListView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>[0-9]+)/$', name='user-detail',
        view=APIUserDetailView.as_view()
    ),
    url(
        regex=r'^users/current/$', name='user-current',
        view=APICurrentUserView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>[0-9]+)/groups/$', name='user-group-list',
        view=APIUserGroupListView.as_view()
    )
]
