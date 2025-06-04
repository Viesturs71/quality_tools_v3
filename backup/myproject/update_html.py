import dominate
from dominate.tags import *
from dominate.util import raw

# Izveido jaunu HTML dokumentu
doc = dominate.document(title='Management System Tools')

# Pievieno CSS un JS failus
with doc.head:
    link(rel='stylesheet', href='{% static "admin/css/custom_admin.css" %}')
    script(src='{% static "bootstrap/js/bootstrap.bundle.min.js" %}')
    script(src='{% static "admin/js/custom_admin.js" %}')

# Pievieno branding bloku
with doc:
    raw('{% block branding %}')
    raw('{% include "admin/includes/header.html" %}')
    raw('{% endblock %}')

# Pievieno usertools bloku
with doc:
    raw('{% block usertools %}')
    with div(id='user-tools'):
        with form(action='{% url "set_language" %}', method='post', klass='d-inline'):
            raw('{% csrf_token %}')
            input(type='hidden', name='next', value='{{ request.path }}')
            with select(name='language', klass='form-select', onchange='this.form.submit()'):
                raw('{% get_current_language as LANGUAGE_CODE %}')
                raw('{% get_available_languages as LANGUAGES %}')
                raw('{% for lang_code, lang_name in LANGUAGES %}')
                option(value='{{ lang_code }}', selected='{{ "selected" if lang_code == LANGUAGE_CODE else "" }}')(
                    raw('{% if lang_code == "lv" %}Latviešu{% else %}{{ lang_name }}{% endif %}')
                )
                raw('{% endfor %}')
            raw('{{ block.super }}')
    raw('{% endblock %}')

# Pievieno nav-global bloku
with doc:
    raw('{% block nav-global %}')
    raw('{# Navbar disabled – using custom header for language switch #}')
    raw('{% endblock %}')

# Pievieno sidebar bloku
with doc:
    raw('{% block sidebar %}')
    raw('{% include "admin/includes/nav.html" %}')
    raw('{% endblock %}')

# Pievieno footer bloku
with doc:
    raw('{% block footer %}')
    raw('{% include "admin/includes/footer.html" %}')
    raw('{% endblock %}')

# Pievieno extrahead bloku
with doc.head:
    raw('{% block extrahead %}')
    raw('{% endblock %}')

# Saglabāj dokumentu kā failu
with open('base_site.html', 'w') as file:
    file.write(doc.render())
