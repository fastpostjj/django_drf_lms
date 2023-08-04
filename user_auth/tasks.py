from user_auth.services.services import check_user_last_login

def task_check_last_login(*args, **kwargs):
    check_user_last_login(args)