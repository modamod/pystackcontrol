from django import forms



class MyForm(forms.Form):
    search_field = forms.CharField(max_length=1000)


class InstanceDetailForm(forms.Form):
    instance_id = forms.CharField(max_length=1000, widget=forms.HiddenInput)





