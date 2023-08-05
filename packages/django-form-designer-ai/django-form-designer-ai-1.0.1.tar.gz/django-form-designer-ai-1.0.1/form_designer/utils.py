import hashlib

from django.utils.crypto import get_random_string
from django.template import Context, Template, TemplateSyntaxError


def get_random_hash(length=32):
    return hashlib.sha1(get_random_string().encode("utf8")).hexdigest()[:length]


def string_template_replace(text, context_dict):
    try:
        t = Template(text)
        return t.render(Context(context_dict))
    except TemplateSyntaxError:
        return text
