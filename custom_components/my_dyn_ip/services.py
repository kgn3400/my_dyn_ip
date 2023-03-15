"""Services for My dyn ip integration."""
from homeassistant.core import HomeAssistant
from .my_dyn_ip_api import MyDynIpApi
from .const import DOMAIN


async def async_setup_services(hass: HomeAssistant, my_dyn_ip_api: MyDynIpApi) -> None:
    """Set up the services for the My dyn ip integration."""

    hass.services.async_register(DOMAIN, "update", my_dyn_ip_api.update_service)
    hass.services.async_register(DOMAIN, "reset", my_dyn_ip_api.reset_service)
