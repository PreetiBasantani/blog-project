from django.urls import path, re_path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('category/<category>', views.PostCategoryListView.as_view(), name='post_category_list'),
    path('info/', views.InfoTemplateView.as_view(), name='about_info'),
    path('post_detail/<pk>', views.PostDetailView.as_view(), name='post_detail'),
    # path('thanks/', views.ThanksTemplateView.as_view(), name='add_comments'),
    path('add_comments/<pk>', views.add_comments, name='add_comments'),
    path('post/add/', views.PostCreateView.as_view(), name='create_post'),
    path('post/drafts/', views.draftview, name='drafts'),
    path('post/update/<pk>', views.PostUpdateView.as_view(), name='update_post'),
    path('post/delete/<pk>', views.PostDeleteView.as_view(), name='delete_post'),
    path('post/publish/<pk>', views.post_publish, name='publish_post'),
    path('success/', views.success, name='success'),
    path('create/user/', views.add_user, name='add_user' )

]
