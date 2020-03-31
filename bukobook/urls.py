from django.urls import path
from .views import auth, blog

app_name = 'bukobook'
urlpatterns = [
    path('', blog.index, name='index'),
    path('register', auth.register, name='register'),
    path('login', auth.login, name='login'),
    path('new', blog.create_article, name='create'),
    path('logout', auth.logout, name='logout'),
    path('article/<int:id>', blog.read_article, name='article'),
    path('update/<int:id>', blog.update, name='update'),
    path('personal/<int:id>', blog.personal, name='personal'),
    path('delect/<int:id>', blog.delete, name='delect'),
    path('comment/<int:id>', blog.submit_comment, name='comment'),
    path('reply/<int:id>', blog.submit_reply, name='reply'),
]