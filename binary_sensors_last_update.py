import logging
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import service
import sqlite3

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config):
    _LOGGER.info("Setting up binary_sensors_last_update component")
    
    conn = sqlite3.connect('/config/home-assistant_v2.db')
    cursor = conn.cursor()
    
    async def read_data(call: ServiceCall):
        cursor.execute("SELECT * FROM binary_sensors_last_update")
        data = cursor.fetchall()
        _LOGGER.info("Data fetched: %s", data)
        return data
    
    async def write_data(call: ServiceCall):
        sensor_id = call.data.get("sensor_id")
        value = call.data.get("value")
        cursor.execute("INSERT INTO binary_sensors_last_update (sensor_id, value) VALUES (?, ?)", (sensor_id, value))
        conn.commit()
    
    hass.services.async_register(
        "binary_sensors_last_update", "read_data", read_data
    )
    hass.services.async_register(
        "binary_sensors_last_update", "write_data", write_data
    )
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    return await async_setup(hass, {})
