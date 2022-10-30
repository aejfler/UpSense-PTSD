from django.core.exceptions import ValidationError


def validate_intensity(obj):
    obj = int(obj)
    if obj not in range(0, 11):
        raise ValidationError(f'Intensity must be in range from 1 to 10!')
