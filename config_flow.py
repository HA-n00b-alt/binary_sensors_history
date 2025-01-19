import logging
from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class BinarySensorsHistoryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the binary_sensors_history integration."""

    async def async_step_user(self, user_input=None):
        """Handle the first step of user input (debug setting)."""
        if user_input is None:
            # Ask the user if they want debug mode enabled
            _LOGGER.debug("Showing config form to the user.")
            return self.async_show_form(
                step_id="user",
                data_schema=self._create_schema()
            )

        debug = user_input.get("debug", False)
        _LOGGER.debug(f"Debug mode set to: {debug}")

        # Save the configuration and return
        return self.async_create_entry(
            title=f"Binary Sensors History (Debug: {debug})",
            data={"debug": debug},
        )

    def _create_schema(self):
        """Return the schema for the user input form."""
        return vol.Schema({
            vol.Optional("debug", default=False): bool,
        })
