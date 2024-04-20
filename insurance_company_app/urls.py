from django.urls import re_path
from .views import news, company_branches, insurance_contract, accounts, insurance_types, discounts

branches_patterns = [
    re_path(r'^branches/$', company_branches.index, name='company_branches'),
    re_path(r'^branches/create/$', company_branches.create, name='create_branch'),
    re_path(r'^branches/edit/(?P<id>\d+)/$', company_branches.edit, name='edit_branch'),
    re_path(r'^branches/delete/(?P<id>\d+)/$', company_branches.delete, name='delete_branch')
]

contracts_patterns = [
    re_path(r'^contracts/$', insurance_contract.index, name='contracts'),
    re_path(r'^contracts/make/$', insurance_contract.create, name='make_contract')
]

accounts_patterns = [
    re_path(r'^accounts/profile/$', accounts.profile, name='profile'),
    re_path(r'^accounts/logout/$', accounts.logout_view, name='logout'),
    re_path(r'^register/$', accounts.register, name='register')
]

urlpatterns = [
    re_path(r'^home/$', news.news_view, name='main_page'),
    re_path(r'^information/$', accounts.superuser_extra_view, name='superuser_extra_information'),
    re_path(r'^insurance_types/$', insurance_types.index, name='insurance_types'),
    re_path(r'^discounts/$', discounts.index, name='special_offers&discounts')
]

urlpatterns += branches_patterns + contracts_patterns + accounts_patterns