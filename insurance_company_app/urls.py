from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import news, company_branches, insurance_contract, accounts, insurance_types, \
    discounts, reviews, faq, vacancies, news, about_company, contacts

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
    re_path(r'^accounts/profile/$', accounts.user_profile_view, name='user_profile_view'),
    re_path(r'^accounts/employee_profile/$', accounts.employee_profile_view, name='employee_profile_view'),
    re_path(r'^accounts/superuser_profile/$', accounts.superuser_profile_view, name='superuser_profile'),
    re_path(r'^accounts/superuser_profile/statistics/$', accounts.superuser_extra_view, name='superuser_extra_view'),
    re_path(r'^accounts/logout/$', accounts.logout_view, name='logout'),
    re_path(r'^register/$', accounts.register, name='signin'),
    re_path(r'^login/$', accounts.custom_login, name='login')
]

review_patterns = [
    re_path(r'^reviews/$', reviews.index, name='reviews'),
    re_path(r'^reviews/make/$', reviews.create_review, name='create_review')
]

urlpatterns = [
    re_path(r'^home/$', news.home, name='home'),
    re_path(r'^insurance_types/$', insurance_types.index, name='insurance_types'),
    re_path(r'^discounts/$', discounts.index, name='special_offers&discounts'),
    re_path(r'^contacts/$', contacts.index, name='contacts'),
    re_path(r'^faq/$', faq.index, name='faq'),
    re_path(r'^vacancies/$', vacancies.index, name='vacancies'),
    re_path(r'^news/$', news.index, name='news'),
    re_path(r'^news/details/(?P<id>\d+)/$', news.details, name='news_details'),
    re_path(r'^about_company/$', about_company.index, name='about_company')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += branches_patterns + contracts_patterns + accounts_patterns + review_patterns
