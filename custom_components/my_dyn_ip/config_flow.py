"""Config flow to configure the My dyn ip integration."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN_NAME, DOMAIN


class SunConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for My dyn ip."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        # if user_input is not None:
        return self.async_create_entry(title=DOMAIN_NAME, data={})

        # return self.async_show_form(step_id="user")