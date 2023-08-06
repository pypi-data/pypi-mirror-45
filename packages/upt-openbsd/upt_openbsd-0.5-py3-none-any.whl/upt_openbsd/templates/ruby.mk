{% extends 'base.mk' %}

{% block modules %}
MODULES=		lang/ruby
CONFIGURE_STYLE=	ruby gem # XXX Maybe "ext" as well'
{% endblock %}

{% block build_deps %}
{% if pkg.run_depends %}
BUILD_DEPENDS=		${RUN_DEPENDS}
{% endif %}
{% endblock %}
