from werkzeug.exceptions import InternalServerError


class ServiceError(InternalServerError):
    pass
