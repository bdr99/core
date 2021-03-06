"""Support for Verisure sensors."""
from __future__ import annotations

from typing import Any, Callable

from homeassistant.const import PERCENTAGE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from . import HUB as hub
from .const import CONF_HYDROMETERS, CONF_MOUSE, CONF_THERMOMETERS


def setup_platform(
    hass: HomeAssistant,
    config: dict[str, Any],
    add_entities: Callable[[list[Entity], bool], None],
    discovery_info: dict[str, Any] | None = None,
) -> None:
    """Set up the Verisure platform."""
    sensors = []
    hub.update_overview()

    if int(hub.config.get(CONF_THERMOMETERS, 1)):
        sensors.extend(
            [
                VerisureThermometer(device_label)
                for device_label in hub.get(
                    "$.climateValues[?(@.temperature)].deviceLabel"
                )
            ]
        )

    if int(hub.config.get(CONF_HYDROMETERS, 1)):
        sensors.extend(
            [
                VerisureHygrometer(device_label)
                for device_label in hub.get(
                    "$.climateValues[?(@.humidity)].deviceLabel"
                )
            ]
        )

    if int(hub.config.get(CONF_MOUSE, 1)):
        sensors.extend(
            [
                VerisureMouseDetection(device_label)
                for device_label in hub.get(
                    "$.eventCounts[?(@.deviceType=='MOUSE1')].deviceLabel"
                )
            ]
        )

    add_entities(sensors)


class VerisureThermometer(Entity):
    """Representation of a Verisure thermometer."""

    def __init__(self, device_label: str):
        """Initialize the sensor."""
        self._device_label = device_label

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return (
            hub.get_first(
                "$.climateValues[?(@.deviceLabel=='%s')].deviceArea", self._device_label
            )
            + " temperature"
        )

    @property
    def state(self) -> str | None:
        """Return the state of the device."""
        return hub.get_first(
            "$.climateValues[?(@.deviceLabel=='%s')].temperature", self._device_label
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            hub.get_first(
                "$.climateValues[?(@.deviceLabel=='%s')].temperature",
                self._device_label,
            )
            is not None
        )

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity."""
        return TEMP_CELSIUS

    # pylint: disable=no-self-use
    def update(self) -> None:
        """Update the sensor."""
        hub.update_overview()


class VerisureHygrometer(Entity):
    """Representation of a Verisure hygrometer."""

    def __init__(self, device_label: str):
        """Initialize the sensor."""
        self._device_label = device_label

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return (
            hub.get_first(
                "$.climateValues[?(@.deviceLabel=='%s')].deviceArea", self._device_label
            )
            + " humidity"
        )

    @property
    def state(self) -> str | None:
        """Return the state of the device."""
        return hub.get_first(
            "$.climateValues[?(@.deviceLabel=='%s')].humidity", self._device_label
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            hub.get_first(
                "$.climateValues[?(@.deviceLabel=='%s')].humidity", self._device_label
            )
            is not None
        )

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity."""
        return PERCENTAGE

    # pylint: disable=no-self-use
    def update(self) -> None:
        """Update the sensor."""
        hub.update_overview()


class VerisureMouseDetection(Entity):
    """Representation of a Verisure mouse detector."""

    def __init__(self, device_label):
        """Initialize the sensor."""
        self._device_label = device_label

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return (
            hub.get_first(
                "$.eventCounts[?(@.deviceLabel=='%s')].area", self._device_label
            )
            + " mouse"
        )

    @property
    def state(self) -> str | None:
        """Return the state of the device."""
        return hub.get_first(
            "$.eventCounts[?(@.deviceLabel=='%s')].detections", self._device_label
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            hub.get_first("$.eventCounts[?(@.deviceLabel=='%s')]", self._device_label)
            is not None
        )

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity."""
        return "Mice"

    # pylint: disable=no-self-use
    def update(self) -> None:
        """Update the sensor."""
        hub.update_overview()
