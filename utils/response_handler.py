from flask import make_response, jsonify

def response_handler(data: dict = {}, statusCode: int = 200, cookies: dict = None):
    response = make_response(jsonify(data), statusCode)
    print("cookies", cookies)
    if cookies:
        for key, value in cookies.items():
            response.set_cookie(key, value)
    return response
