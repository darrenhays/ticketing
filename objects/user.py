from objects.abstract_model_object import AbstractModelObject


class User(AbstractModelObject):
    __attributes = {}
    sensitive_attributes = ['password']
    allowed_attributes = [
        'email',
        'first_name',
        'last_name',
        'parent_user_id'
    ] + sensitive_attributes
