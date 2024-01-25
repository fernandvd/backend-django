from app.apps.core.renderers import CustomJSONRender

class ProfileJSONRenderer(CustomJSONRender):
    object_label = 'profile'
    pagination_object_label = 'profiles'
    pagination_count_label = 'profilesCount'
