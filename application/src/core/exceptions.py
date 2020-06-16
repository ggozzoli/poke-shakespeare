from werkzeug.exceptions import InternalServerError


class ServiceError(InternalServerError):
    pass


class RepositoryError(Exception):
    pass
