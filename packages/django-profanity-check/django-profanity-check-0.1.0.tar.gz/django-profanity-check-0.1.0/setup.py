# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['profanity', 'profanity.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['profanity-check>=1.0,<2.0']

setup_kwargs = {
    'name': 'django-profanity-check',
    'version': '0.1.0',
    'description': 'A Django template filter that wraps around profanity-check',
    'long_description': "## django-profanity-check\n\nA Django template filter that wraps around [profanity-check](https://github.com/vzhou842/profanity-check).\n\n**Note**: `numpy`, `scipy`, and `scikit-learn` are all dependencies of `profanity-check`.\n\n## Usage\n\n1. Install with `pip`.\n\n   ```\n   pip install django-profanity-check\n   ```\n\n1. Add `profanity` to your `INSTALLED_APPS`.\n\n   ```python\n   # settings.py\n\n   INSTALLED_APPS = [ ..., 'profanity', ...]\n\n   ```\n\n1. Use it in a template!\n\n   ```python-django\n   {# ... #}\n\n   {% load profanity %}\n\n   {# ... #}\n\n   {% with sentence='Hey, fuck you!' %}\n      {{ sentence | censor }} {# Will result in: 'Hey, **** you!' #}\n   {% endwith %}\n\n   ```\n\n## Todo\n\n- [ ] Allow custom replacement characters\n- [ ] Allow custom replacement character length\n- [ ] Template tests\n\n## Credits\n\nVictor Zhou's [profanity-check](https://github.com/vzhou842/profanity-check) Python package does all the heavy lifting.\n\nInspired by [django-profanity-filter](https://github.com/ReconCubed/django-profanity-filter).\n",
    'author': 'Raúl Negrón',
    'author_email': 'raul.esteban.negron@gmail.com',
    'url': 'https://github.com/rnegron/django-profanity-check',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
