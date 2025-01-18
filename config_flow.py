import logging
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

class BinarySensorsHistoryConfigFlow(config_entries.ConfigFlow, domain="binary_sensors_history"):
    """Handle a config flow for the binary_sensors_history integration."""

    def __init__(self):
        """Initialize the flow."""
        self.debug = False

    async def async_step_user(self, user_input=None):
        """Handle the first step of user input (debug setting)."""
        if user_input is None:
            # Ask the user if they want debug mode enabled
            return self.async_show_form(
                step_id="user", data_schema=self._create_schema()
            )

        self.debug = user_input.get("debug", False)

        # Save the configuration and return
        return self.async_create_entry(
            title="Binary Sensors History",
            data={"debug": self.debug},
        )

    def _create_schema(self):
        """Return the schema for the user input form."""
        from homeassistant.helpers import config_validation as cv
        from voluptuous import Optional

        return {
            Optional("debug", default=False): bool,  # Add debug option to the form
        }


