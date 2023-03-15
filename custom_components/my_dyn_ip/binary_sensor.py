"""Support for My dyn ip."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .entity import MyDynIpEntity
from .my_dyn_ip_api import MyDynIpApi


# ------------------------------------------------------
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup for My dyn ip"""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    my_dyn_ip_api: MyDynIpApi = hass.data[DOMAIN][entry.entry_id]["my_dyn_ip_api"]

    sensors = []

    sensors.append(MyDynIpBinarySensor(coordinator, entry, my_dyn_ip_api))

    async_add_entities(sensors)


# ------------------------------------------------------
# ------------------------------------------------------
class MyDynIpBinarySensor(MyDynIpEntity, BinarySensorEntity):
    """Sensor class for My dyn ip"""

    # ------------------------------------------------------
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        my_dyn_ip_api: MyDynIpApi,
    ) -> None:
        super().__init__(coordinator, entry)

        self.my_dyn_ip_api = my_dyn_ip_api
        self.coordinator = coordinator

        self._name = "Changed"
        self._unique_id = "changed"

    # ------------------------------------------------------
    @property
    def name(self) -> str:
        return self._name

    # ------------------------------------------------------
    @property
    def icon(self) -> str:
        return "mdi:ip-network"

    # ------------------------------------------------------
    @property
    def is_on(self) -> bool:
        """Get the state."""

        return self.my_dyn_ip_api.changed

    # ------------------------------------------------------
    @property
    def extra_state_attributes(self) -> dict:
        attr: dict = {}

        return attr

    # ------------------------------------------------------
    @property
    def unique_id(self) -> str:
        return self._unique_id

    # ------------------------------------------------------
    @property
    def should_poll(self) -> bool:
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    # ------------------------------------------------------
    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    # ------------------------------------------------------
    async def async_update(self) -> None:
        """Update the entity. Only used by the generic entity update service."""
        await self.coordinator.async_request_refresh()

    # ------------------------------------------------------
    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
