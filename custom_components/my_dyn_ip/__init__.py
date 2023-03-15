"""The My dyn ip integration."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .services import async_setup_services

from .const import (
    DOMAIN,
    LOGGER,
)
from .my_dyn_ip_api import MyDynIpApi

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]


# ------------------------------------------------------------------
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up My dyn ip from a config entry."""
    session = async_get_clientsession(hass)

    hass.data.setdefault(DOMAIN, {})

    my_dyn_ip_api: MyDynIpApi = MyDynIpApi(
        session,
    )

    coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
        hass,
        LOGGER,
        name=DOMAIN,
        update_interval=timedelta(minutes=30),
        update_method=my_dyn_ip_api.update,
    )

    await coordinator.async_config_entry_first_refresh()
    entry.async_on_unload(entry.add_update_listener(update_listener))

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "my_dyn_ip_api": my_dyn_ip_api,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    await async_setup_services(hass, my_dyn_ip_api)

    return True


# ------------------------------------------------------------------
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


# ------------------------------------------------------------------
async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


# ------------------------------------------------------------------
async def update_listener(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> None:
    """Reload on config entry update."""

    my_dyn_ip_api: MyDynIpApi = hass.data[DOMAIN][config_entry.entry_id][
        "my_dyn_ip_api"
    ]

    await hass.config_entries.async_reload(config_entry.entry_id)
    await my_dyn_ip_api.update()

    return