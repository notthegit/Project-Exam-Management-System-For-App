# analysis_data / urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^hello-world/$', views.HelloAPI.as_view(), name='hello_api'),
    url(r'^api-project/$', views.ApiProject.as_view(), name='api_project'),    
    url(r'^grade$', views.GradeApi.as_view(), name='grade_api'),
    url(r'^gradeadvisor$', views.GradeAdvisorApi.as_view(), name='grade_advisor_api'),
    url(r'^gradeposter$', views.GradePosterApi.as_view(), name='grade_poster_api'),
    url(r'^savegrade$', views.SaveGradeApi.as_view(), name='save_grade_api'),
    url(r'^savegradeadvisor$', views.SaveGradeAdvisorApi.as_view(), name='save_grade_advisor_api'),
    url(r'^savegradeposter$', views.SaveGradePosterApi.as_view(), name='save_grade_poster_api'),
    url(r'^project/$', views.ProjectApi.as_view(), name='project_api'),
    url(r'^schedule/$', views.ScheduleApi.as_view(), name='schedule_api'),
    url(r'^scheduleposter/$', views.SchedulePosterApi.as_view(), name='schedule_poster_api'),
    url(r'^score/$', views.ScoreApi.as_view(), name='score_api'),
    url(r'^login/$', views.myLogin, name='login_api'),
    url(r'^setting/$', views.SettingApi.as_view(), name='setting_api'),
    url(r'^settingadmin$', views.SettingAdminApi.as_view(), name='setting_admin_api'),
    url(r'^scoreprojid$', views.ScoreProjIdApi.as_view(), name='score_proj_id_api'),
    url(r'^scoreposterjid$', views.ScorePosterjIdApi.as_view(), name='score_poster_id_api'),
    url(r'^allschedule$', views.AllScheduleApi.as_view(), name='all_schedule_api'),
]