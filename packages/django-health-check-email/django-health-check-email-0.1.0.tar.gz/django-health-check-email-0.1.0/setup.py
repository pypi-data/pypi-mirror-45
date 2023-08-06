# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['health_check_email']

package_data = \
{'': ['*']}

install_requires = \
['django-health-check>=3.9,<4.0']

setup_kwargs = {
    'name': 'django-health-check-email',
    'version': '0.1.0',
    'description': 'Add email check to django-health-check.',
    'long_description': '# django-health-check-email\n\nThis is a plugin for [django-health-check](https://github.com/KristianOellegaard/django-health-check), which check that your app can send emails through the email backend configured in your Django settings.\n\n## Installation\n\nInstall with pip in your environment:\n\n```bash\npip install django-health-check django-health-check-email\n```\n\nAdd the app to your `INSTALLED_APPS`:\n\n```python\nINSTALLED_APPS = [\n    # ...\n    \'health_check\',                             # required\n    # ...\n    \'health_check_email\',\n]\n```\n\nApply migrations:\n\n```bash\npython manage.py migrate\n```\n\n## Configuration\n\nAdd your settings to `HEALTH_CHECK`:\n\n```python\nHEALTH_CHECK = {\n    "EMAIL_ENABLED": True,\n    "EMAIL_IS_CRITICAL": True,\n    "EMAIL_SUBJECT": "my email health check",\n    "EMAIL_MESSAGE": "my message",\n    "EMAIL_FROM": "test@example.com",\n    "EMAIL_TO": ["admin@example.com", "dev@example.com"],\n}\n```\n',
    'author': 'Nicolas KAROLAK',
    'author_email': 'nicolas.karolak@ubicast.eu',
    'url': 'https://www.ubicast.eu',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
