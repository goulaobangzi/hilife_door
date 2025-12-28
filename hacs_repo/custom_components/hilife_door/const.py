"""Constants for the HiLife Door integration."""

DOMAIN = "hilife_door"

# Configuration keys
CONF_PHONE = "phone"
CONF_PASSWORD = "password"
CONF_USER_ID = "user_id"
CONF_COMMUNITY_ID = "community_id"
CONF_COMMUNITY_NAME = "community_name"

# API endpoints
API_LOGIN = "https://token.91helife.com/oauth/token"
API_CARD_NOS = "https://www.91helife.com/erp/front/interface/door/CardNos/three"
API_GET_DOORS = "https://www.91helife.com/erp/front/interface/es/door/v3/getDoors"
API_OPEN_DOOR = "https://www.91helife.com/erp/front/interface/door/openDoor/three"

# Auth
AUTH_CLIENT = "esnMobileClient:esnMobile"
