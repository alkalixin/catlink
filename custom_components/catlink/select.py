"""Support for select."""

import asyncio
import logging

from homeassistant.components.select import DOMAIN as ENTITY_DOMAIN, SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN, CatlinkEntity, Device

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{ENTITY_DOMAIN}.{DOMAIN}"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the CatLink selects."""
    coordinator = config_entry.runtime_data
    
    # Create select entities for all devices
    entities = []
    for device in coordinator.device_list:
        if hasattr(device, 'hass_select'):
            for select_key, select_config in device.hass_select.items():
                entities.append(
                    CatlinkSelectEntity(select_key, device, select_config)
                )
    
    if entities:
        async_add_entities(entities)


class CatlinkSelectEntity(CatlinkEntity, SelectEntity):
    """SelectEntity"""

    def __init__(self, entity_key: str, device: Device, option=None):
        super().__init__(entity_key, device, option)
        self._attr_options = self._option.get("options", [])

    def update(self):
        super().update()
        self._attr_current_option = self._attr_state

    async def async_select_option(self, option: str):
        """Change the selected option."""
        ret = False
        fun = self._option.get("async_select")
        if callable(fun):
            ret = await fun(option)
        if ret:
            self._attr_current_option = option
            self.async_write_ha_state()
            if dly := self._option.get("delay_update"):
                await asyncio.sleep(dly)
                self._handle_coordinator_update()
        return ret
