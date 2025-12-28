"""HiLife Door API Client."""
import base64
import logging
import requests
from typing import Optional

from .const import (
    API_LOGIN,
    API_CARD_NOS,
    API_GET_DOORS,
    API_OPEN_DOOR,
    AUTH_CLIENT,
)

_LOGGER = logging.getLogger(__name__)


class HiLifeApiError(Exception):
    """HiLife API Error."""
    pass


class HiLifeApi:
    """HiLife Door API Client."""

    def __init__(self, phone: str, password: str, user_id: str = None):
        """Initialize the API client."""
        self.phone = phone
        self.password = password
        self.user_id = user_id
        self.access_token: Optional[str] = None
        self._session = requests.Session()
        self._session.verify = False

    def login(self) -> bool:
        """Login and get access token."""
        try:
            auth = base64.b64encode(AUTH_CLIENT.encode()).decode()
            
            resp = self._session.post(
                API_LOGIN,
                headers={
                    "Authorization": f"Basic {auth}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "multiple",
                    "username": self.phone,
                    "password": self.password
                },
                timeout=15
            )
            
            if resp.status_code == 200:
                data = resp.json()
                self.access_token = data.get("access_token")
                # Auto-detect user_id (openID) if not set
                if not self.user_id:
                    self.user_id = data.get("openID")
                
                if self.access_token:
                    _LOGGER.debug("Login successful. User ID: %s", self.user_id)
                    return True
            
            _LOGGER.error("Login failed: %s", resp.text)
            return False
            
        except Exception as e:
            _LOGGER.error("Login error: %s", e)
            return False

    def get_communities(self) -> list:
        """Get list of communities (from card info)."""
        if not self.access_token:
            if not self.login():
                return []
        
        try:
            url = f"{API_CARD_NOS}?access_token={self.access_token}"
            resp = self._session.post(
                url,
                headers={"Content-Type": "application/json"},
                json={"userId": self.user_id},
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == 1:
                    cards = data.get("data", [])
                    # Extract unique communities
                    communities = {}
                    for card in cards:
                        cid = card.get("communityId")
                        cname = card.get("communityName", f"小区 {cid}")
                        door_cid = card.get("doorCommunityId", cid)
                        if cid and cid not in communities:
                            communities[cid] = {
                                "id": cid,
                                "name": cname,
                                "door_community_id": door_cid,
                                "card_no": card.get("cardNo", self.phone)
                            }
                    return list(communities.values())
            
            _LOGGER.error("Get communities failed: %s", resp.text)
            return []
            
        except Exception as e:
            _LOGGER.error("Get communities error: %s", e)
            return []

    def get_doors(self, community_id: str, card_no: str = None) -> list:
        """Get list of doors for a community."""
        if not self.access_token:
            if not self.login():
                return []
        
        if not card_no:
            card_no = self.phone
        
        try:
            url = f"{API_GET_DOORS}?access_token={self.access_token}"
            resp = self._session.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "communityID": str(community_id),
                    "communityId": str(community_id),
                    "type": "1",
                    "userId": self.user_id,
                    "cardNo": card_no,
                    "phoneNo": card_no,
                    "begin": 1,
                    "end": 200,
                    "lat": "0",
                    "lon": "0",
                },
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == 1:
                    doors = data.get("data", {}).get("dataList", [])
                    return [
                        {
                            "id": door.get("msDoorId"),
                            "name": door.get("msDoorName"),
                            "door_id": door.get("id"),
                            "card_no": door.get("cardno", card_no),
                        }
                        for door in doors
                    ]
            
            _LOGGER.error("Get doors failed: %s", resp.text)
            return []
            
        except Exception as e:
            _LOGGER.error("Get doors error: %s", e)
            return []

    def open_door(
        self,
        door_id: int,
        door_name: str,
        community_id: str,
        door_community_id: str = None,
        card_no: str = None
    ) -> dict:
        """Open a door."""
        if not self.access_token:
            if not self.login():
                return {"status": -1, "msg": "登录失败"}
        
        if not door_community_id:
            door_community_id = community_id
        if not card_no:
            card_no = self.phone
        
        try:
            url = f"{API_OPEN_DOOR}?access_token={self.access_token}"
            resp = self._session.post(
                url,
                headers={"Content-Type": "application/json; charset=UTF-8"},
                json={
                    "doorName": door_name,
                    "doorCommunityId": str(door_community_id),
                    "communityId": str(community_id),
                    "doorId": door_id,
                    "cardNo": card_no,
                    "userId": self.user_id,
                    "isScan": 2,
                },
                timeout=10
            )
            
            if resp.status_code == 200:
                result = resp.json()
                _LOGGER.debug("Open door result: %s", result)
                return result
            
            return {"status": -1, "msg": f"HTTP {resp.status_code}"}
            
        except Exception as e:
            _LOGGER.error("Open door error: %s", e)
            return {"status": -1, "msg": str(e)}

    def test_connection(self) -> bool:
        """Test the connection."""
        return self.login()
