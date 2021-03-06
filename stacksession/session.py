from keystoneauth1.identity import v3
from keystoneauth1 import session
from glanceclient import client as gclient
from novaclient import client as novaclient
from cinderclient import client as cinderclient
from neutronclient.v2_0 import client as neutronclient

auth = v3.Password(auth_url='http://192.168.56.101:5000/v3',
                   username='admin',
                   password='nomoresecret',
                   project_name='admin',
                   user_domain_id='default',
                   project_domain_id='default')
auth_neutron = v3.Password(auth_url='http://192.168.56.101:35357/v3',
                   username='admin',
                   password='nomoresecret',
                   project_name='admin',
                   user_domain_id='default',
                   project_domain_id='default')
sess = session.Session(auth=auth)
sess2 = session.Session(auth=auth_neutron)
glance = gclient.Client("2", session=sess)
nova = novaclient.Client("2.1", session=sess)
cinder = cinderclient.Client("2", session=sess)
neutron = neutronclient.Client(session=sess2)

