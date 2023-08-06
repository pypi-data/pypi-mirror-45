{% macro depends(kind, deps) %}
{%- if deps %}
{{ kind }}_DEPENDS=
    {%- for dep in deps %}
      {%- if loop.first %}
		{{ dep|reqformat }}
      {%- else %}
			{{ dep|reqformat }}
      {%- endif %}
      {% if not loop.last %} \
      {% endif %}
    {% endfor %}
{% endif -%}
{% endmacro -%}
# $OpenBSD$

COMMENT=		{{ pkg._summary() }}

{% block version %}
VERSION=		{{ pkg.upt_pkg.version }}
{% endblock %}
DISTNAME=		{{ pkg._distname() }}
PKGNAME=		{{ pkg._pkgname() }}

CATEGORIES=		XXX

HOMEPAGE=		{{ pkg.upt_pkg.homepage }}

MAINTAINER=		XXX <xxx@xxx.xxx>

{{ pkg._license_info() }}

{% block modules %}
{% endblock %}

{% block build_deps %}
{{ depends('BUILD', pkg.build_depends) }}
{% endblock %}
{% block run_deps %}
{{ depends('RUN', pkg.run_depends) }}
{% endblock %}
{% block test_deps %}
{{ depends('TEST', pkg.test_depends) }}
{% endblock %}

.include <bsd.port.mk>
