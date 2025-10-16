def get_full_name(user):
     return (
        f"{user.last_name} {user.first_name} {user.middle_name or ''}"
        .strip()
    )