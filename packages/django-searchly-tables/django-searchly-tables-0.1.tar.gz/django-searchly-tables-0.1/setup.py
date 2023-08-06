import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
	README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name = 'django-searchly-tables',
	version = '0.1',
	packages = find_packages(),
	include_pakage_data=True,
	license = 'MIT License',
	description = 'A simple Django app that adds search and sort to HTML tables.',
	long_description = README,
	url = 'https://github.com/peterschueler/django-searchly-tables',
	author = 'Peter Schueler',
	author_email = 'peter@orangemirrorentertainment.com',
	classifiers = [
		'Environment :: Web Environment',
		'Framework :: Django',
		'Framework :: Django :: 2.1',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.7',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
)