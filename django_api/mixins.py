from django.core.serializers import serialize
import json
class SerializeMixin(object):
    "SerializeMixin for json data and python dicttionary data structure"
    def serialize(self, qs):
        """ To convert json data into python data """
        json_data = serialize('json', qs)
        py_dict_data =json.loads(json_data)
        new_dict={}
        for dict_data in py_dict_data:
            new_dict.append(dict_data['fields'])
        json_data = json.dumps(new_dict)
        return json_data
class HttpResponseMixin(object):
    """ Http Response mixin class topass default staus and data"""
    def render_to_http_rsponse(self, data, status=200):
        """this method return data and stsus type of applications"""
        return HttpResponse(data, content_type='application/json', status=status)
