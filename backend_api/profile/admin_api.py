from typing import List

from ninja import Router
from .models.profile import get_profile_or_404, Profile
from .models.contact import contacted_with
from .schemas import ContactRead

from app.admin_auth import AdminAuthBearer
from utils.models import ErrorMessage

profile_admin_router = Router(auth=AdminAuthBearer())


@profile_admin_router.post("/contact-users", response=List[ContactRead])
def contact_users(request, first_user_id: int, second_user_id: int):
    first_user: Profile = get_profile_or_404(first_user_id)
    second_user: Profile = get_profile_or_404(second_user_id)

    contact_1 = contacted_with(first_user, second_user_id)
    contact_2 = contacted_with(second_user, first_user_id)

    return [contact_1, contact_2]

