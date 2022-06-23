from django.core.exceptions import PermissionDenied


def user_is_staff(request) -> bool:
    """Проверка является ли текущий пользователь персоналом."""
    if request.user.is_superuser or request.user.is_staff:
        has_access = True
    else:
        has_access = False
    return has_access


def staff_required(function):
    """Ограничивает просмотр только для персонала."""

    def _inner(request, *args, **kwargs):
        if not user_is_staff(request):
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return _inner
