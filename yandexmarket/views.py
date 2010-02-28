from django import http
from yandexmarket import utils


def generate_yml(request):
    yml_generator = utils.YMLGenerator(request.META['HTTP_HOST'])
    return http.HttpResponse(yml_generator.generate())
