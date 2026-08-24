import uuid
from contextvars import ContextVar

correlation_id = ContextVar("correlation_id", default=str(uuid.uuid4()))
