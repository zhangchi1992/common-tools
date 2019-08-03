from setuptools import setup, find_packages
setup(
    name='disktool',
    version='1.0.0',
    description='Disk tool that integrates smartool and megacli information',
    keywords='qingstor cli smartool megacli',
    author='Yunify Qingstor Team',
    author_email='zhangchi@yunify.com',
    packages=find_packages('.'),
    scripts=['bin/disktool'],
)
