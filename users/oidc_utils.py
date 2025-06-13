
def oidc_userinfo(claims, user):
    """
    Формирует payload для userinfo endpoint, на основе стандартных claims и вашей модели User.
    `claims` — уже сформированные базовые claims, можно расширять.
    `user` — экземпляр вашей модели User.
    """
    return {
        'sub': str(user.id),
        'name': user.full_name,
        'preferred_username': user.username,
        'email': user.email,
    }