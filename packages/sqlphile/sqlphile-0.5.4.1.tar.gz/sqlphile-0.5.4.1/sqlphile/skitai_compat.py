try:
    from skitai.rpc.cluster_dist_call import Result

except ImportError:
    EMPTY = None

else:
    class Response:
        def __init__ (self, data):
            self.description = None
            self.data = data
            self.expt = None
            self.code, self.msg = 200, "OK"
            self.status_code, self.reason = self.code, self.msg  

    def dispatch (data):
        return Result (None, 3, Response (data), None)

    EMPTY = dispatch ([])    
