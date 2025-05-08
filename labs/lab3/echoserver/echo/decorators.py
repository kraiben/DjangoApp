from django.contrib.auth.decorators import login_required, user_passes_test

def user_required(view_func):
    return login_required(view_func)

def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_admin(),
        login_url='/login/'
    )(view_func)