from setuptools import setup

description = '''\
`wtime` draws a weekly timetable.

Dependencies
------------

* [Python](https://www.python.org) 3.6+
* [Inkscape](https://inkscape.org) — *optional, for PNG and PDF rendering*
* [OptiPNG](http://optipng.sourceforge.net) — *optional, for PNG optimization*'''

setup(
	name = 'wtime',
	version = '0.3',
	description = 'Week Time',
	url = 'http://phyl.io/?page=wtime.html',
	author = 'Philippe Kappel',
	author_email = 'philippe.kappel@gmail.com',
	license = 'MIT',
	long_description = description,
	long_description_content_type = 'text/markdown',
	keywords = 'SVG PNG PDF',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Topic :: Multimedia :: Graphics',
		'Topic :: Office/Business :: Scheduling',
		'Topic :: Utilities'],
	packages = ['wtime'],
	entry_points = {'console_scripts': ['wtime = wtime:main']}
)