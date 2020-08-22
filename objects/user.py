from objects.abstract_object import AbstractObject


class User(AbstractObject):
    __attributes = {}
    sensitive_attributes = ['password']
    allowed_attributes = [
        'id',
        'created',
        'updated',
        'email',
        'first_name',
        'last_name'
    ] + sensitive_attributes
