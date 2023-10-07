from django.urls import path

from robots.views import RobotInfoCreate, RobotList, RobotInfoList, RobotInfoReport

app_name = 'robots'

urlpatterns = [
    path('', RobotList.as_view(), name='robot_list'),
    path('robots_info/', RobotInfoList.as_view(), name='robot_info_list'),
    path('robots_create/', RobotInfoCreate.as_view(), name='robot_create'),
    path('robots_info_report/', RobotInfoReport.as_view(), name='robot_info_report'),
]
