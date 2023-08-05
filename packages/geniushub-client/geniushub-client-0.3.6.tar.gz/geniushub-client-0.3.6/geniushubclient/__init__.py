"""Python client library for the Genius Hub API.

   see: https://my.geniushub.co.uk/docs
   """
# import asyncio
from hashlib import sha256
import logging
import re

import aiohttp
import json

from .const import (
    API_STATUS_ERROR,
    DEFAULT_INTERVAL_V1, DEFAULT_INTERVAL_V3,
    DEFAULT_TIMEOUT_V1, DEFAULT_TIMEOUT_V3,
    ITYPE_TO_TYPE, IMODE_TO_MODE, MODE_TO_IMODE,
    LEVEL_TO_TEXT, DESCRIPTION_TO_TEXT,
    ZONE_TYPES, ZONE_MODES, KIT_TYPES)

HTTP_OK = 200  # cheaper than: from http import HTTPStatus.OK

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.WARNING)

# pylint: disable=no-member, invalid-name, protected-access

def _without_keys(dict_obj, keys) -> dict:
    _info = dict(dict_obj)
    _info = {k: v for k, v in _info.items() if k[:1] != '_'}
    _info = {k: v for k, v in _info.items() if k not in keys}
    return _info

def _extract_zones_from_zones(raw_json) -> list:
    """Extract Zones from /v3/zones JSON.

    This extracts a list of Zones from a flat list of Zones.
    """
    _LOGGER.debug("_zones_from_zones(): raw_json = %s", raw_json)

    return raw_json

def _extract_devices_from_data_manager(raw_json) -> list:
    """Extract Devices from /v3/data_manager JSON.

    This extracts a list of Devices from a nested list of Devices. Each
    Zone may have multiple Devices.
    """
    _LOGGER.debug("_devices_from_data_manager(): raw_json = %s", raw_json)

    result = []
    for k1, v1 in raw_json['childNodes'].items():
        if k1 != 'WeatherData':
            for device_id, device in v1['childNodes'].items():
                # if device_id != '1':  # alternatively: device['addr'] != '1':
                if device_id != '88':  # alternatively: device['addr'] != '1':
                    result.append(device)

    return result

def _extract_devices_from_zones(raw_json) -> list:
    """Extract Devices from /v3/zones JSON.

    This extracts a list of Devices from a list of Zones. Each Zone may
    have multiple Devices.
    """
    _LOGGER.debug("_devices_from_zones(): raw_json = %s", raw_json)

    result = []
    for zone in raw_json:
        # if 'nodes' in zone:
        for device in zone['nodes']:
            # if device['addr'] not in ['1', 'WeatherData']:
            if device['addr'] not in ['WeatherData']:
                result.append(device)

    return result

def _extract_issues_from_zones(raw_json) -> list:
    """Extract Issues from /v3/zones JSON.

    This extracts a list of Issues from a list of Zones.  Each Zone may
    have multiple Issues.
    """
    _LOGGER.debug("_issues_from_zones(): raw_json = %s", raw_json)

    result = []
    for zone in raw_json:
        for issue in zone['lstIssues']:
            # TODO: might better be an ID
            issue.update({'zone_name': zone['strName']})
            result.append(issue)

    return result


def natural_sort(dict_list, dict_key):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c)
        for c in re.split('([0-9]+)', key[dict_key]) ]
    return sorted(dict_list, key = alphanum_key)


class GeniusHubClient(object):
    """The class for a connection to a Genius Hub."""
    def __init__(self, hub_id, username=None, password=None, session=None,
                 debug=False):
        if debug is True:
            _LOGGER.setLevel(logging.DEBUG)
            _LOGGER.debug("Debug mode is explicitly enabled.")
        else:
            _LOGGER.debug("Debug mode is not explicitly enabled "
                          "(but may be enabled elsewhere).")

        _LOGGER.info("GeniusHubClient(hub_id=%s)", hub_id)

        # use existing session if provided
        self._session = session if session else aiohttp.ClientSession()

        # if no credentials, then hub_id is a token for v1 API
        self._api_v1 = not (username or password)
        if self._api_v1:
            self._auth = None
            self._url_base = 'https://my.geniushub.co.uk/v1/'
            self._headers = {'authorization': "Bearer " + hub_id}
            self._timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT_V1)
            self._poll_interval = DEFAULT_INTERVAL_V1
        else:  # using API ver3
            sha = sha256()
            sha.update((username + password).encode('utf-8'))
            self._auth = aiohttp.BasicAuth(
                login=username, password=sha.hexdigest())
            self._url_base = 'http://{}:1223/v3/'.format(hub_id)
            self._headers = {"Connection": "close"}
            self._timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT_V3)
            self._poll_interval = DEFAULT_INTERVAL_V3

        self._verbose = False
        hub_id = hub_id[:8] + "..." if len(hub_id) > 20 else hub_id

        self.hub = GeniusHub(self, {'id': hub_id})

    @property
    def verbose(self) -> int:
        """Currently unused, ignore."""
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        """Currently unused, ignore."""
        self._verbose = 0 if value is None else value


