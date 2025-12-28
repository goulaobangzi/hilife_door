"""The HiLife Door integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    CONF_PHONE,
    CONF_PASSWORD,
    CONF_USER_ID,
    CONF_COMMUNITY_ID,
)
from .api import HiLifeApi

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.LOCK]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HiLife Door from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create API client
    api = HiLifeApi(
        phone=entry.data[CONF_PHONE],
        password=entry.data[CONF_PASSWORD],
        user_id=entry.data[CONF_USER_ID],
    )

    # Login
    logged_in = await hass.async_add_executor_job(api.login)
    if not logged_in:
        _LOGGER.error("Failed to login to HiLife")
        return False

    # Get doors
    community_id = entry.data[CONF_COMMUNITY_ID]
    card_no = entry.data.get("card_no", entry.data[CONF_PHONE])
    
    doors = await hass.async_add_executor_job(
        api.get_doors, community_id, card_no
    )

    if not doors:
        _LOGGER.warning("No doors found for community %s", community_id)

    # Create coordinator
    async def async_update_data():
        """Fetch data from API."""
        # Re-login if needed
        if not api.access_token:
            await hass.async_add_executor_job(api.login)
        
        # Get updated door list
        return await hass.async_add_executor_job(
            api.get_doors, community_id, card_no
        )

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(
            seconds=entry.options.get("scan_interval", 300)
        ),
    )

    # Store data
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
        "doors": doors,
        "community_id": community_id,
        "door_community_id": entry.data.get("door_community_id", community_id),
        "card_no": card_no,
    }

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
