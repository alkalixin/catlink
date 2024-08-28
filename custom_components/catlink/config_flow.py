import voluptuous as vol

from homeassistant import config_entries

from .const import (
    CONF_API_BASE,
    CONF_LANGUAGE,
    CONF_PASSWORD,
    CONF_PHONE,
    CONF_PHONE_IAC,
    DEFAULT_API_BASE,
    DOMAIN,
)

ACCOUNT_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_API_BASE, default=DEFAULT_API_BASE): str,
        vol.Required(CONF_PHONE): str,
        vol.Required(CONF_PHONE_IAC, default="86"): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional(CONF_LANGUAGE, default="zh_CN"): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(
                title=f"Catlink: {user_input[CONF_PHONE]}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=ACCOUNT_SCHEMA,
        )
