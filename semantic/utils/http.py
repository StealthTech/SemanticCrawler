class HttpStatus:
    success = 200
    bad_request = 400
    forbidden = 403
    not_found = 404
    internal_server_error = 500


class JsonStatus:
    success = 'ok'
    fail = 'error'


class WebStatus:
    http = HttpStatus
    json = JsonStatus
