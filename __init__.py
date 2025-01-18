from homeassistant.core import HomeAssistant
from .binary_sensors_last_update import async_setup

async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    return await async_setup(hass, {})

