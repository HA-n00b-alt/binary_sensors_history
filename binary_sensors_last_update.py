from homeassistant.core import HomeAssistant
from homeassistant.helpers.service import async_register_domain_service
import sqlite3

async def async_setup(hass: HomeAssistant, config):
    conn = sqlite3.connect('/config/home-assistant_v2.db')
    cursor = conn.cursor()
    
    # Example function to read data
    def read_data():
        cursor.execute("SELECT * FROM binary_sensors_last_update")
        return cursor.fetchall()
    
    # Example function to write data
    def write_data(sensor_id, value):
        cursor.execute("INSERT INTO binary_sensors_last_update (sensor_id, value) VALUES (?, ?)", (sensor_id, value))
        conn.commit()
    
    # Register services
    async_register_domain_service(hass, "binary_sensors_last_update", "read_data", read_data)
    async_register_domain_service(hass, "binary_sensors_last_update", "write_data", write_data)
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    return await async_setup(hass, {})

