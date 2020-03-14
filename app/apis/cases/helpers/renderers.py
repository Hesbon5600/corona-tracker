import json
from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import JSONRenderer


class RequestJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        errors = None
        errors = data.get('errors', None)
        if data and data.get('detail', '') and isinstance(data.get('detail', ''), ErrorDetail):
            errors = data['detail']
        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            data['status'] = 'failed'
            return super(RequestJSONRenderer, self).render(data)

        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'data': data,
            'status': 'success'
        })
