from django import forms
from django.core.exceptions import ValidationError
from .models import client_equipment

# class ClientEquipmentForm(forms.Form):
#     client_name = forms.CharField(min_length=10)
#     substation_name = forms.CharField(min_length=5)
#     equipment_name = forms.CharField(min_length=3)
#     equipment_type_full = forms.CharField()
#     equipment_type = forms.CharField()
#     testing_part = forms.CharField()
#     equipment_serial_number = forms.CharField()
#
#     def clean_substation_name(self):
#         data = self.cleaned_data['substation_name']
#         quotes_num = data.count('\"')
#         if "\'" in data:
#             raise ValidationError('Используйте двойные кавычки - "" при заполнении поля!')
#         if '\"' not in data:
#             raise ValidationError('Используйте двойные кавычки - "" при заполнении поля!')
#         if quotes_num != 2:
#             raise ValidationError(f'Проверьте количество используемых двойных кавычек (""). Вы указали {quotes_num}!')
#         return data


class ClientEquipmentForm(forms.ModelForm):

    class Meta:
        model = client_equipment
        fields = '__all__'

    def clean_substation_name(self):
        data = self.cleaned_data['client_name']
        quotes_num = data.count('\"')
        if "\'" in data:
            raise ValidationError('Используйте двойные кавычки - "" при заполнении поля!')
        if '\"' not in data:
            raise ValidationError('Используйте двойные кавычки - "" при заполнении поля!')
        if quotes_num != 2:
            raise ValidationError(f'Проверьте количество используемых двойных кавычек (""). Вы указали {quotes_num}!')
        return data
