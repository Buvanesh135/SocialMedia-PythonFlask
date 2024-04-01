""" Errors and Exceptions """


class APIError(Exception):
    """ API Error Base Class """

    def __init__(self, error_description, status=None, data=None, *args, **kwargs):
        super(APIError, self).__init__(*args, **kwargs)
        if type(error_description) is dict:
            self.error_code = error_description.get('code', None)
            self.description = error_description.get('message', '')
            self.server_error = error_description.get('server_error', True)
        else:
            self.error_code = None
            self.description = error_description
            self.server_error = True
        self.data = data
        self.status = status


class NotFoundError(APIError):
    """ `NotFoundError` """
    code = 404


class InvalidData(APIError):
    """ Conflict in data """
    code = 400


class ServerError(APIError):
    """ Server error """
    code = 500


class InsufficientData(APIError):
    """ Data is insufficient """
    code = 422


class UnauthorizedError(APIError):
    """ Unauthorized access """
    code = 401


class ForbiddenError(APIError):
    """ Token validation failed """
    code = 403


class ThirdPartyApiError(APIError):
    """ 3rd party api failure """
    code = 503

