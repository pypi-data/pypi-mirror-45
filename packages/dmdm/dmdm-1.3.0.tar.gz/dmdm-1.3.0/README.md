#  Django MarkDown Mail
[![PyPI version](https://badge.fury.io/py/dmdm.svg)](https://pypi.org/project/dmdm)
[![Build Status](https://travis-ci.org/nim65s/dmdm.svg?branch=master)](https://travis-ci.org/nim65s/dmdm)
[![Coverage Status](https://coveralls.io/repos/github/nim65s/dmdm/badge.svg?branch=master)](https://coveralls.io/github/nim65s/dmdm?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/6737a84239590ddc0d1e/maintainability)](https://codeclimate.com/github/nim65s/dmdm/maintainability)

Write your email in markdown, and send them in txt & html.

## Requirements

- Python 3.4+
- Django 2.0+
- [yejianye/mdmail](https://github.com/yejianye/mdmail)

## Install

`pip install dmdm`

## Usage

This replaces django's `django.core.email.send_mail`, but the mail will have an html alternative rendered from the text
part with markdown. You can also provide a custon `css` and even images (that will be inlined) located in `image_root`.


```python
from dmdm import send_mail

send_mail(subject, message, from_email, recipient_list, context=None, request=None, fail_silently=False, css=None,
          image_root='.', auth_user=None, auth_password=None, connection=None)
```

If you want to write your markdown in a template, just put the name of the template in `message` and add a `context`
(which can be `{}`) and eventually a `request`:

```
send_mail(subject, 'test_email_template.md', from_email, recipient_list, {'template_variable': 'value'})
```
