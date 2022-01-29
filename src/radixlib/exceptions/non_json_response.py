class NonJsonResponseError(Exception):
    """ An exception raised when the response to the provider is not a valid JSON response. """