[![Build Status](https://travis-ci.org/Frojd/django-react-templatetags.svg?branch=master)](https://travis-ci.org/Frojd/django-react-templatetags)
[![PyPI version](https://badge.fury.io/py/django_react_templatetags.svg)](https://badge.fury.io/py/django_react_templatetags)

# Django-React-Templatetags

This django library allows you to add React (16+) components into your django templates.


## Index

- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Setup](#quick-setup)
- [Usage](#usage)
- [Settings](#settings)
- [Examples](#examples)
- [Example Application](#example-application)
- [Working With Models](#working-with-models)
- [Server Side Rendering](#server-side-rendering)
- [FAQ](#faq)
- [Tests](#tests)
- [Contributing](#contributing)
- [License](#license)


## Requirements

- Python 2.7 / Python 3.5+ / PyPy
- Django 1.11+


## Installation

Install the library with pip:

```
$ pip install django_react_templatetags
```


## Quick Setup

Make sure `django_react_templatetags` is added to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = (
    # ...
    'django_react_templatetags',
)
```

You also need to add the `react_context_processor` into the `context_middleware`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates...',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                ...
                'django_react_templatetags.context_processors.react_context_processor',
            ],
        },
    },
]
```

This should be enough to get started.


## Usage

1. Load the `{% load react %}`
2. Insert the component anywhere in your template: `{% react_render component="Component" props=my_data %}`. This will create a dom placeholder.
3. Put `{% react_print %}` in the end of your template. (This will output `ReactDOM.render()`/`ReactDOM.hydrate()` javascript).
3. Make sure `React` and `ReactDOM` are included and that `ReactDOM` are exposed globally in js (ex `window.ReactDOM = ReactDOM`)


## Settings

### General

- `REACT_COMPONENT_PREFIX`: Adds a prefix to your React.createElement include, if you want to retrive your components from somewhere else then the global scope. (Default is `""`).
    - Example using (`REACT_COMPONENT_PREFIX="Cookie."`) will look for components in a global scope object named `Cookie`.
    - ...Becomes: `React.createElement(Cookie.MenuComponent, {})`
- `REACT_RENDER_TAG_MANAGER`: This is a advanced setting that lets you replace our tag parsing rules (ReactTagManager) with your own. (Default is `""`)
    - Example: `"myapp.manager.MyReactTagManager"`

### SSR (Server Side Rendering)

- `REACT_RENDER_HOST`: Which endpoint SSR requests should be posted at. (Default is `""`)
    - Example: `http://localhost:7000/render-component/`
    - The render host is a web service that accepts a post request and and renders the component to HTML. (This is what our [Hastur](https://github.com/Frojd/hastur) service does)
- `REACT_RENDER_TIMEOUT`: Timeout for SSR requests, in seconds. (Default is `20`)
- `REACT_RENDER_HEADERS`: Override the default request headers sent to the SSR service. Default: `{'Content-type': 'application/json', 'Accept': 'text/plain'}`.
    - Example: `REACT_RENDER_HEADERS = {'Authorization': 'Basic 123'}`


## Examples

### Single Component Example

This view...

```python
from django.shortcuts import render

def menu_view(request):
    return render(request, 'myapp/index.html', {
        'menu_data': {
            'example': 1,
        },
    })
```

... and this template:

```html
{% load react %}
<html>
    <head>...</head>

    <body>
        <nav>
            {% react_render component="Menu" props=menu_data %}
        </nav>
    </body>

    {% react_print %}
</html>
```

Will transform into this:

```html
<html>
    <head>...</head>

    <body>
        <nav>
            <div id="Menu_405190d92bbc4d00b9e3376522982728"></div>
        </nav>
    </body>

    <script>
        ReactDOM.render(
            React.createElement(Menu, {"example": 1}),
            document.getElementById('Menu_405190d92bbc4d00b9e3376522982728')
        );
    </script>
</html>
```

### Multi Component Example

You can also have multiple components in the same template

This view...

```python
from django.shortcuts import render

def menu_view(request):
    return render(request, 'myapp/index.html', {
        'menu_data': {
            'example': 1,
        },
        'title_data': 'My title',
        'footer_data': {
            'credits': 'Copyright Company X'
        }
    })
```

... and this template:

```html
{% load react %}
<html>
    <head>...</head>

    <body>
        <nav>
            {% react_render component="Menu" props=menu_data %}
            {% react_render component="Title" prop_title=title %}
            {% react_render component="Footer" props=footer_data %}
        </nav>
    </body>

    {% react_print %}
</html>
```

Will transform into this:

```html
<html>
    <head>...</head>

    <body>
        <nav>
            <div id="Menu_405190d92bbc4d00b9e3376522982728"></div>
        </nav>
        <main>
            <div id="Title_405190d92bbc4d00b9e3376522982728"></div>
        </main>
        <footer>
            <div id="Footer_405190d92bbc4d00b9e3376522982728"></div>
        </footer>
    </body>

    <script>
        ReactDOM.render(
            React.createElement(Menu, {"example": 1}),
            document.getElementById('Menu_405190d92bbc4d00b9e3376522982728')
        );
        ReactDOM.render(
            React.createElement(Title, {"title": "My title"}),
            document.getElementById('Title_405190d92bbc4d00b9e3376522982728')
        );
        ReactDOM.render(
            React.createElement(Footer, {"credits": "Copyright Company X"}),
            document.getElementById('Footer_405190d92bbc4d00b9e3376522982728')
        );
    </script>
</html>
```


## Example Application

Here is an [example application of a fully React-rendered Django application with react-sass-starterkit](https://github.com/mikaelengstrom/django-react-polls-example/). This was an example app for a Django-meetup talk, you might find the [slides on Slideshare](https://www.slideshare.net/Frojd/integrating-react-in-django-while-staying-sane-and-happy) helpful.


## Working with models

In this example, by adding `RepresentationMixin` as a mixin to the model, the templatetag will know how to generate the component data. You only need to pass the model instance to the `react_render` templatetag.

This model...

```python
from django.db import models
from django_react_templatetags.mixins import RepresentationMixin

class Person(RepresentationMixin, models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def to_react_representation(self, context={}):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
```

...and this view

```python
import myapp.models import Person

def person_view(request, pk):
    return render(request, 'myapp/index.html', {
        'menu_data': {
            'person': Person.objects.get(pk=pk),
        },
    })
```

...and this template:

```html
{% load react %}
<html>
    <head>...</head>

    <body>
        <nav>
            {% react_render component="Menu" props=menu_data %}
        </nav>
    </body>

    {% react_print %}
</html>
```

...will transform into this:

```html
...

<script>
    ReactDOM.render(
        React.createElement(Menu, {"first_name": "Tom", "last_name": "Waits"}),
        document.getElementById('Menu_405190d92bbc4d00b9e3376522982728')
    );
</script>
```


## Server Side Rendering

This library supports SSR (Server Side Rendering) throught third-part library [Hastur](https://github.com/Frojd/Hastur).

It works by posting component name and props to endpoint, that returns the html rendition. Payload example:

```json
{
    "componentName": "MyComponent",
    "props": {
        "title": "my props title",
        "anyProp": "another prop"
    },
    "context": {"location": "http://localhost"},
    "static": false
}
```

`REACT_RENDER_HOST` needs to be defined to enable communication with service.

You can set the context-parameter by using the `ssr_context` property on the template tag:
```html
{% react_render component="Component" ssr_context=ctx %}
```

## FAQ

<details>

### How do I override the markup generated by `react_print`?

Simple! Just override the template `react_print.html`

### This library only contains templatetags, where is the react js library?

This library only covers the template parts (that is: placeholder and js render).

### I dont like the autogenerated element id, can I supply my own?

Sure! Just add the param `identifier="yourid"` in `react_render`.

Example:
```
{% react_render component="Component" identifier="yourid" %}
```

...will print 
```html
<div id="yourid"></div>
```

### How do I pass individual props?

Add your props as arguments prefixed with `prop_*` to your `{% react_render ... %}`. 

Example: 
```html
{% react_render component="Component" prop_country="Sweden" prop_city="Stockholm" %}
```

...will give the component this payload:
```javascript
React.createElement(Component, {"country": "Sweden", "city": "Stockholm"}),
```

### How do I apply my own css class to the autogenerated element?
    
Add `class="yourclassname"` to your `{% react_render ... %}`. 
    
Example: 
```html
{% react_render component="Component" class="yourclassname" %}
```

...will print 
```html
<div id="Component_405190d92bbc4d00b9e3376522982728" class="yourclassname"></div>
```


### Can I skip SSR on a certain request?

Yup, just pass the header `HTTP_X_DISABLE_SSR` in your request and SSR will be skipped in that response.


### I want to pass the component name as a variable, is that possible?

Yes! Just remove the string declaration and reference a variable in your `{% react_render ... %}`, the same way you do with `props`.

Example:

This view

```python
render(request, 'myapp/index.html', {
    'component_name': 'MegaMenu',
})
```

...and this template

```html
{% react_render component=component_name %}
```

...will print:

```html
<div id="Component_405190d92bbc4d00b9e3376522982728" class="yourclassname"></div>
React.createElement(MegaMenu),
```

</details>


## Tests

This library include tests, just run `python runtests.py`

You can also run separate test cases: `runtests.py tests.test_filters.ReactIncludeComponentTest`


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Django-React-Templatetags is released under the [MIT License](http://www.opensource.org/licenses/MIT).
