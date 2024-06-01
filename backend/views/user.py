from rest_framework.decorators import api_view
from backend.utils import validator
from backend.utils import response
from backend.queries.user import UserQuery


@api_view(['POST','PATCH','GET'])
def otp_view(request):
    if request.method=='POST':
        rules = {
            'mobile':{'type': 'integer', 'required': True},
            'user_type':{'type': 'string', 'required': True},
            }
        request_data = validator.validate(rules,request)
        return response.respond_201(create_otp(request_data))
    
    if request.method=='PATCH':
        rules = {
                'mobile':{'type': 'integer', 'required': True},
                'otp':{'type': 'integer', 'required': True}
                }
        request_data = validator.validate(rules,request)
        return response.respond_201(check_update_otp(request,request_data))
    
def create_otp(request_data):

    data = UserQuery().generate_new_otp(data = request_data)
    mobile = data.pop('mobile')
    is_already_registered = True if data.pop('name') else False
    output = {
        'mobile':mobile,
        "is_already_registered":is_already_registered
    }
    return output

def check_update_otp(request,request_data):
    """_summary_

    Args:
        request (_type_): WSGI Object
        request_data (_type_): request data

    Returns:
        _type_: user object in case of company else token user dict in case of User
    """
    data = UserQuery().verify_otp(request,data = request_data)
    
    return data

    