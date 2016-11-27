# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from datetime import datetime

from stacksession.session import glance, nova, neutron
from web.forms import MyForm, InstanceDetailForm, RulesAddForm
from django.forms import HiddenInput


def index(request):

    images = glance.images.list()
    instances = nova.servers.list()
    if request.method == 'POST':
        form = InstanceDetailForm(request.POST)
        if form.is_valid():
            instance_id = form.cleaned_data['instance_id']
            if 'instance_detail' in request.POST:
                return redirect('instance', instance_id=instance_id)
            elif 'console' in request.POST:
                inst = nova.servers.get(instance_id)
                return redirect(inst.get_vnc_console('novnc')['console']['url'])
            elif 'delete_instance' in request.POST:
                raise NotImplementedError
    context = {
        'title': "Home Page",
        'images': images,
        'instances': instances,
    }
    return render(request, template_name='index.html', context=context)


def image(request, image_id):
    res = glance.images.get(image_id)
    template = loader.get_template('image.html')
    context = {
        'title': "Image Detail",
        'image': res,
    }
    return HttpResponse(template.render(context, request))


def instance(request, instance_id):
    res = nova.servers.get(instance_id)
    secgrp = nova.servers.list_security_group(res.id)
    neutronsecres = neutron.list_security_groups()['security_groups']
    secgrpres = []
    for s in secgrp:
        for sn in neutronsecres:
            if s.id == sn['id']:
                secgrpres.append(sn)

    host = res.__getattr__('OS-EXT-SRV-ATTR:host')
    launch = res.__getattr__('OS-SRV-USG:launched_at')
    created_at = datetime.strptime(res.created, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%S')
    launched_at = datetime.strptime(launch, '%Y-%m-%dT%H:%M:%S.%f')
    uptime = datetime.strptime(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%S') - \
             datetime.strptime(launched_at.strftime('%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%S')
    console_url = str(res.get_vnc_console('novnc')['console']['url'])
    template = loader.get_template('instance.html')
    form = RulesAddForm()
    context = {
        'title': "Instance Detail",
        'instance': res,
        'console_url': console_url,
        'host': host,
        'launched_at': launched_at.strftime('%Y-%m-%dT%H:%M:%S'),
        'uptime': uptime,
        'created_at': created_at,
        'securitygrps': secgrpres,
        'ruleform': form
    }
    return HttpResponse(template.render(context, request))


def security_groups(request):
    # res = nova.servers.list_security_group('8e50d487-f156-457a-924a-6cc0d7aadb18')
    res = nova.security_groups.list()
    template = loader.get_template('security_groups.html')
    context = {
        'title': "Security Groups",
        'securitygrps': res,
    }
    return HttpResponse(template.render(context, request))


def overview(request):
    hyp = nova.hypervisors.list()
    ins = nova.servers.list()

    template = loader.get_template('overview.html')
    context = {
        'title': "Overview",
        'hypervisors': hyp,
        'instances': ins,

    }
    # return HttpResponse(template.render(context, request))
    return render(request=request, template_name='overview.html', context=context)


def search(request):
    context = {}
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            context = {
                'title': "My Form",
                'form': form,
            }
            return HttpResponseRedirect(reverse('home'), context)
    else:
        form = MyForm()
        context = {
            'title': "My Form",
            'form': form,
        }

    return render(request, template_name='myform.html', context=context)


def deleterule(request, rule_id, instance_id):
    if request.method == 'POST':
        neutron.delete_security_group_rule(rule_id)
    return redirect('instance', instance_id=instance_id)

def createrule(request, secgrp_id, instance_id):
    if request.method == 'POST':
        form = RulesAddForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            security_group_rule = {
                "direction": form.cleaned_data['direction'].lower(),
                "port_range_min": form.cleaned_data['port_range_min'],
                "ethertype": form.cleaned_data['ethertype'].lower(),
                "port_range_max": form.cleaned_data['port_range_max'],
                "protocol": form.cleaned_data['protocol'].lower(),
                "remote_ip_prefix": form.cleaned_data['remote_ip_prefix'],
                "security_group_id": secgrp_id,
            }
            neutron.create_security_group_rule(body={'security_group_rule': security_group_rule})
            print "Wooooorkkkkkeeeeedd yeeeeeeeeeeyyyy !!!!!!!"
    return redirect('instance', instance_id=instance_id)
