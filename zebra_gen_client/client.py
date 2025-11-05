import logging
from . import phone
from .base import ZoomSession

log = logging.getLogger(__name__)


class ZoomSimpleClient:
    def __init__(self, access_token, base_url="https://api.zoom.us/v2", verify=True):
        session = ZoomSession(access_token, base_url, verify)
        self.phone_sites = phone.PhoneSites(session)
        self.phone_devices = phone.PhoneDevices(session)
        self.phone_common_areas = phone.PhoneCommonAreas(session)