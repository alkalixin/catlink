"""Support for select."""

import asyncio
import logging

from homeassistant.components.select import DOMAIN as ENTITY_DOMAIN, SelectEntity

from . import DOMAIN, CatlinkEntity, Device, async_setup_accounts

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{ENTITY_DOMAIN}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    hass.data[DOMAIN]["add_entities"][ENTITY_DOMAIN] = async_add_entities
    await async_setup_accounts(hass, ENTITY_DOMAIN)


class CatlinkSelectEntity(CatlinkEntity, SelectEntity):
    def __init__(self, entity_key, device: Device, option=None):
        super().__init__(entity_key, device, option)
        self._attr_current_option = None
        self._attr_options = self._option.get("options")

    def update(self):
        super().update()
        self._attr_current_option = self._attr_state

    async def async_select_option(self, option: str):
        """Change the selected option."""
        ret = False
        fun = self._option.get("async_select")
        if callable(fun):
            kws = {
                # 'entity': self,
            }
            ret = await fun(option, **kws)
        if ret:
            self._attr_current_option = option
            self.async_write_ha_state()
            if dly := self._option.get("delay_update"):
                await asyncio.sleep(dly)
                self._handle_coordinator_update()
        return ret
