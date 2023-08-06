from setuptools import setup, find_packages
from os.path import join, dirname
import django_deploy_templates

setup(
    name='django-deploy-templates',
    version=django_deploy_templates.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    long_description_content_type='text/x-rst',
    install_requires=[
        'Django>=2',
        'Jinja2>=2.10'
    ]
)
