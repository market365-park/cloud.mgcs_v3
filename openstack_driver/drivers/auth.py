from keystoneauth1.identity import v3
from keystoneauth1 import session

# auth = v3.Password(
#     auth_url='http://10.12.14.31:5000/v3',
#     username='test',
#     password='test',
#     project_name='test',
#     user_domain_name='default',
#     project_domain_name='default'
# )

# auth = v3.Password(
#     auth_url='http://10.12.14.31:5000/v3',
#     username='admin',
#     password='devOps!23',
#     project_name='admin',
#     user_domain_name='default',
#     project_domain_name='default'
# )

#auth = v3.Password(
#    auth_url='http://10.12.14.31:5000/v3',
#    username='testuser',
#    password='testuser',
#    project_name='test_project',
#    user_domain_name='default',
#    project_domain_name='default'
# )

auth = v3.Password(
    auth_url='http://10.12.14.36:5000/v3',
    username='admin',
    password='docker!23',
    project_name='devops',
    user_domain_name='default',
    project_domain_name='default'
)

sess = session.Session(auth=auth)