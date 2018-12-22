from django.shortcuts import render #to display template tags but it loads html page
from django.views.generic import View
import json# convert python data into json and traverse
from django_api.models import Employee #data base table
from django.http import HttpResponse #to display data in template tags but it display string data
from django.core.utils.decorators import method_decorstors
from django.views.decorators.csrf import csrf_exempt
from django_api.utils import is_json
from django_api.forms import EmployeeForm
# Create your views here.
class EmployeeCRUDView(SerializeMixin, HttpResponseMixin, View):
    def get_object_by_id(id):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExit:
            emp=None
        return emp

    def get(self, request, *args, **kwargs):
        data = request.body
        if is not is_json(data):
            return render_to_http_rsponse(json.dumps({'msg':'Please send valid json data'}), status=401)
        data = json.loads(request.body)
        id=json.get('id', None)
        if id is not None:
            obj = self.get_object_by_id(id)
            if obj is None:
                return render_to_http_rsponse(json.dumps({'msg':'no matched record found for this id'}), staus=404)
            json_data = self.serialize([obj,])
            return render_to_http_rsponse(json_data)
        qs=Employee.objects.all()
        json_data = self.serialize(qs)
        return self.render_to_http_rsponse(json_data)
