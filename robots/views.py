import json
from http.client import HTTPException

from django.http import Http404, HttpResponse
from django.views import View
from django.views.generic import ListView

from robots.business import robot_info_report
from robots.models import Robot, RobotInfo


class RobotList(ListView):
    model = Robot
    ordering = '-created'
    template_name = 'robot/robot_list.html'
    context_object_name = 'robot_list'


class RobotInfoList(ListView):
    model = RobotInfo
    ordering = '-created'
    template_name = 'robot/robot_info_list.html'
    context_object_name = 'robot_info_list'


class RobotInfoCreate(View):
    def post(self, request):
        try:
            post_body = json.loads(request.body)
            robot_model = post_body.get('model')
            robot_version = post_body.get('version')
            robot_created = post_body.get('created')

            if Robot.objects.filter(model=robot_model).exists():
                robot_info = RobotInfo(
                    serial=robot_model + "-" + robot_version,
                    model=robot_model,
                    version=robot_version,
                    created=robot_created
                )
                robot_info.save()
                return HttpResponse('Экземпляр модели RobotInfo успешно создан', status=201)
            raise Http404('Robot not found')
        except json.JSONDecodeError as e:
            raise HTTPException(str(e))


class RobotInfoReport(View):
    def get(self, request):
        robot_info_report()
        return HttpResponse('Отчет создан', status=200)
