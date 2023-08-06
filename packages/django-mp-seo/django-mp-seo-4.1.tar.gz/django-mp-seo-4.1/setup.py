
from setuptools import setup, find_packages


version = '4.1'
url = 'https://github.com/pmaigutyak/mp-seo'


setup(
    name='django-mp-seo',
    version=version,
    description='Django seo app',
    long_description=open('README.md').read(),
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT'
)
