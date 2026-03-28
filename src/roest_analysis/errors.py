class RoestAnalysisError(Exception):
    pass


class ConfigurationError(RoestAnalysisError):
    pass


class ApiError(RoestAnalysisError):
    pass


class NotFoundError(ApiError):
    pass
