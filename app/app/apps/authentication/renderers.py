from app.apps.core.renderers import CustomJSONRender

class UserJSONRenderer(CustomJSONRender):
    object_label = 'user'
    pagination_object_label = 'users'
    pagination_count_label = 'usersCount'

    def render(self, data, media_type=None, renderer_context=None):
        token = data.get('token', )
        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super().render(data, media_type, renderer_context)