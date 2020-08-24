from objects.abstract_model_object import AbstractModelObject


class Ticket(AbstractModelObject):
    allowed_attributes = [
        'id',
        'event_id',
        'event_title',
        'event_description',
        'ticket_type_id',
        'ticket_type_title',
        'ticket_type_description',
        'amount_paid'
    ]
