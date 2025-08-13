"""Support for binary_sensor."""

import logging

from homeassistant.components.binary_sensor import (
    DOMAIN as ENTITY_DOMAIN,
    BinarySensorEntity,
)
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
    """Set up the CatLink binary sensors."""
    coordinator = config_entry.runtime_data
    
    # Create binary sensor entities for all devices
    entities = []
    for device in coordinator.device_list:
        if hasattr(device, 'hass_binary_sensor'):
            for sensor_key, sensor_config in device.hass_binary_sensor.items():
                entities.append(
                    CatlinkBinarySensorEntity(sensor_key, device, sensor_config)
                )
    
    if entities:
        async_add_entities(entities)


class CatlinkBinarySensorEntity(CatlinkBinaryEntity, BinarySensorEntity):
    """BinarySensorEntity"""
