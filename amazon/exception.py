"""
.. module:: exception

"""

class AmazonException(Exception):
    """
        Class representing an exception raised by any call

        Properties
            *status (string)*
                type of exception
            *reason (string, object)*
                detail of the exception

    """
    def __init__(self, status=None, reason=None):
        """init function"""
        self.status = status
        self.reason = reason
        

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\n"\
                        "Reason: {1}\n".format(self.status, self.reason)

        return error_message
