from objects.abstract_object import AbstractObject


class Ticket(AbstractObject):
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