class GeniusObject(object):
    """The base class for Genius Hub, Zone & Device."""
    def __init__(self, client, obj_dict, hub=None, assignedZone=None):

        self.__dict__.update(obj_dict)

        self._client = client
        self._api_v1 = client._api_v1

        if isinstance(self, GeniusHub):
            self.zone_objs = []
            self.zone_by_id = {}
            self.zone_by_name = {}

            self.device_objs = []
            self.device_by_id = {}

        elif isinstance(self, GeniusZone):
            self.hub = hub

            self.device_objs = []
            self.device_by_id = {}

        elif isinstance(self, GeniusDevice):
            self.hub = hub
            self.assignedZone = assignedZone

    def _convert_zone(self, raw_dict) -> dict:
        """Convert a v3 zone's dict/json to the v1 schema."""
        if self._api_v1:
            return raw_dict

        result = {}
        result['id'] = raw_dict['iID']
        result['type'] = ITYPE_TO_TYPE[raw_dict['iType']]
        result['name'] = raw_dict['strName']

        if raw_dict['iType'] in [ZONE_TYPES.ControlSP, ZONE_TYPES.TPI]:
            result['temperature'] = raw_dict['fPV']
            result['setpoint'] = raw_dict['fSP']

        if raw_dict['iType'] == ZONE_TYPES.OnOffTimer:
            result['setpoint'] = raw_dict['fSP'] != 0

        result['mode'] = IMODE_TO_MODE[raw_dict['iMode']]

        # l = parseInt(i.iFlagExpectedKit) & e.equipmentTypes.Kit_PIR
        if raw_dict['iFlagExpectedKit'] & KIT_TYPES.PIR:
            # = parseInt(i.iMode) === e.zoneModes.Mode_Footprint
            u = raw_dict['iMode'] == ZONE_MODES.Footprint

            # = null != (s = i.zoneReactive) ? s.bTriggerOn : void 0,
            d = raw_dict['objFootprint']['objReactive']['bTriggerOn']

            # = parseInt(i.iActivity) || 0,
            # c = raw_dict['iActivity'] | 0

            # o = t.isInFootprintNightMode(i)
            o = raw_dict['objFootprint']['bIsNight']

            # u && l && d && !o ? True : False
            result['occupied'] = u and d and not o

        if raw_dict['iType'] in [ZONE_TYPES.OnOffTimer,
                                 ZONE_TYPES.ControlSP,
                                 ZONE_TYPES.TPI]:
            result['override'] = {}
            result['override']['duration'] = raw_dict['iBoostTimeRemaining']
            if raw_dict['iType'] == ZONE_TYPES.OnOffTimer:
                result['override']['setpoint'] = (raw_dict['fBoostSP'] != 0)
            else:
                result['override']['setpoint'] = raw_dict['fBoostSP']

            result['schedule'] = {}

        return result

    def _convert_device(self, raw_dict) -> dict:
        """Convert a v3 device's dict/json to the v1 schema."""
        if self._api_v1:
            return raw_dict

        def _check_fingerprint(device, device_fingerprint):
            if not device['type']:
                _LOGGER.debug("Device %s: Matched by fingerprint '%s'",
                    device['id'], device_fingerprint)
                device['type'] = device_fingerprint

            elif device['type'] == device_fingerprint:
                _LOGGER.debug("Device %s: Type matches its fingerprint '%s'",
                    device['id'], device_fingerprint)

            elif device['type'][:21] == device_fingerprint:  # "Dual Channel Receiver"
                _LOGGER.debug("Device %s: Type matches its fingerprint '%s'",
                    device['id'], device_fingerprint)

            else:  # device['type'] != device_type:
                _LOGGER.error("Device %s: Type doesn't match fingerprint '%s'",
                    device['id'], device_fingerprint)

        result = {}
        # Determine Device Id...
        result['id'] = raw_dict['addr']

        # Determine Device Type...
        result['type'] = None

        node = raw_dict['childNodes']['_cfg']['childValues']
        if node:
            result['type'] = node['name']['val']
            result['_sku'] = node['sku']['val']

        node = raw_dict['childValues']
        # try to find the Dual Channel Receiver
        if 'SwitchBinary' in node and \
                node['SwitchBinary']['path'].count('/') == 3:

            device_type = 'Dual Channel Receiver - Channel {}'
            path = node['SwitchBinary']['path']

            if result['type'] is None:
                result['id'] = '{}-{}'.format(path[-3], path[-1])
                result['type'] = device_type.format(path[-1])
            else:
                _LOGGER.error("Clash for Device type: "
                              "via Method 1: %s, via Method 2: %s",
                              result['type'], device_type.format(path[-1]))

        # try to 'fingerprint' the device type
        if 'SwitchBinary' in node:
            if 'TEMPERATURE' in node:
                _check_fingerprint(result, "Electric Switch")

            elif 'SwitchAllMode' in node:
                _check_fingerprint(result, "Smart Plug")

            else:
                _check_fingerprint(result, "Dual Channel Receiver")

        elif 'setback' in node:
            if 'TEMPERATURE' in node:
                _check_fingerprint(result, "Genius Valve")
            else:
                _check_fingerprint(result, "Radiator Valve")

        elif 'Motion' in node:
            _check_fingerprint(result, "Room Sensor")

        elif 'Indicator' in node:
            _check_fingerprint(result, "Room Thermostat")

        else:  # unknown device fingerprint
            if result['type']:
                _LOGGER.debug("Device %s: Can't obtain a fingerprint",
                    result['id'])
            else:
                _LOGGER.error("Device %s: Can't obtain a fingerprint",
                    result['id'])

        # Determine Device assignedZones...
        result['assignedZones'] = [{'name': None}]
        node = raw_dict['childValues']['location']
        if node['val']:
            result['assignedZones'] = [{'name': node['val']}]

        # Determine Device state...
        state = result['state'] = {}
        node = raw_dict['childValues']

        # DCCR, PLUG = ['outputOnOff']
        # VALV, ROMT = ['batteryLevel', 'setTemperature', 'measuredTemperature']
        # ROMS =  ['batteryLevel',  'measuredTemperature', 'luminance',  'occupancyTrigger']
        # RADR = ['batteryLevel', 'setTemperature']
        # RADR = ['outputOnOff', 'measuredTemperature']

        # if result['type'] in ["Electric Switch"]:
        if 'SwitchBinary' in node:
            state['outputOnOff'] = node['SwitchBinary']['val'] != 0

        # if result['type'] in ["Genius Valve", "Room Sensor", "Room Thermostat"]:
        if 'Battery' in node:
            state['batteryLevel'] = node['Battery']['val']

        # if result['type'] in ["Genius Valve", "Room Thermostat"]:
        if 'HEATING_1' in node:
            state['setTemperature'] = node['HEATING_1']['val']

        # if result['type'] in ["Electric Switch", "Genius Valve", "Room Sensor", "Room Thermostat"]:
        if 'TEMPERATURE' in node:
            state['measuredTemperature'] = node['TEMPERATURE']['val']

        if 'LUMINANCE' in node:
            state['luminance'] = node['LUMINANCE']['val']

        if 'Motion' in node:
            state['occupancyTrigger'] = node['Motion']['val']

        return result

    def _convert_issue(self, raw_dict) -> dict:
        """Convert a v3 issues's dict/json to the v1 schema."""
        if self._api_v1:
            return raw_dict

        description = DESCRIPTION_TO_TEXT.get(raw_dict['id'], raw_dict['id'])

        if '{zone}' in description and '{device}' in description:
            zone = raw_dict['zone_name']
            device = self.device_by_id[raw_dict['data']['nodeID']].type
            description = description.format(zone=zone, device=device)

        elif '{zone}' in description:
            zone = raw_dict['zone_name']
            description = description.format(zone)

        elif '{device}' in description:
            device = self.device_by_id[raw_dict['data']['nodeID']].type
            description = description.format(device)

        level = LEVEL_TO_TEXT.get(raw_dict['level'], raw_dict['level'])

        return {'description': description, 'level': level}

    async def _request(self, method, url, data=None):
        _LOGGER.debug("_request(method=%s, url='%s', data='%s')",
                      method, url, data)

        http_method = {
            "GET": self._client._session.get,
            "PATCH": self._client._session.patch,
            "POST": self._client._session.post,
            "PUT": self._client._session.put,
        }.get(method)

        try:
            _LOGGER.debug("_request(): 1st try: method=%s url=%s data=%s",
                          method, url, data)
            async with http_method(
                self._client._url_base + url,
                json=data,
                headers=self._client._headers,
                auth=self._client._auth,
                timeout=self._client._timeout
            ) as resp:
                assert resp.status == HTTP_OK
                response = await resp.json(content_type=None)
            if method != 'GET':
                _LOGGER.debug(
                    "_request(method=%s, url=%s, data=%s): response: %s",
                    method, url, data, response)
            return response

        except aiohttp.client_exceptions.ServerDisconnectedError as err:
            _LOGGER.warning("_request(): 2nd try: method=%s url=%s data=%s. "
                            "Exception was: ServerDisconnected, message: %s",
                            method, url, data, err)
            _session = aiohttp.ClientSession()
            async with http_method(
                self._client._url_base + url,
                json=data,
                headers=self._client._headers,
                auth=self._client._auth,
                timeout=self._client._timeout
            ) as resp:
                assert resp.status == HTTP_OK
                response = await resp.json(content_type=None)
            if method != 'GET':
                _LOGGER.debug(
                    "_request(method=%s, url=%s, data=%s): response: %s",
                    method, url, data, response)
            await _session.close()
            return response

        # except concurrent.futures._base.TimeoutError as err:


