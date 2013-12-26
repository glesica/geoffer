try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Geoffer',
    'author': 'George Lesica',
    'url': 'https://github.com/glesica/geoffer',
    'download_url': 'https://github.com/glesica/geoffer',
    'author_email': 'george@lesica.com',
    'version': open('VERSION', 'r').read().strip(),
    'install_requires': ['nose'],
    'packages': ['geoffer'],
    'scripts': [],
    'name': 'geoffer'
}

setup(**config)
