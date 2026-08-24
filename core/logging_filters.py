from .request_context import correlation_id


class CorrelationIdFilter:
    def filter(self, record):
        record.correlation_id = correlation_id.get()
        return True
