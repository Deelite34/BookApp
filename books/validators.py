import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_publication_date(date):
    """
    Ensure that inputed date does not represent future.
    :param date: datetime.datetime object
    """
    current_date = datetime.datetime.now().date()
    if date > current_date:
        raise ValidationError(
            _('%(value)s Data publikacji nie może być w przyszłości!'),
            params={'value': date},
        )
