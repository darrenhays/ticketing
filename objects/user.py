from objects.abstract_model_object import AbstractModelObject


class User(AbstractModelObject):
    __attributes = {}
    sensitive_attributes = ['password']
    allowed_attributes = [
        'id',
        'email',
        'first_name',
        'last_name'
    ] + sensitive_attributes
