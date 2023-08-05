class KTDKError(Exception):
    def __init__(self, msg: str = None, **kwargs):
        super().__init__()
        self.msg = msg

    def __str__(self):
        return f"{self.__class__.__name__}: {self.msg}"


class KTDKAssertionError(KTDKError):
    pass


class RequireFailedError(KTDKAssertionError):
    pass


class KillCheckError(KTDKAssertionError):
    pass


class RequiredTaskFailed(KTDKAssertionError):
    pass


class TaskRunFailed(KTDKError):
    pass


class ContextIsNotInitializedError(KTDKError):
    def __init__(self, class_name: str):
        message = f'Context has not been initialized yet for class: {class_name}'
        super(ContextIsNotInitializedError, self).__init__(msg=message)
