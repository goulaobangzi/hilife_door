"""Lock platform for HiLife Door integration."""
import logging
from typing import Any

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HiLife Door lock entities."""
    data = hass.data[DOMAIN][entry.entry_id]
    
    api = data["api"]
    coordinator = data["coordinator"]
    doors = data["doors"]
    community_id = data["community_id"]
    door_community_id = data["door_community_id"]
    card_no = data["card_no"]

    entities = []
    for door in doors:
        entities.append(
            HiLifeDoorLock(
                coordinator=coordinator,
                api=api,
                door_id=door["id"],
                door_name=door["name"],
                community_id=community_id,
                door_community_id=door_community_id,
                card_no=door.get("card_no", card_no),
                entry_id=entry.entry_id,
            )
        )

    async_add_entities(entities)


class HiLifeDoorLock(CoordinatorEntity, LockEntity):
    """Representation of a HiLife Door lock."""

    def __init__(
        self,
        coordinator,
        api,
        door_id: int,
        door_name: str,
        community_id: str,
        door_community_id: str,
        card_no: str,
        entry_id: str,
    ):
        """Initialize the lock."""
        super().__init__(coordinator)
        
        self._api = api
        self._door_id = door_id
        self._door_name = door_name
        self._community_id = community_id
        self._door_community_id = door_community_id
        self._card_no = card_no
        self._entry_id = entry_id
        
        self._attr_unique_id = f"hilife_door_{door_id}"
        self._attr_name = door_name
        self._attr_is_locked = True  # Doors are always "locked"
        self._attr_is_locking = False
        self._attr_is_unlocking = False

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, str(self._door_id))},
            "name": self._door_name,
            "manufacturer": "HiLife 合生活",
            "model": "Smart Door",
        }

    @property
    def is_locked(self) -> bool:
        """Return true if the lock is locked."""
        return self._attr_is_locked

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the device (no-op for doors)."""
        # Doors cannot be locked remotely
        pass

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the device (open the door)."""
        self._attr_is_unlocking = True
        self.async_write_ha_state()

        try:
            result = await self.hass.async_add_executor_job(
                self._api.open_door,
                self._door_id,
                self._door_name,
                self._community_id,
                self._door_community_id,
                self._card_no,
            )

            if result.get("status") == 1:
                _LOGGER.info("Door %s opened successfully", self._door_name)
                # Temporarily show as unlocked
                self._attr_is_locked = False
                self.async_write_ha_state()
                
                # Reset to locked after 3 seconds
                await self._async_reset_lock_state()
            else:
                _LOGGER.error(
                    "Failed to open door %s: %s",
                    self._door_name,
                    result.get("msg", "Unknown error")
                )
        except Exception as e:
            _LOGGER.error("Error opening door %s: %s", self._door_name, e)
        finally:
            self._attr_is_unlocking = False
            self.async_write_ha_state()

    async def _async_reset_lock_state(self):
        """Reset lock state after a delay."""
        import asyncio
        await asyncio.sleep(3)
        self._attr_is_locked = True
        self.async_write_ha_state()

    async def async_open(self, **kwargs: Any) -> None:
        """Open the door (same as unlock)."""
        await self.async_unlock(**kwargs)
