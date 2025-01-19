from homeassistant.core import HomeAssistant
from .binary_sensors_history import async_setup

async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Set up the binary_sensors_history integration from a config entry."""
    return await async_setup(hass, entry.data)
