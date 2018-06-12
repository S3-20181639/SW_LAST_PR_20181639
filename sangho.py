#from wsgiref.simple_server import make_server
from cgi import parse_qs
import json

class RangeError(Exception):
    pass

def is_valid_range(x):
    i = int(x)
    if i < 1 or i > 1000:
        raise RangeError
    else:
        return i

def application(environ, start_response):
    path = environ['PATH_INFO'].split('/')
    request_body_size = int(environ.get('CONTENT_LENGTH', '0'))
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)
    guess = d.get('guess', [''])[0]
    dap = d.get('dap', [''])[0]

    print('method: %s' % environ['REQUEST_METHOD'])
    print('path: %s' % repr(path))
    
    v = ""

    try:
        guess_int = is_valid_range(guess)
        dap_int = is_valid_range(dap)
    except ValueError:
        v = "ValueError! Please input integer"
    except RangeError:
        v = "RangeError! Please input 1 ~ 1000 integer"

    if v != "":
        answer = v
    else:
        if guess_int > dap_int:
            answer = "Greater"
        elif guess_int == dap_int:
            answer = "Success"
        else:
            answer = "Smaller"

    response = {'answer': answer}
    response_body = json.dumps(response)

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]

if __name__ == '__main__':
    httpd = make_server(
        'localhost',
        8051,
        application
    )

    httpd.serve_forever()
