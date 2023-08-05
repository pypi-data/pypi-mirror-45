from setuptools import setup, find_packages

from install_requirements import get_required_packages
from version import get_package_version

setup(
    name='django-config-initializer-dev',
    version=get_package_version(),
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='BSD License',
    author='lior.yehonatan',
    author_email='lior.yehonatan@inel.com',
    description='a small package to support loading configuration from local yaml in dev environment',
    python_requires='>=3.6',
    install_requires=get_required_packages()
)

