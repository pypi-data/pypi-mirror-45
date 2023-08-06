# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ratelimit']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.0']

setup_kwargs = {
    'name': 'django-fast-ratelimit',
    'version': '0.2',
    'description': 'Fast ratelimit implementation with django caches',
    'long_description': '# django-fast-ratelimit\n\n\nDjango-fast-ratelimit provides a secure and fast ratelimit facility based on the django caching framework.\n\n\n## Installation\n\n```` bash\npip install django-fast-ratelimit\n\n````\n\nNote: pip >= 19 is required, I use the novel pyproject.toml method\n\n## usage\n\n\nDecorator:\n\n```` python\nimport ratelimit\n\n@ratelimit.decorate(key="ip", rate="1/s")\ndef expensive_func(request):\n    # how many ratelimits request limiting\n    if request.ratelimit["request_limit"] > 0:\n        # reschedule with end of rate epoch\n        return request_waiting(request.ratelimit["end"])\n\n````\n\nblocking Decorator (raises RatelimitError):\n\n```` python\nimport ratelimit\n\n@ratelimit.decorate(key="ip", rate="1/s", block=True, methods=ratelimit.UNSAFE)\ndef expensive_func(request):\n    # how many ratelimits request limiting\n    if request.ratelimit["end"] > 0:\n\n````\n\n\n\ndecorate View (requires group):\n\n```` python\nimport ratelimit\nfrom django.views.generic import View\nfrom django.utils.decorators import method_decorator\n\n\n@method_decorator(ratelimit.decorate(\n  key="ip", rate="1/s", block=True, methods=ratelimit.SAFE, group="required"\n), name="dispatch")\nclass FooView(View):\n    ...\n````\n\nmanual\n```` python\nimport ratelimit\n\n\ndef func(request):\n    ratelimit.get_ratelimit(key="ip", rate="1/s", request=request, group="123")\n    # or only for GET\n    ratelimit.get_ratelimit(\n        key="ip", rate="1/s", request=request, group="123", methods="GET"\n    )\n    # also simple calls possible (note: key in bytes format)\n    ratelimit.get_ratelimit(\n        key=b"abc", rate="1/s", group="123"\n    )\n\n````\n\n\n\n\n## TODO\n\n* more documentation\n',
    'author': 'Alexander Kaftan',
    'author_email': None,
    'url': 'https://https://github.com/devkral/django-fast-ratelimit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
