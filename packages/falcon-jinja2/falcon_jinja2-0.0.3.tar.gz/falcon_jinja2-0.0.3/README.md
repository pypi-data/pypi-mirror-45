# falcon-jinja2

[![Build Status](https://travis-ci.org/mikeylight/falcon-jinja.svg?branch=master)](https://travis-ci.org/mikeylight/falcon-jinja)


Simple jinja2 support for Falcon framework.


Installation
============
```
pip install falcon-jinja2
```


Examples
========
```
import falcon

from falcon_jinja2 import FalconTemplate

# NOTE: if you want to change name of folder where your HTML files are defined
# Add `path` argument to the FalconTemplate class
#    Example:
#        falcon_template = FalconTemplate(path='path_to_your_folder')

falcon_template = FalconTemplate()

class FirstResource:
    @falcon_template.render('index.html')
    def on_get(self, req, resp):
        resp.context = {'framework': 'Falcon'}

app = falcon.API()
app.add_route('/first', FirstResource())
```

TODO
====
- [ ] Add ```url_for``` support
- [ ] Add ```flash``` messages support


Contributing
============
1. Fork the repository.
2. Create a branch with feature/fix/cleanup, and create an Pull request.
3. Have fun :)
