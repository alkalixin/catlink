"""Support for sensor."""

import logging

import voluptuous as vol

from homeassistant.components.sensor import DOMAIN as ENTITY_DOMAIN, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN, CatlinkEntity

_LOGGER = logging.getLogger(__name__)

DATA_KEY = f"{ENTITY_DOMAIN}.{DOMAIN}"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the CatLink sensors."""
    coordinator = config_entry.runtime_data
    
    # Create sensor entities for all devices
    entities = []
    for device in coordinator.device_list:
        if hasattr(device, 'hass_sensor'):
            for sensor_key, sensor_config in device.hass_sensor.items():
                entities.append(
                    CatlinkSensorEntity(sensor_key, device, sensor_config)
                )
    
    if entities:
        async_add_entities(entities)

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        "request_api",
        {
            vol.Required("api"): cv.string,
            vol.Optional("params", default={}): vol.Any(dict, None),
            vol.Optional("method", default="GET"): cv.string,
            vol.Optional("throw", default=True): cv.boolean,
        },
        "async_request_api",
    )


class CatlinkSensorEntity(CatlinkEntity, SensorEntity):
    """SensorEntity"""

    def update(self):
        super().update()
        self._attr_native_value = self._attr_state
