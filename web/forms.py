from Pyrex.Plex.Traditional import re

from django import forms
from django.core.validators import RegexValidator, validate_ipv46_address
import re

class MyForm(forms.Form):
    search_field = forms.CharField(max_length=1000)


class InstanceDetailForm(forms.Form):
    instance_id = forms.CharField(max_length=1000, widget=forms.HiddenInput)


class RulesAddForm(forms.Form):
    direction= forms.CharField(validators=[RegexValidator(r'[iI]ngress|[eE]gress')])
    port_range_min= forms.IntegerField(min_value=1, max_value=65535)
    ethertype= forms.CharField(validators=[RegexValidator(re.compile(r'IPv4|IPv6', re.IGNORECASE))])
    port_range_max= forms.IntegerField(min_value=1, max_value=65535)
    protocol= forms.CharField(validators=[RegexValidator(re.compile(r'icmp|tcp|udp|null', re.IGNORECASE))])
    remote_ip_prefix= forms.CharField(validators=[RegexValidator(r'^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?')])
    # security_group_id = forms.CharField(max_length=100)


