from keystoneauth1.identity import v3
from keystoneauth1 import session
from glanceclient import client as gclient
from novaclient import client as novaclient
from cinderclient import client as cinderclient

auth = v3.Password(auth_url='http://192.168.56.101:5000/v3',
                   username='admin',
                   password='nomoresecret',
                   project_name='admin',
                   user_domain_id='default',
                   project_domain_id='default')
sess = session.Session(auth=auth)
glance = gclient.Client("2", session=sess)
nova = novaclient.Client("2.1", session=sess)
cinder = cinderclient.Client("2", session=sess)


