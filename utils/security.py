from utils.response import CustomResponse
from db.user import UserAuth
from django.http import HttpRequest
def require_app_key(func):
    def wrapper(*args, **kwargs):
        request :HttpRequest= args[1]
        app_key = request.GET.get('APP_KEY')
        if app_key is None:
            return CustomResponse("App Key is required!").send_failure_response(400)
        user = UserAuth.objects.filter(app_key=app_key).first()
        if user is None:
            return CustomResponse("Invalid App Key!").send_failure_response(400)
        args[1].user = user
        return func(*args, **kwargs)
    return wrapper