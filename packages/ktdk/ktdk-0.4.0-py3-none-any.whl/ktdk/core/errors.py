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


class DeclarativeError(KTDKError):
    def __init__(self, msg: str = None):
        super(DeclarativeError, self).__init__(msg=msg)


class DeclSchemaError(KTDKError):
    def __init__(self, msg: str = None):
        super(DeclSchemaError, self).__init__(msg=msg)


class DeclAttributeMissingError(DeclSchemaError):
    def __init__(self, attribute: str = None):
        msg = f"Attribute missing in the schema: {attribute}"
        super(DeclSchemaError, self).__init__(msg=msg)


class DeclMatcherNotExistError(DeclarativeError):
    def __init__(self, schema=None):
        msg = f"Matcher not found for the check: {schema}"
        super(DeclMatcherNotExistError, self).__init__(msg=msg)


class DeclRegistryNotFoundError(DeclarativeError):
    def __init__(self, which=None, name=None):
        msg = f"{which} not found: {name}"
        super(DeclRegistryNotFoundError, self).__init__(msg=msg)


class FileNotExists(KTDKError):
    pass
