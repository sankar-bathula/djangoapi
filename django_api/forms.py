from django import forms
from django_api.models import Employee
class EmployeeForm(forms.ModelForm):
    def clen_esal(self):
        inputsal = self.cleaned_data['esal']
        if esal < 5000:
            raise forms.ValidationError('the minimum salary grater than 5000')
        return inputsal
        class Meta:
            model = Employee
            fields = '__all__'
