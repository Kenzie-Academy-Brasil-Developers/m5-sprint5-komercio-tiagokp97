class SerializerByMethodMixin:
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'PATCH':
            self.check_object_permissions(self.request, self.get_object())
        return self.serializer_map.get(self.request.method, self.serializer_class)

