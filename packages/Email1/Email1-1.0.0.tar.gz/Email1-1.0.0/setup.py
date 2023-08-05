from distutils.core import setup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

setup(
    name='Email1',
    version='1.0.0',
    py_modules=['send_mail'],
    author='lyl',
    author_email='919188649@qq.com',
    url='',
    description='test'
)