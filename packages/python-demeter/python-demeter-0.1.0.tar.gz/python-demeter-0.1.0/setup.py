from setuptools import setup

install_requires = [
    'oauth2client',
    'google-api-python-client',
    'google-auth-httplib2',
    'google-auth-oauthlib'
    ]

setup(
    name='python-demeter',
	version='0.1.0',
	description='Extremely limited library for downloading files from Google Drive.',
	author='Jerome Montino',
    author_email='jerome.montino@gmail.com',
    url='https://github.com/jerome-montino/demeter',
    license='MIT',
    py_modules=['demeter'],
    install_requires=install_requires
)