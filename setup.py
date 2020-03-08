from setuptools import setup, find_packages

setup (
	name='iudx',
	version='0.0.1',
	packages=find_packages(),
	install_requires=['requests', 'urllib3'],
	url='https://github.com/iudx/iudx-python-sdk',
	license='ISC',
	author='IUDX Team',
	author_email='contact@iudx.org.in',
	description='Simple Python SDK for IUDX.'
)
