

class AmazonException(Exception):

    def __init__(self, status=None, reason=None):
        
        self.status = status
        self.reason = reason
        

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\n"\
                        "Reason: {1}\n".format(self.status, self.reason)

        return error_message