class GeniusHub(GeniusObject):
    """The class for a Genius Hub."""
    # conn.post("/v3/system/reboot", { username: e, password: t, json:{} })
    # conn.get("/v3/auth/test", { username: e, password: t, timeout: n })

    def __init__(self, client, hub_dict):
        _LOGGER.info("GeniusHub(client, hub=%s)", hub_dict['id'])
        super().__init__(client, hub_dict)

        self._info = {}  # a dict of attrs
        self._zones = []  # a list of dicts
        self._devices = []  # a list of dicts
        self._issues = []  # a list of dicts

        self._info_raw = None
        self._issues_raw = self._devices_raw = self._zones_raw = None

    async def update(self):
        """Update the Hub with its latest state data."""
        _LOGGER.debug("Hub(%s).update()", self.id)

        def _populate_zone(zone_raw):
            hub = self  # for now, only Hubs invoke this method
            zone_dict = self._convert_zone(zone_raw)

            zone_id = zone_dict['id']
            try:  # does the hub already know about this device?
                zone = hub.zone_by_id[zone_id]
            except KeyError:
                _LOGGER.debug("Creating a Zone (hub=%s, zone=%s)",
                              hub.id, zone_dict['id'])
                zone = GeniusZone(self._client, zone_dict, hub)
                # await zone.update()

                hub.zone_objs.append(zone)
                hub.zone_by_id[zone.id] = zone
                hub.zone_by_name[zone.name] = zone
            else:
                _LOGGER.debug("Found a Zone (hub=%s, zone=%s)",
                              hub.id, zone_dict['id'])

            zone.__dict__.update(zone_dict)
            zone._info_raw = zone_raw

            return zone_dict['id'], zone

        def _populate_device(device_raw):
            # TODO: maybe? _populate_device(self, device_raw, parent_zone=None)
            device_dict = self._convert_device(device_raw)

            if isinstance(self, GeniusHub):
                hub = self
                # or parent if None?
                name = device_dict['assignedZones'][0]['name']
                zone = hub.zone_by_name[name] if name else None
            else:
                hub = self.hub
                zone = self

            device_id = device_dict['id']
            try:  # does the Hub already know about this device?
                device = hub.device_by_id[device_id]
            except KeyError:
                _LOGGER.debug("Creating a Device (device=%s, hub=%s, zone=??)",
                              device_dict['id'], hub.id)
                device = GeniusDevice(self._client, device_dict, hub, zone)
                # await device.update()

                hub.device_objs.append(device)
                hub.device_by_id[device.id] = device
            else:
                _LOGGER.debug("Found a Device (hub=%s, device=%s)",
                              hub.id, device_dict['id'])

            if zone:
                try:  # does the (parent) Zone already know about this device?
                    device = zone.device_by_id[device_id]
                except KeyError:
                    _LOGGER.debug("Adding a Device (zone=%s, device=%s)",
                                  zone.id, device_dict['id'])
                    zone.device_objs.append(device)
                    zone.device_by_id[device.id] = device
                else:
                    _LOGGER.debug("Found a Device (zone=%s, device=%s)",
                                  zone.id, device_dict['id'])

            # TODO: this code may be redundant
            if isinstance(self, GeniusZone):
                # TODO: remove this
                print("LOOK FOR THIS IN THE LIBRARY")
                try:  # does the zone already know about this device?
                    device = self.device_by_id[device_id]
                except KeyError:
                    self.device_objs.append(device)
                    self.device_by_id[device.id] = device

            device.__dict__.update(device_dict)
            device._info_raw = device_raw

            return device_dict['id'], device

        def _populate_issue(issue_raw):
            hub = self  # for now, only Hubs invoke this method
            issue_dict = self._convert_issue(issue_raw)

            _LOGGER.debug("Found an Issue (hub=%s, zone=%s, issue=%s)",
                          hub.id, "TBD", issue_dict)

            return issue_dict['description'], None

        for z in await self._get_zones:
            _populate_zone(z)
        for d in await self._get_devices:
            _populate_device(d)
        for i in await self._get_issues:
            _populate_issue(i)

        _LOGGER.debug("Hub(%s).update(): len(hub.zone_objs) = %s",
                      self.id, len(self.zone_objs))
        _LOGGER.debug("Hub(%s).update(): len(hub.device_objs) = %s",
                      self.id, len(self.device_objs))
        _LOGGER.debug("Hub(%s).update(): len(hub._issues_raw) = %s",
                      self.id, len(self._issues_raw))

    @property
    def info(self) -> dict:
        """Return all information for the hub."""
        _LOGGER.debug("Hub(%s).info", self.id)

        keys = ['device_by_id', 'device_objs',
                'zone_by_id', 'zone_by_name', 'zone_objs']
        info = _without_keys(self.__dict__, keys)

        _LOGGER.debug("Hub(%s).info = %s", self.id, info)
        return info

    @property
    async def _get_zones(self) -> list:
        """Return a list (of dicts) of zones included in the system."""
        # getAllZonesData = x.get("/v3/zones", {username: e, password: t})

        raw_json = await self._request("GET", 'zones')
        if self._api_v1:
            self._zones_raw = raw_json
        else:
            self._zones_raw = _extract_zones_from_zones(raw_json['data'])

        _LOGGER.debug("Hub()._get_zones(): len(self._zones_raw) = %s",
                      len(self._zones_raw))
        return self._zones_raw

    @property
    def zones(self) -> list:
        """Return a list of Zones known to the Hub.

          v1/zones/summary: id, name
          v1/zones: id, name, type, mode, temperature, setpoint, occupied,
          override, schedule
        """
        self._zones = [self._convert_zone(z) for z in self._zones_raw]

        _LOGGER.debug("Hub().zones: len(self._devices) = %s",
                      len(self._devices))
        return self._zones

    @property
    async def _get_devices(self) -> list:
        """Return a list (of dicts) of devices included in the system."""
        # getDeviceList = x.get("/v3/data_manager", {username: e, password: t})

        if not self._api_v1:  # required for Dual Channel detection...
            # WORKAROUND: There's a aiohttp.ServerDisconnectedError on 2nd HTTP
            # method (2nd GET v3/zones or GET v3/zones & get /data_manager) if
            # it is done the v1 way (above) for v3
            self._devices_raw = _extract_devices_from_zones(
                self._zones_raw)
        # son = await self._request('GET', 'devices' if self._api_v1 else 'zones')
        else:
            raw_json = await self._request('GET',
                                           'devices' if self._api_v1 else 'data_manager')
            if self._api_v1:
                self._devices_raw = raw_json
            else:
                self._devices_raw = _extract_devices_from_data_manager(
                    raw_json['data'])

        _LOGGER.debug("Hub()._get_devices(): len(self._devices_raw) = %s",
                      len(self._devices_raw))
        return self._devices_raw

    @property
    def devices(self) -> list:
        """Return a list of Devices known to the Hub.

          v1/devices/summary: id, type
          v1/devices: id, type, assignedZones, state
        """
        self._devices = [self._convert_device(d) for d in self._devices_raw]

        # Hack v3 output match v1: add missing Dual channel controller
        if not self._api_v1:
            for device in self._devices:
                if '-1' in device['id']:
                    new_device = dict(device)
                    new_device['id'] = device['id'][0]
                    new_device['type'] = 'Dual Channel Receiver'
                    new_device['assignedZones'] = [{'name': None}]
                    self._devices.append(new_device)
                    break

        self._devices = natural_sort(self._devices, 'id')

        _LOGGER.debug("Hub().devices: len(self._devices) = %s",
                      len(self._devices))
        return self._devices

    @property
    async def _get_issues(self) -> list:
        """Return a list (of dicts) of issues known to the hub."""

        if self._api_v1:
            self._issues_raw = await self._request('GET', 'issues')
        else:
            self._issues_raw = _extract_issues_from_zones(
                self._zones_raw)

        _LOGGER.info("Hub()._get_issues(): len(self._issues_raw) = %s",
                     len(self._issues_raw))
        return self._issues_raw

    @property
    def issues(self) -> list:
        """Return a list of Issues known to the Hub.

          v1/issues: ???
        """

        if self._api_v1:
            self._issues = self._issues_raw
        else:
            self._issues = [self._convert_issue(d) for d in self._issues_raw]

        _LOGGER.debug("Hub().issues: len(self._issues) = %s",
                      len(self._issues))
        return self._issues


