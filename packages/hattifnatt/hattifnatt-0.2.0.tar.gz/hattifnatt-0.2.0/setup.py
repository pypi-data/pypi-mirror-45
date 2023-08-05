from setuptools import setup

with open('README.rst', 'r') as fp:
	for line in fp:
		if not line[:-1]: break
	readme = ''.join(line for line in fp)

setup(
	name='hattifnatt',
	version='0.2.0',
	author='Alexander Shpilkin',
	author_email='ashpilkin@gmail.com',
	description='Push directory to Telegram channel',
	long_description=readme,
	long_description_content_type='text/x-rst',
	url='https://github.com/alexshpilkin/hattifnatt',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: End Users/Desktop',
		'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Communications :: Chat',
		'Topic :: Communications :: File Sharing',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Utilities',
	],

	py_modules=['hattifnatt'],
	entry_points={
		'console_scripts': [
			'hat = hattifnatt:main',
		],
	},
	python_requires='>=3.5, <4',
	install_requires=[
		'pathtools >=0.1.2',
		'python-telegram-bot >=10.0.2, <12',
		'watchdog >=0.9.0',
	]
)
