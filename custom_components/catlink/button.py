"""Support for button."""

import logging

from homeassistant.components.button import DOMAIN as ENTITY_DOMAIN, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN, CatlinkEntity

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{ENTITY_DOMAIN}.{DOMAIN}"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the CatLink buttons."""
    coordinator = config_entry.runtime_data
    
    # Create button entities for all devices
    entities = []
    for device in coordinator.device_list:
        if hasattr(device, 'hass_button'):
            for button_key, button_config in device.hass_button.items():
                entities.append(
                    CatlinkButtonEntity(button_key, device, button_config)
                )
    
    if entities:
        async_add_entities(entities)


class CatlinkButtonEntity(CatlinkEntity, ButtonEntity):
    """ButtonEntity"""

    async def async_press(self) -> None:
        """Handle the button press."""
        fun = self._option.get("async_press")
        if callable(fun):
            await fun()
