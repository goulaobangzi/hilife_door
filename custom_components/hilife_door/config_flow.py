"""Config flow for HiLife Door integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_PHONE,
    CONF_PASSWORD,
    CONF_USER_ID,
    CONF_COMMUNITY_ID,
    CONF_COMMUNITY_NAME,
)
from .api import HiLifeApi

_LOGGER = logging.getLogger(__name__)


class HiLifeDoorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HiLife Door."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._phone: str = ""
        self._password: str = ""
        self._user_id: str = ""
        self._communities: list = []
        self._api: HiLifeApi = None

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step - credentials."""
        errors = {}

        if user_input is not None:
            self._phone = user_input[CONF_PHONE]
            self._password = user_input[CONF_PASSWORD]
            self._user_id = user_input[CONF_USER_ID]

            # Test connection
            self._api = HiLifeApi(self._phone, self._password, self._user_id)
            
            valid = await self.hass.async_add_executor_job(
                self._api.test_connection
            )

            if valid:
                # Get communities
                self._communities = await self.hass.async_add_executor_job(
                    self._api.get_communities
                )
                
                if len(self._communities) == 0:
                    errors["base"] = "no_communities"
                elif len(self._communities) == 1:
                    # Only one community, skip selection
                    community = self._communities[0]
                    return self.async_create_entry(
                        title=f"HiLife - {community['name']}",
                        data={
                            CONF_PHONE: self._phone,
                            CONF_PASSWORD: self._password,
                            CONF_USER_ID: self._user_id,
                            CONF_COMMUNITY_ID: community["id"],
                            CONF_COMMUNITY_NAME: community["name"],
                            "door_community_id": community["door_community_id"],
                            "card_no": community["card_no"],
                        },
                    )
                else:
                    # Multiple communities, show selection
                    return await self.async_step_community()
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PHONE): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_USER_ID): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "user_id_help": "从 App 或 mitmproxy 抓包获取的 personId/userId"
            },
        )

    async def async_step_community(self, user_input=None) -> FlowResult:
        """Handle community selection step."""
        errors = {}

        if user_input is not None:
            community_id = user_input[CONF_COMMUNITY_ID]
            
            # Find selected community
            community = next(
                (c for c in self._communities if str(c["id"]) == str(community_id)),
                None
            )
            
            if community:
                return self.async_create_entry(
                    title=f"HiLife - {community['name']}",
                    data={
                        CONF_PHONE: self._phone,
                        CONF_PASSWORD: self._password,
                        CONF_USER_ID: self._user_id,
                        CONF_COMMUNITY_ID: community["id"],
                        CONF_COMMUNITY_NAME: community["name"],
                        "door_community_id": community["door_community_id"],
                        "card_no": community["card_no"],
                    },
                )
            else:
                errors["base"] = "invalid_community"

        # Build community selection options
        community_options = {
            str(c["id"]): c["name"] for c in self._communities
        }

        return self.async_show_form(
            step_id="community",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_COMMUNITY_ID): vol.In(community_options),
                }
            ),
            errors=errors,
            description_placeholders={
                "community_count": str(len(self._communities))
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return HiLifeDoorOptionsFlow(config_entry)


class HiLifeDoorOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for HiLife Door."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "scan_interval",
                        default=self.config_entry.options.get("scan_interval", 300),
                    ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
                }
            ),
        )
