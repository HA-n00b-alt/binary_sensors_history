import logging
import sqlite3
import json
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

async def read_sensor_data(hass: HomeAssistant, call: ServiceCall):
    try:
        db_path = hass.config.path('home-assistant_v2.db') 
        conn = sqlite3.connect(db_path) 
        cur = conn.cursor()

        # Get the entity_id from the service call data
        entity_id = call.data.get('entity_id') 
        if not entity_id:
            _LOGGER.error("No entity_id provided in the service call.")
            return

        cur.execute("SELECT * FROM binary_sensors_last_update WHERE entity=?", (entity_id,))
        row = cur.fetchone()

        if row:
            last_update_data = {
                "entity": row[0],
                "timestamp": row[1],
                "state": row[2],
                "last_row_update": row[3]
            }
            _LOGGER.info(f"Last update data for {entity_id}: {json.dumps(last_update_data)}")
        else:
            _LOGGER.info(f"No data found for entity_id: {entity_id} in binary_sensors_last_update table.")

        cur.close()
        conn.close()

    except sqlite3.Error as e:
        _LOGGER.error(f"Error accessing SQLite database: {e}")
    except Exception as e:
        _LOGGER.error(f"An unexpected error occurred: {e}")

async def async_setup(hass: HomeAssistant, config):
    """Set up the binary_sensors_history integration."""
    # Set the logger level based on the 'debug' setting from the config
    _LOGGER.setLevel(logging.DEBUG if config.get("debug", False) else logging.INFO) 

    # Register the service with the correct function signature
    hass.services.async_register(
        "binary_sensors_history", "read_sensor_data", read_sensor_data
    )

    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up the binary_sensors_history integration from a config entry."""
    _LOGGER.info("async_setup_entry called for binary_sensors_history")

    # Set the logger level based on the 'debug' setting from the config entry
    _LOGGER.setLevel(logging.DEBUG if entry.data.get("debug", False) else logging.INFO) 

    return await async_setup(hass, entry.data)
