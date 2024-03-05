from django.urls import path
from .views import (edit_profile_view, user_profile_view, current_user_view, user_profile_details_view,
                    follow_unfollow_view, search_view, get_search_users_view, get_user_posts_view)


urlpatterns = [
    path('', user_profile_view, name='user_profile'),
    path('<int:user_id>/', current_user_view, name='current_user_profile'),
    path('details/<int:user_id>/', user_profile_details_view, name='user_profile_details'),
    path('follow-unfollow/', follow_unfollow_view, name='follow_unfollow'),
    path('edit-profile/<str:username>/', edit_profile_view, name='edit_profile'),
    path('get-user-posts/<int:num_posts>/', get_user_posts_view, name='get_user_posts'),

    path('search/', search_view, name='search'),
    path('search-users/', get_search_users_view, name='search_users'),

]
