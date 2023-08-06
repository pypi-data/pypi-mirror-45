{% extends 'base.mk' %}

{% block version %}
MODPY_EGG_VERSION=	{{ pkg.upt_pkg.version }}
{% endblock %}

{% block modules %}
MODULES=		lang/python
MODPY_SETUPTOOLS=	Yes
MODPY_PI=		Yes

FLAVORS =		python3
FLAVOR ?=
{% endblock %}
