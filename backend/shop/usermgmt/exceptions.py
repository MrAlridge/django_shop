# 定义自定义异常类
from urllib import response
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response

class CustomValidationError(APIException):
    status_code = 400
    default_detail = 'Invalid input data.'
    default_code = 'invalid'

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)  # * 先调用DRF默认的异常处理

    if response is not None:    # 如果DRF默认处理返回了响应
        if isinstance(exc, CustomValidationError):  # ? 如果是自定义的CustomValidationError异常
            response.data['custom_error_code'] = 'CUSTOM_VALIDATION_ERROR'  # 添加自定义错误代码
            response.data['message'] = exc.default_detail # 添加自定义错误信息

    return response
