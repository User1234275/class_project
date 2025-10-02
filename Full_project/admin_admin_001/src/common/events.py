from .logger import logger

def publish_event(event_name: str, payload: dict):
    logger.info("Event published: %s %s", event_name, payload)
