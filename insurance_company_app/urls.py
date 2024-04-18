from django.urls import path
from .views import news, company_branches, insurance_contract, accounts

urlpatterns = [
    path('', news.news_view, name='main_page'),
    path('branches/', company_branches.index, name='company_branches'),
    path('branches/create/', company_branches.create, name='create_branch'),
    path('branches/edit/<int:id>/', company_branches.edit, name='edit_branch'),
    path('branches/delete/<int:id>', company_branches.delete, name='delete_branch'),
    path('contracts/', insurance_contract.index, name='contracts'),
    path('accounts/profile/', accounts.profile, name='profile'),
    path('accounts/logout/', accounts.logout_view, name='logout'),
    path('register/', accounts.register, name='register')
]
