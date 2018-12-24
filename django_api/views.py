from django.shortcuts import render
from django.views.generic import View
from django_api.models import Employee
import json
from django.http import HttpResponse
from django.core.serializers import serialize
from django_api.mixins import SerializeMixin,HttpResponseMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_api.utils import is_json
from django_api.forms import EmployeeForm
# Create your views here.
# @method_decorator(csrf_exempt, name='dispatch')
# class EmployeeCRUDView(SerializeMixin, HttpResponseMixin, View):
#     def get_object_by_id(id):
#         try:
#             emp = Employee.objects.get(id=id)
#         except Employee.DoesNotExit:
#             emp=None
#         return emp
#     def get(self, request, *args, **kwargs):
#         data = request.body
#         if not is_json(data):
#             return render_to_http_rsponse(json.dumps({'msg':'Please send valid json data'}), status=401)
#         data = json.loads(request.body)
#         id=json.get('id', None)
#         if id is not None:
#             obj = self.get_object_by_id(id)
#             if obj is None:
#                 return render_to_http_rsponse(json.dumps({'msg':'no matched record found for this id'}), staus=404)
#             json_data = self.serialize([obj,])
#             return render_to_http_rsponse(json_data)
#         qs=Employee.objects.all()
#         json_data = self.serialize(qs)
#         return self.render_to_http_rsponse(json_data)

@method_decorator(csrf_exempt,name='dispatch')
class EmployeeCRUDCBV(HttpResponseMixin,SerializeMixin,View):
    def get_object_by_id(self,id):
        try:
            emp=Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp=None
        return emp

    def get(self,request,*args,**kwargs):
        data=request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg':'plz send valid json data only'}),status=400)
        data=json.loads(request.body)
        id=data.get('id',None)
        if id is not None:
            obj=self.get_object_by_id(id)
            if obj is None:
                return self.render_to_http_response(json.dumps({'msg':'No Matched Record Found with Specified Id'}),status=404)
            json_data=self.serialize([obj,])
            return self.render_to_http_response(json_data)
        qs=Employee.objects.all()
        json_data=self.serialize(qs)
        return self.render_to_http_response(json_data)

    def post(self,request,*args,**kwargs):
        data=request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg':'plz send valid json data only'}),status=400)
        empdata=json.loads(request.body)
        form=EmployeeForm(empdata)
        if form.is_valid():
            obj = form.save(commit=True)
            return self.render_to_http_response(json.dumps({'msg':'resource created successfully'}))
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_http_response(json_data,status=400)
    def put(self,request,*args,**kwargs):
        data=request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg':'plz send valid json data only'}),status=400)
        data=json.loads(request.body)
        id=data.get('id',None)
        if id is None:
            return self.render_to_http_response(json.dumps({'msg':'To perform updation id is mandatory,you should provide'}),status=400)
        obj=self.get_object_by_id(id)
        if obj is None:
            json_data=json.dumps({'msg':'No matched record found, Not possible to perform updataion'})
            return self.render_to_http_response(json_data,status=404)

        new_data=data
        old_data={
        'eno':obj.eno,
        'ename':obj.ename,
        'esal':obj.esal,
        'eaddr':obj.eaddr,
        }
        # for k,v in new_data.items():
        #     old_data[k]=v
        old_data.update(new_data)
        form=EmployeeForm(old_data,instance=obj)
        if form.is_valid():
            form.save(commit=True)
            json_data=json.dumps({'msg':'Updated successfully'})
            return self.render_to_http_response(json_data,status=201)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_http_response(json_data,status=400)
    def delete(self,request,*args,**kwargs):
        data=request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg':'plz send valid json data only'}),status=400)
        data=json.loads(request.body)
        id=data.get('id',None)
        if id is None:
            return self.render_to_http_response(json.dumps({'msg':'To perform delete, id is mandatory,you should provide'}),status=400)
        obj=self.get_object_by_id(id)
        if obj is None:
            json_data=json.dumps({'msg':'No matched record found, Not possible to perform delete operation'})
            return self.render_to_http_response(json_data,status=404)
        status,deleted_item=obj.delete()
        if status==1:
            json_data=json.dumps({'msg':'Resource Deleted successfully'})
            return self.render_to_http_response(json_data,status=201)
        json_data=json.dumps({'msg':'unable to delete ...plz try again'})
        return self.render_to_http_response(json_data,status=500)
