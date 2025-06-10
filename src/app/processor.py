"""Processor module for supply chain signal extraction.

Analyzes text-based data for supply disruptions, vendor risk,
or logistical constraints using basic keyword matching.
"""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import validate_dict

# Initialize module logger
logger = setup_logger(__name__)

# Sample keywords per category (customize as needed)
DISRUPTION_KEYWORDS = {"delay", "shortage", "disruption", "backlog", "unavailable"}
RISK_KEYWORDS = {"fraud", "bankruptcy", "recall", "compliance", "violation"}
LOGISTICS_KEYWORDS = {"port", "shipping", "freight", "logistics", "transit"}


def process(payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Process a batch of supply chain-related messages.

    Detects keywords indicating supply chain issues or risks and
    annotates the payload with simplified tags.

    Parameters
    ----------
    payloads : list[dict[str, Any]]
        Incoming messages to process.

    Returns
    -------
    list[dict[str, Any]]
        Enriched messages with issue classification.
    """
    results: list[dict[str, Any]] = []

    for item in payloads:
        if not validate_dict(item, ["text"]):
            logger.warning("⚠️ Skipping message: missing required 'text' field: %s", item)
            continue

        text = item.get("text", "").lower()
        tags: list[str] = []

        try:
            if any(word in text for word in DISRUPTION_KEYWORDS):
                tags.append("disruption")
            if any(word in text for word in RISK_KEYWORDS):
                tags.append("vendor_risk")
            if any(word in text for word in LOGISTICS_KEYWORDS):
                tags.append("logistics_issue")

            item["supplychain_tags"] = tags or ["unclassified"]
            results.append(item)
        except Exception as e:
            logger.exception("❌ Failed to process item: %s | Error: %s", item, e)

    return results
