SUPER_ADMIN_GROUP_NAME = "Super Admin"


def site_auth_nav(request):
    user = request.user
    is_super_admin = user.is_authenticated and (
        user.is_superuser
        or user.groups.filter(name=SUPER_ADMIN_GROUP_NAME).exists()
    )
    return {"user_is_super_admin": is_super_admin}
