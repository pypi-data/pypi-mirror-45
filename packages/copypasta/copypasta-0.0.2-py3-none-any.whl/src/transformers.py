'''
Transformers that inflate template files

- TODO transformers should define allowed extensions and be registered into the main context,
where the allowed extensions get mapped to their instance.
Also makes transformers more pluggable
'''
import os
from jinja2 import Template, StrictUndefined

DEFAULT_J2_PARAMS = {'undefined': StrictUndefined}


class Jinja2Transformer(object):
    file_extensions = set(['.j2'])

    def __init__(self, j2_params=None):
        if not j2_params:
            j2_params = DEFAULT_J2_PARAMS
        self.j2_params = j2_params

    def transform_string(self, s, params=None):
        if not params:
            return Template(s, **self.j2_params).render()
        return Template(s, **self.j2_params).render(params)

    def transform(self, src, dst, params):
        dst = os.path.splitext(dst)[0]
        with open(src, 'r') as f:
            contents = f.read()
            # TODO dont crash when there are undefined variables, catch and prompt
            transformed_contents = self.transform_string(contents, params)
            with open(dst, 'w') as outf:
                outf.write(transformed_contents)
