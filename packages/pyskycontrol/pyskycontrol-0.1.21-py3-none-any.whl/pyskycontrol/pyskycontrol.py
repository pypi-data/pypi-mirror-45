"""
Sky TV - Platforms
"""

import re
import math
import array
import socket
import logging
import requests
import time
import datetime
from .const import urls, commands
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)


class Sky:
    """Sky Control Class"""

    def __init__(self):
        """Initialise Sky Attributes"""
        self.port = 49160
        self.search_timeout = 5
        self.devices = []
        self.hosts = None
        self.dict_channel_list = None
        self.urls = urls
        self.commands = commands

    def search_boxes(self, timeout):
        """Search for Sky Q Boxes on local network"""
        device = {}

        if self.hosts is None:
            msg = \
                'M-SEARCH * HTTP/1.1\r\n' \
                'HOST:239.255.255.250:1900\r\n' \
                'ST:upnp:rootdevice\r\n' \
                'MX:2\r\n' \
                'MAN:"ssdp:discover"\r\n' \
                '\r\n'

            # Set up UDP socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                              socket.IPPROTO_UDP)
            s.settimeout(timeout)
            s.sendto(msg.encode(), ('239.255.255.250', 1900))

            try:
                while True:
                    data, addr = s.recvfrom(65507)
                    data_text = data.decode("utf-8")
                    url = re.search("(?P<url>https?://[^\s]+)",
                                    data_text).group("url")
                    if "Sky" in data_text:
                        if addr[0] not in device:
                            device[addr[0]] = []
                        device[addr[0]].append(url)
            except socket.timeout:
                pass
        else:
            ip_address = self.hosts
            for a in ip_address:
                device[a] = []
                for i in range(10):
                    url = 'http://{0}:49153/description{1}.xml'
                    device[a].append(url.format(a, i))

        compl = []
        for IP in device:
            for url in device[IP]:
                if IP in compl:
                    break
                else:
                    try:
                        headers = {
                            'USER-AGENT': 'SKY_skyplus',
                            'CONTENT-TYPE': 'text/xml; charset="utf-8"'
                        }
                        request = requests.get(url=url, data=None,
                                               headers=headers)
                        response = BeautifulSoup(
                            request.text, 'lxml-xml')
                        base_url = response.find(
                            'URLBase').string[:-1]
                        for node in response.find_all('service'):
                            service = node.serviceType.string
                            ctrl_url = base_url + node.controlURL.string
                            scpd_url = base_url + node.SCPDURL.string

                            if "SkyPlay:2" in service and \
                                    "player_avt.xml" in scpd_url:
                                result = self.request(request_type="GET",
                                                      response_type='JSON',
                                                      target=IP,
                                                      request_url=self.urls[
                                                          "info_url"])
                                name = result["btID"]
                                self.devices.append({"IP": IP,
                                                     "PORT": self.port,
                                                     "NAME": name,
                                                     "XML_URL": url,
                                                     "CONTROL_URL": ctrl_url,
                                                     "SCPD_URL": scpd_url,
                                                     "SERVICE_TYPE": service})
                                compl.append(IP)
                    except:
                        pass

        return self.devices

    @staticmethod
    def epochtime(date_time, pattern, action):
        """ date/time conversion to epoch"""
        if action == 'to_epoch':
            pattern = '%d.%m.%Y %H:%M:%S'
            epochtime = int(time.mktime(
                time.strptime(str(date_time), pattern)))
            return epochtime
        elif action == 'from_epoch':
            date = datetime.fromtimestamp(int(date_time)).strftime(pattern)
            return date

    @staticmethod
    def get_sec(epoch):
        """Convert epoch time into total seconds."""
        clock = time.strftime('%H:%M:%S', time.localtime(epoch))
        h, m, s = clock.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)

    def request(self, request_type, response_type, target, request_url):
        """JSON Call to Sky Box"""
        json_url = request_url
        response = None
        if target != "N/A":
            json_url = self.urls["start"] + str(target) + str(request_url)

        if request_type == 'POST':
            response = requests.post(json_url, data=None, headers=None)
        elif request_type == 'GET':
            response = requests.get(json_url, data=None, headers=None)

        if response_type == 'JSON':
            json_data = response.json()
            return json_data
        else:
            return response

    @staticmethod
    def soap_request(command, ctrl_url):
        """Make a Soap request"""
        xml = """<?xml version="1.0" encoding="utf-8"?>
                <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
                <s:Body>
                <u:{} xmlns:u="urn:schemas-nds-com:service:SkyPlay:2">
                <InstanceID>0</InstanceID>
                </u:{}>
                </s:Body>
                </s:Envelope>""".format(command, command)

        headers = {
            "Content-Length": "{}".format(len(xml)),
            "SOAPACTION":
                "\"urn:schemas-nds-com:service:SkyPlay:2#{}\"".format(command),
            "Content-Type": "text/xml; char-set=utf-8"}

        xml_response = requests.post(url=ctrl_url, data=xml, headers=headers)
        return BeautifulSoup(xml_response.text, "lxml-xml")

    def soap_status(self, host, ctrl_url):
        """Send soap command to the Sky Q box to get status"""
        test = self.request(request_type="GET",
                            response_type="JSON",
                            target=host,
                            request_url=self.urls["info_url"])

        if test["activeStandby"] != True:
            command = "GetTransportInfo"
            response = self.soap_request(command, ctrl_url)
            return response.find('CurrentTransportState').string
        else:
            response = 'STOPPED'
            return response

    def channel_epg(self, host):
        """Get the Sky EPG"""
        channel_list = {}
        request = self.request(request_type="GET",
                               response_type="JSON",
                               target=host,
                               request_url=self.urls["channel_epg"])
        channels = request['services']
        for channel in channels:
            if channel["t"] not in channel_list:
                channel_list.update({channel["t"]: channel})
        channel_list.update({'Recording': {'sid': '0', 't': 'Recording'}})
        self.dict_channel_list = channel_list
        return channel_list

    def current_program(self, host, ctrl_url):
        """Get the current channel"""
        data = {}
        ps = None
        prog_type = None
        ch = None
        channel = None
        desc = None
        command = "GetMediaInfo"

        response = self.soap_request(command, ctrl_url)
        soap_result = response.find('CurrentURI').string

        if soap_result is None:
            data.update({'pvr_sid': 'off'})
            return data
        elif 'xsi' in soap_result:
            prog_type = 'Channel'
            ps = str(int(re.split('\\bxsi://\\b', soap_result)[-1], 16))
            data.update({'pvr_sid': ps})
            data.update({'type': prog_type})
        elif 'pvr' in soap_result:
            prog_type = 'Recording'
            ps = "P" + re.split('\\bfile://pvr/\\b', soap_result)[-1].lower()
            data.update({'pvr_sid': ps})
            data.update({'type': prog_type})

        if prog_type == 'Channel':
            d = datetime.datetime.now()
            d_date = d.strftime('%Y%m%d')
            response = self.request(request_type='GET',
                                    response_type='JSON',
                                    target="N/A",
                                    request_url=self.urls["chn_list"].format(d_date, ps))
            p_list = response["schedule"][0]["events"]
            current_epoch = self.epochtime(
                datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                None, 'to_epoch')
            for prog in p_list:
                if prog["st"] + prog["d"] > current_epoch:
                    ch = prog
                    break

            for cha in self.dict_channel_list:
                if ps == self.dict_channel_list[cha]["sid"]:
                    channel = self.dict_channel_list[cha]['t']
                    data.update({"channel": channel})
                    break

        elif prog_type == 'Recording':
            response = self.request(request_type='GET',
                                    response_type='JSON',
                                    target=host,
                                    request_url=self.urls["rec_list"])
            p_list = response["pvrItems"]
            for rec in p_list:
                if rec["pvrid"] == ps:
                    ch = rec
                    if 'cn' in ch:
                        channel = ch['cn']
                        data.update({"channel": channel})
                    if 'osid' in ch:
                        ps = ch['osid']
                    break

        if ch is not None:
            if 't' in ch:
                title = ch['t']
                data.update({"title": title})
            if 'sy' in ch:
                desc = ch['sy']
                if ':' in desc:
                    s_t = desc.split(":")
                    series_title = s_t[0]
                    data.update({'series_title': series_title})
            if 'seasonnumber' in ch and 'episodenumber' in ch:
                season = ch['seasonnumber']
                episode = ch['episodenumber']
                data.update({"season": season})
                data.update({"episode": episode})
                source_type = 'TV'
                data.update({"source_type": source_type})
            else:
                source_type = 'Video'
                data.update({"source_type": source_type})
            if 'programmeuuid' in ch:
                programmeuuid = ch['programmeuuid']
                imageurl = self.urls['metadata_url'].format(
                    str(programmeuuid), str(ps))
                data.update({"imageurl": imageurl})

        _LOGGER.debug(data)
        return data

    def sendcommand(self, host, port, command):
        """Send command to the Sky Q box"""
        code = self.commands[command]
        cmd1 = int(math.floor(224 + (code / 16)))
        cmd2 = int(code % 16)
        command1 = array.array('B', [4, 1, 0, 0, 0, 0, cmd1, cmd2]).tostring()
        command2 = array.array('B', [4, 0, 0, 0, 0, 0, cmd1, cmd2]).tostring()

        s = socket.socket()
        s.connect((host, port))  # connect to Sky TV box
        reply = s.recv(12)  # Receive handshake
        s.send(reply)  # send handshake
        reply = s.recv(2)  # Receive 2 bytes
        s.send(reply)  # send 1 byte
        reply = s.recv(24)  # Receive 24 bytes

        s.send(command1)  # send command bytes part 1
        s.send(command2)  # send command bytes part 2

        s.close()  # close connection
