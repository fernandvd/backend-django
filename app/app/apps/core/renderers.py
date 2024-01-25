import json 
from rest_framework.renderers import JSONRenderer
from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS,
)

class CustomJSONRender(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    pagination_object_label = 'objects'
    pagination_object_count = 'count'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return super().render(data, accepted_media_type, renderer_context)
        
        if data.get('results', None) is not None:
            return json.dumps({
                self.pagination_object_label: data['results'],
                self.pagination_count_label: data['count'],
            })
        
        elif data.get('errors') is not None:
            return super().render(data, accepted_media_type, renderer_context)
        else:
            indent = self.get_indent(accepted_media_type, renderer_context)

            if indent is None:
                separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
            else:
                separators = INDENT_SEPARATORS
            ret = json.dumps({
                self.object_label: data,
            }, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators)

            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')

            return ret.encode()