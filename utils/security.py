from utils.response import CustomResponse
from db.user import UserAuth, AccessKey
from django.http import HttpRequest
from utils.types import AccessKeyScope
from db.candidate import CandidateProfile


def require_app_key(func):
    def wrapper(*args, **kwargs):
        try:
            request :HttpRequest= args[1]
            app_key = request.GET.get('APP_KEY')
            if app_key is None:
                return CustomResponse("App Key is required!").send_failure_response(400)
            user = UserAuth.objects.filter(app_key=app_key).first()
            if user is None:
                return CustomResponse("Invalid App Key!").send_failure_response(400)
            args[1].user = user
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while validating app key!").send_failure_response(500)
        return func(*args, **kwargs)
    return wrapper

def require_access_key(scope:AccessKeyScope):
    def decorator(view_func):
        def wrapped_view_func(obj, request, *args, **kwargs):
            try:
                access_key = request.GET.get('ACCESS_KEY')
                if access_key is None:
                    return CustomResponse("Access Key is required!").send_failure_response(400)
                key = AccessKey.objects.filter(key=access_key).first()
                if key is None:
                    return CustomResponse("Invalid Access Key!").send_failure_response(400)
                if key.scope != scope:
                    return CustomResponse("Invalid Access key used!").send_failure_response(400)
                if scope == AccessKeyScope.CANDIDATE_PROFILE.value:
                    candidate = CandidateProfile.objects.filter(userId=key.userId.id).first()
                    print("Candidate",candidate)
                    request.candidate = candidate
                    request.user = key.userId
                return view_func(obj, request, *args, **kwargs)
            except Exception as e:
                print(e)
                return CustomResponse("Error Occured while validating access key!").send_failure_response(500)
        return wrapped_view_func
    return decorator
