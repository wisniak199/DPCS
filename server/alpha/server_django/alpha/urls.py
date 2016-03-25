from django.conf.urls import url
from alpha import views

urlpatterns = [
    url(r'^crash-reports/$', views.crash_report_list),
    url(r'^crash-reports/(?P<pk>[0-9]+)/$', views.crash_report_detail),

    url(r'^crash-groups/$', views.crash_group_list),
    url(r'^crash-groups/(?P<pk>[0-9]+)/$', views.crash_group_detail),

    url(r'^crash-groups/add/$', views.crash_group_add),
    url(r'^crash-reports/add/$', views.crash_report_add),

    url(r'^solutions/(?P<pk>[0-9]+)/$', views.solution_detail),
    url(r'^solutions/$', views.solution_list),
]
