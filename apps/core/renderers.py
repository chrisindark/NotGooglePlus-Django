import json

from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    # charset = 'utf-8'
    # object_label = 'object'
    # pagination_object_label = 'objects'
    # pagination_object_count = 'count'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # if data is None:
        #     return bytes()
        #
        # renderer_context = renderer_context or {}
        # indent = self.get_indent(accepted_media_type, renderer_context)

        # if data.get('results', None) is not None:
        #     return json.dumps({
        #         self.pagination_object_label: data['results'],
        #         self.pagination_object_count: data['count']
        #     })

        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        # elif data.get('errors', None) is not None:
        #     return super(CustomJSONRenderer, self).render(data)
        #
        # else:
        #     return json.dumps({
        #         self.object_label: data
        #     })
        return super(CustomJSONRenderer, self).render(data)
