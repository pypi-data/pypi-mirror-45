

class TYPE_NOT_DEFINED(Exception):
    """Raised when the requested data type has not been defined in the library"""
    def __init___(self,dErrorArguments):
        Exception.__init__(self,"exception was raised with arguments {0}".format(dErrArguments))
        self.dErrorArguments = dErrorArguements

class TABLE_NOT_FOUND(Exception):
    """"""
    pass

class STATEMENT_EXCEPTION(Exception):
    pass    
