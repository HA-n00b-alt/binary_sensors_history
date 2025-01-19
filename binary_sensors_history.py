import logging
import sqlite3
import json
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

async def update_sensor_data(hass: HomeAssistant, call: ServiceCall):
    """Update sensor data in the database."""
    try:
        _LOGGER.debug("Connecting to SQLite database...")
        db_path = hass.config.path('home-assistant_v2.db')
        conn = sqlite3.connect(db_path)
        _LOGGER.debug(f"Connected to SQLite database: {db_path}")
        cur = conn.cursor()

        # Get the entity_id from the service call data
        entity_id = call.data.get('entity_id')
        if not entity_id:
            _LOGGER.error("No entity_id provided in the service call.")
            return

        _LOGGER.debug(f"Executing SQL query for entity_id: {entity_id}")
        cur.execute("""
            WITH filtered_states AS (
                SELECT
                    datetime(s.last_updated_ts, 'unixepoch') AS timestamp, 
                    s.state,
                    LAG(s.state) OVER (PARTITION BY s.metadata_id ORDER BY s.last_updated_ts) AS prev_state,
                    sm.entity_id
                FROM
                    states s
                JOIN
                    states_meta sm ON s.metadata_id = sm.metadata_id
                WHERE
                    sm.entity_id = ?
            ),
            latest_events AS (
                SELECT
                    entity_id,
                    timestamp,
                    state,
                    prev_state,
                    ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY timestamp DESC) AS rn
                FROM
                    filtered_states
                WHERE
                    state IN ('on', 'off')
                    AND prev_state IN ('on', 'off')
            ),
            latest_event AS (
                SELECT
                    entity_id,
                    timestamp,
                    state
                FROM
                    latest_events
                WHERE
                    rn = 1
            )
            INSERT OR REPLACE INTO binary_sensors_last_update (entity, timestamp, state, last_row_update)
            SELECT
                entity_id,
                timestamp,
                state,
                datetime('now')
            FROM
                latest_event;
        """, (entity_id,))
        conn.commit()
        _LOGGER.debug("SQL query executed and committed.")

        cur.close()
        conn.close()
        _LOGGER.debug("Database connection closed.")

    except sqlite3.Error as e:
        _LOGGER.error(f"Error accessing SQLite database: {e}")
    except Exception as e:
        _LOGGER.error(f"An unexpected error occurred: {e}")

async def async_setup(hass: HomeAssistant, config):
    hass.services.async_register(
        "binary_sensors_history", "update_sensor_data", update_sensor_data
    )
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up the binary_sensors_history integration from a config entry."""
    _LOGGER.info("async_setup_entry called for binary_sensors_history")

    # Now get the 'debug' setting from the config entry data and set the logger level
    debug_mode = entry.data.get("debug", False)

    if debug_mode:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("async_setup called for binary_sensors_history")
    else:
        _LOGGER.setLevel(logging.INFO)

    return await async_setup(hass, entry.data)