import logging
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config):
    """Set up the binary_sensors_history integration."""
    _LOGGER.info("async_setup called for binary_sensors_history")

    async def log_test(call: ServiceCall):  # Add 'call' as argument
        """Log a message when the service is called."""
        _LOGGER.info("PIPPO")  # You can also log 'call' data here if needed
        # Example: _LOGGER.info(f"Service called with data: {call.data}")

    hass.services.async_register(
        "binary_sensors_history", "log_test", log_test
    )

    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up the binary_sensors_history integration from a config entry."""
    _LOGGER.info("async_setup_entry called for binary_sensors_history")
    return await async_setup(hass, entry.data)
