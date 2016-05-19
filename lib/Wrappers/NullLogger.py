class NullLogger:
    """
    magic method that does nothing when you call null_logger.foo(),
    null_logger.bar(), null_logger.whatever()
    """
    def __getattr__(self, item):
        return lambda *args, **kwargs: None
