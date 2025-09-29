import logging
import sys
from typing import Any, Dict

import structlog
from structlog.types import Processor

from app.core.config import get_settings


def add_request_context(
	_logger: Any, _method_name: str, event_dict: Dict[str, Any]
) -> Dict[str, Any]:
	"""Add request context to log entries if available."""
	return event_dict


def setup_logging() -> None:
	"""Configure comprehensive structured logging."""
	settings = get_settings()

	processors: list[Processor] = [
		structlog.contextvars.merge_contextvars,
		structlog.processors.add_log_level,
		structlog.processors.TimeStamper(fmt='iso'),
		add_request_context,
		structlog.processors.StackInfoRenderer(),
	]

	if settings.log_format == 'json':
		processors.extend([structlog.dev.set_exc_info, structlog.processors.JSONRenderer()])
	else:
		processors.extend([structlog.dev.set_exc_info, structlog.dev.ConsoleRenderer(colors=True)])

	structlog.configure(
		processors=processors,
		wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, settings.log_level)),
		logger_factory=structlog.WriteLoggerFactory(file=sys.stdout),
		cache_logger_on_first_use=True,
	)

	logging.basicConfig(
		format='%(message)s',
		stream=sys.stdout,
		level=getattr(logging, settings.log_level),
	)

	logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
	logging.getLogger('uvicorn.error').setLevel(logging.INFO)


def get_logger(name: str = '') -> structlog.BoundLogger:
	"""Get a structured logger instance."""
	return structlog.get_logger(name)
