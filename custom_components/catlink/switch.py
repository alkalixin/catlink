"""Support for switch."""

import asyncio
import logging

from homeassistant.components.switch import DOMAIN as ENTITY_DOMAIN, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN, CatlinkBinaryEntity

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{ENTITY_DOMAIN}.{DOMAIN}"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the CatLink switches."""
    coordinator = config_entry.runtime_data
    
    # Create switch entities for all devices
    entities = []
    for device in coordinator.device_list:
        if hasattr(device, 'hass_switch'):
            for switch_key, switch_config in device.hass_switch.items():
                entities.append(
                    CatlinkSwitchEntity(switch_key, device, switch_config)
                )
    
    if entities:
        async_add_entities(entities)


class CatlinkSwitchEntity(CatlinkBinaryEntity, SwitchEntity):
    async def async_turn_switch(self, on=True, **kwargs):
        """Turn the entity on/off."""
        ret = False
        fun = self._option.get("async_turn_on" if on else "async_turn_off")
        if callable(fun):
            # kwargs['entity'] = self
            ret = await fun(**kwargs)
        if ret:
            self._attr_is_on = not not on
            self.async_write_ha_state()
            if dly := self._option.get("delay_update"):
                await asyncio.sleep(dly)
                self._handle_coordinator_update()
        return ret

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        return await self.async_turn_switch(True)

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        return await self.async_turn_switch(False)