class GeniusZone(GeniusObject):
    """The class for Genius Zone."""

    def __init__(self, client, zone_dict, hub):
        _LOGGER.info("GeniusZone(hub=%s, zone['id]=%s)",
                     hub.id, zone_dict['id'])
        super().__init__(client, zone_dict, hub=hub)

        self._info = {}
        self._devices = []
        self._issues = []

        self._info_raw = None
        self._issues_raw = self._devices_raw = None

    @property
    def info(self) -> dict:
        """Return all information for a zone."""
        _LOGGER.debug("Zone(%s).info", self.id)

        keys = ['device_by_id', 'device_objs']
        info = _without_keys(self.__dict__, keys)

        _LOGGER.debug("Zone(%s).info = %s", self.id, info)
        return info

    @property
    def devices(self) -> list:
        """Return information for devices assigned to a zone.

          This is a v1 API: GET /zones/{zoneId}devices
        """
        self._devices = [self._convert_device(d) for d in self._devices_raw
                         if d['assignedZone'] == self.name]

        # self._devices = []
        # for device in self.device_objs:
        #     self._devices.append(device.info)

        _LOGGER.debug("Zone(%s).devices: len(self._devices) = %s",
                      self.id, len(self._devices))
        return self._devices

    @property
    def issues(self) -> list:
        """Return a list of Issues known to the Zone."""

        self._issues = [self._convert_issue(i) for i in self._issues_raw]

        _LOGGER.debug("Hub().devices: len(self._devices) = %s",
                      len(self._devices))
        return self._issues

    @property
    def schedule(self) -> list:
        """Return the list of scheduled setpoints for this Zone."""
        raise NotImplementedError()

    async def set_mode(self, mode):
        """Set the mode of the zone.

          mode is in {'off', 'timer', footprint', 'override'}
        """
        # TODO: device-specific logic to prevent placing into an invalid mode
        # TODO: e.g. zones only support footprint if they have a PIR
        ALLOWED_MODES = [ZONE_MODES.Off, ZONE_MODES.Override, ZONE_MODES.Timer]
        ALLOWED_MODE_STRS = [IMODE_TO_MODE[i] for i in ALLOWED_MODES]

        if hasattr(self, 'occupied'):
            ALLOWED_IMODES += [ZONE_MODES.Footprint]

        if isinstance(mode, int) and mode in ALLOWED_MODES:
            mode_str = IMODE_TO_MODE[mode]
        elif isinstance(mode, str) and mode in ALLOWED_MODE_STRS:
            mode_str = mode
            mode = MODE_TO_IMODE[mode_str]
        else:
            raise TypeError(
                "Zone.set_mode(): mode={} isn't valid (str/int).".format(mode))

        _LOGGER.debug("Zone(%s).set_mode(mode=%s, mode_str='%s')...",
                      self.id, mode, mode_str)

        if self._api_v1:
            # v1 API uses strings
            url = 'zones/{}/mode'
            resp = await self._request("PUT", url.format(self.id),
                                       data=mode_str)
        else:
            # v3 API uses dicts
            # TODO: check PUT(POST?) vs PATCH
            url = 'zone/{}'
            resp = await self._request("PATCH", url.format(self.id),
                                       data={'iMode': mode})

        if resp:  # for v1, resp = None?
            resp = resp['data'] if resp['error'] == 0 else resp
        _LOGGER.debug("set_mode(%s): done, response = %s", self.id, resp)

    async def set_override(self, setpoint=None, duration=3600):
        """Set the zone to override to a certain temperature.

          duration is in seconds
          setpoint is in degrees Celsius
        """
        setpoint = self.setpoint if setpoint is None else setpoint

        _LOGGER.debug("Zone(%s).set_override(setpoint=%s, duration=%s)...",
                      self.id, setpoint, duration)

        if self._api_v1:
            url = 'zones/{}/override'
            data = {'setpoint': setpoint, 'duration': duration}
            resp = await self._request("POST", url.format(self.id), data=data)
        else:
            url = 'zone/{}'
            data = {'iMode': ZONE_MODES.Boost,
                    'fBoostSP': setpoint,
                    'iBoostTimeRemaining': duration}
            resp = await self._request("PATCH", url.format(self.id), data=data)

        if resp:  # for v1, resp = None?
            resp = resp['data'] if resp['error'] == 0 else resp
        _LOGGER.debug(
            "set_override_temp(%s): done, response = %s", self.id, resp)

    async def update(self):
        """Update the Zone with its latest state data."""
        _LOGGER.debug("Zone(%s).update(xx)", self.id)

        if self._api_v1:
            _LOGGER.debug("Zone(%s).update(v1): type = %s",
                          self.id, type(self))
            url = 'zones/{}'
            data = await self._request("GET", url.format(self.id))
            self.__dict__.update(data)
        else:  # a WORKAROUND...
            _LOGGER.debug("Zone(%s).update(v3): type = %s",
                          self.id, type(self))
            await self.hub.update()


