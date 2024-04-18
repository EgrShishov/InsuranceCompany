from django.urls import path, include
from .views import news, company_branches, account

urlpatterns = [
    path('', news.news_view, name='main_page'),
    path('branches/', company_branches.index, name='company_branches'),
    path('branches/create/', company_branches.create, name='create_branch'),
    path('branches/edit/<int:id>/', company_branches.edit, name='edit_branch'),
    path('branches/delete/<int:id>', company_branches.delete, name='delete_branch'),
    path('account/', account.index, name='account'),
    path('register/', account.register, name='register')
]
