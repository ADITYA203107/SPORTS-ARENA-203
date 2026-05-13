"""Who may open / post in a learner ↔ academy chat thread."""

from .models import Academy


def user_can_access_chat_room(request, room) -> bool:
    """
    Learners always access their own thread.
    Academy side: designated owner, or any academy-role user if owner is unset
    (first responder becomes owner so replies work without a prior approval step).
    """
    user = request.user
    if not user.is_authenticated:
        return False
    if user.id == room.learner_id:
        return True
    acad = room.academy
    if acad.owner_id:
        return user.id == acad.owner_id
    if getattr(user, 'role', None) == 'academy':
        Academy.objects.filter(pk=acad.pk, owner__isnull=True).update(owner=user)
        return True
    return False


def user_can_send_in_chat_room(request, room) -> bool:
    return user_can_access_chat_room(request, room)
