from django import forms

class SensorImportForm(forms.Form):
    file = forms.FileField(label='Arquivo CSV', help_text='Selecione um arquivo .csv para importar')
