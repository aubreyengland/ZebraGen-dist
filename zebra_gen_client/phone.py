import logging
from typing import Iterator
from . import ZoomServerFault
from .base import (
    CRUDEndpoint,
    Endpoint,
    GetEndpointMixin,
    ListEndpointMixin,
    UpdateEndpointMixin,
    CreateEndpointMixin,
)

log = logging.getLogger(__name__)

class PhoneSites(CRUDEndpoint):
    uri = "phone/sites"

    def get_settings(self, site_id: str, setting_type: str = None):
        if setting_type:
            url = self.url(f"{site_id}/settings/{setting_type}")
        else:
            url = self.url(f"{site_id}/settings")

        return self._get(url)

    def add_settings(self, site_id: str, setting_type: str, payload: dict):
        """
        setting_type must be one of holiday_hours,security
        """
        url = self.url(f"{site_id}/settings/{setting_type}")
        resp = self.session.post(url, json=payload)
        return resp.json()

    def update_settings(self, site_id: str, setting_type: str, payload: dict):
        """
        setting_type must be one of local_based_routing, business_hours, closed_hours, holiday_hours
        outbound_caller_id, audio_prompt, desk_phone, dial_by_name, billing_account
        """
        url = self.url(f"{site_id}/settings/{setting_type}")
        self.session.patch(url, json=payload)

    def delete_settings(self, site_id: str, setting_type: str, setting_value: str):
        """
        setting_type must be one of holiday_hours,security
        setting_val must be a holiday hour setting ID or device type
        """
        url = self.url(f"{site_id}/settings/{setting_type}")
        param_name = "holiday_id" if setting_type == "holiday_hours" else "device_type"
        self.session.delete(url, params={param_name: setting_value})

    def list_caller_id(self, site_id: str, **params):
        url = self.url(f"{site_id}/outbound_caller_id/customized_numbers")
        yield from self._paged_get(url, "customize_numbers", params)

    def add_caller_id(self, site_id: str, payload: dict):
        """
        RequestBuilder ex:
            {"phone_number_ids": ["55JUZPwERHuGttd_j4qBsQ"]}
        """
        url = self.url(f"{site_id}/outbound_caller_id/customized_numbers")
        self.session.post(url, json=payload)

    def remove_caller_id(self, site_id: str, phone_number_ids: list):
        url = self.url(f"{site_id}/outbound_caller_id/customized_numbers")
        params = dict(customize_ids=phone_number_ids)
        self.session.delete(url, params=params)


class PhoneDevices(CRUDEndpoint):
    uri = "phone/devices"

    def sync_desk_phones(self, payload: dict) -> None:
        url = self.url("sync")
        self.session.post(url, json=payload)

    def reboot_desk_phone(self, device_id: str) -> None:
        url = self.url(f"{device_id}/reboot")
        self.session.post(url)

    def assign_entities(self, device_id: str, payload: dict) -> None:
        url = self.url(f"{device_id}/extensions")
        self.session.post(url, json=payload)

    def unassign_entity(self, device_id: str, extension_id: str) -> None:
        url = self.url(f"{device_id}/extensions/{extension_id}")
        self.session.delete(url)



class PhoneCommonAreas(CRUDEndpoint):
    uri = "phone/common_areas"

    def get_settings(self, identifier: str) -> dict:
        """
        Lists devices common area is set on.

        Args:
            identifier (str): Common area ID or common area extension ID.
        """
        url = self.url(f"{identifier}/settings")
        return self._get(url)

    def add_settings(self, identifier: str, setting_type: str) -> dict:
        """
        Add the common area setting according to the setting type, specifically for desk phones.

        Args:
            identifier (str): Common area ID or common area extension ID.
            setting_type (str): Must be one of desk_phone
        """
        url = self.url(f"{identifier}/settings/{setting_type}")
        resp = self.session.post(url)
        return resp.json()

    def update_settings(self, identifier: str, setting_type: str, payload: dict) -> None:
        """
        Args:
            identifier (str): Common area ID or common area extension ID.
            setting_type (str): Must be one of desk_phone
            payload (dict): desk_phone payload
        """
        url = self.url(f"{identifier}/settings/{setting_type}")
        self.session.patch(url, json=payload)

    def delete_settings(self, identifier: str, setting_type: str, device_id: str) -> None:
        """
        Remove device association from the common area
        Args:
            identifier (str): Common area ID or common area extension ID.
            setting_type (str): Must be one of desk_phone
            device_id (str): ID of device to remove from common area
        """
        url = self.url(f"{identifier}/settings/{setting_type}")
        self.session.delete(url, params={"device_id": device_id})

    def assign_calling_plan(self, identifier: str, payload: list) -> None:
        """
        Assign calling plans to an existing Common Area.

        The calling plans must be provided as a list of dictionaries
        with a 'type' key containing the integer ID for the calling plan
        to assign. An optional 'billing_account_id' can be provided but this is only
        needed for Indian calling plans

        Args:
            identifier (str): Common area ID or common area extension ID.
            payload (list): List of calling plan dictionaries
        """
        url = self.url(f"{identifier}/calling_plans")
        resp = self.session.post(url, json=payload)
        return resp.json()

    def unassign_calling_plan(
        self, identifier: str, calling_plan_type: str, **params
    ) -> None:
        """
        Un-assign a calling plan to an existing Common Area.
        Accepts 'billing_account_id' as query param

        Args:
            identifier (str): Common area ID or common area extension ID.
            calling_plan_type (str): Calling plan type value
        """
        url = self.url(f"{identifier}/calling_plans/{calling_plan_type}")
        self.session.delete(url, params=params)

    def assign_phone_numbers(self, identifier: str, payload: dict) -> None:
        """
        Args:
            identifier (str): Common area ID or common area extension ID.
            payload (dict): Dict of phone numbers or id values
            {"phone_numbers": [{"number": "+12243416415","id": "TqH98ec8RVCu6Z00aBv9ow"}]}
        """
        url = self.url(f"{identifier}/phone_numbers")
        resp = self.session.post(url, json=payload)
        return resp.json()

    def unassign_phone_number(self, identifier: str, phone_number_id: str) -> None:
        """
        Args:
            identifier (str): Common area ID or common area extension ID.
            phone_number_id (str): The phone number or the phone number ID.
        """
        url = self.url(f"{identifier}/phone_numbers/{phone_number_id}")
        self.session.delete(url)
        
    def block_outbound_calling(self, identifier: str, payload: dict) -> None:
        """
        Update outbound calling for a common area by country or region.

        Args:
            identifier (str): Common area ID or common area extension ID.
            payload (dict): Payload to block outbound calling.
        """
        url = self.url(f"{identifier}/outbound_calling/countries_regions")
        self.session.patch(url, json=payload)
