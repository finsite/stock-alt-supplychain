"""Main entry point for the service.

This script initializes logging, loads the queue consumer,
and begins consuming data using the configured processing callback.
"""

import os
import sys
from typing import Any

# Add 'src/' to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import config_shared
from app.output_handler import send_to_output
from app.queue_handler import consume_messages
from app.utils.setup_logger import setup_logger
from app.processor import process

# Initialize the module-level logger
logger = setup_logger(__name__)


def handle_message_batch(batch: list[dict[str, Any]]) -> None:
    """Handle incoming messages by processing and routing the results.

    Parameters
    ----------
    batch : list[dict[str, Any]]
        Raw messages consumed from the queue.
    """
    try:
        enriched = process(batch)
        if enriched:
            send_to_output(enriched)
        else:
            logger.info("ℹ️ No messages passed processing validation.")
    except Exception as e:
        logger.exception("❌ Failed to handle message batch: %s", e)


def main() -> None:
    """Start the data processing service."""
    logger.info("🚀 Starting supply chain processing service...")
    consume_messages(handle_message_batch)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("❌ Unhandled exception in main: %s", e)
        sys.exit(1)