class GeniusDevice(GeniusObject):
    """The class for Genius Device."""

    def __init__(self, client, device_dict, hub, zone=None):
        _LOGGER.info("GeniusZone(hub=%s, zone=%s,device['id']=%s)",
                     hub.id, zone, device_dict['id'])
        super().__init__(client, device_dict, hub=hub, assignedZone=zone)

        self._info = {}
        self._issues = []

        self._info_raw = None
        self._issues_raw = None

    @property
    def info(self) -> dict:
        """Return all information for a device."""
        _LOGGER.debug("Device(%s).info: type = %s", self.id, type(self))

        keys = []
        info = _without_keys(self.__dict__, keys)

        _LOGGER.debug("Device(%s).info = %s", self.id, info)
        return info

    @property
    def location(self) -> dict:  # aka assignedZones
        """Return the parent Zone of this Device."""
        raise NotImplementedError()

    async def update(self):
        """Update the Device with its latest state data."""
        _LOGGER.debug("Device(%s).update(xx)", self.id)

        if self._api_v1:
            _LOGGER.debug("Device(%s).update(v1): type = %s",
                          self.id, type(self))
            url = 'devices/{}'
            data = await self._request("GET", url.format(self.id))
            self.__dict__.update(data)
        else:  # a WORKAROUND...
            await self.hub.update()
            _LOGGER.debug("Device(%s).update(v3): type = %s",
                          self.id, type(self))
