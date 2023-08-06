"""OpenHlTest Restconf transport
"""

import sys
import os
import ssl
import time
import json
import requests
import logging
import copy
from datetime import datetime

class HttpError(Exception):
    def __init__(self, response):
        """The base error class for all OpenHlTest errors"""
        self._status_code = response.status_code
        self._reason = response.reason
        self._text = response.text
        print response.content

    @property
    def message(self):
        return '%s %s %s' % (self._status_code, self._reason, self._text)

class AlreadyExistsError(HttpError):
    def __init__(self, response):
        """The requested object exists on the server"""
        super(AlreadyExistsError, self).__init__(response)

class BadRequestError(HttpError):
    def __init__(self, response):
        """The server has determined that the request is incorrect"""
        super(BadRequestError, self).__init__(response)

class NotFoundError(HttpError):
    def __init__(self, response):
        """The requested object does not exist on the server"""
        super(NotFoundError, self).__init__(response)

class ServerError(HttpError):
    def __init__(self, response):
        """The server has encountered an uncategorized error condition"""
        super(ServerError, self).__init__(response)

def _ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

class HttpTransport(object):
    """OpenHlTest Restconf transport."""
    LOGGER_NAME = 'openhltest'

    def __init__(self, hostname, rest_port=443):
        """ Set the connection parameters to a rest server

        Args:
            hostname (str): hostname or ip address
            rest_port (int, optional, default=443): the rest port of the server
        """
        if sys.version < '2.7.9':
            import requests.packages.urllib3
            requests.packages.urllib3.disable_warnings()
        else:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._headers = {}
        self._verify_cert = False
        self.trace = False
        self._scheme = 'https'
        self._connection = '%s://%s:%s' % (self._scheme, hostname, rest_port)
        now = datetime.now()
        date_time = now.strftime('%Y-%m-%d_%H-%M-%S')

        if os.name == 'nt':
            log_path = os.environ.get('USERPROFILE', 'c:/')
            log_path = os.path.join( log_path, 'Documents\\Spirent\\TestCenter\\Logs\\openhlt')
        else:
            log_path = os.environ.get('HOME', '/tmp')
            log_path = os.path.join( log_path, 'Spirent/TestCenter/Logs')
        if not os.path.exists( log_path):
            os.makedirs( log_path)
        log_file_name = os.path.join( log_path, "oht_%s.log" % date_time)
        print('Log file: %s' % log_file_name)
        if len(logging.getLogger(HttpTransport.LOGGER_NAME).handlers) == 0:
            handlers = []
            if log_file_name is not None:
                handlers.append(logging.FileHandler(log_file_name, mode='w'))
            formatter = logging.Formatter(fmt='%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            formatter.converter = time.gmtime
            for handler in handlers:
                handler.setFormatter(formatter)
                logging.getLogger(HttpTransport.LOGGER_NAME).addHandler(handler)
            logging.getLogger(HttpTransport.LOGGER_NAME).setLevel(logging.INFO)
            logging.getLogger(HttpTransport.LOGGER_NAME).info('using python version %s' % sys.version)
            # try:
            #     version = pkg_resources.get_distribution("openhltest").version
            #     logging.getLogger(HttpTransport.LOGGER_NAME).info('using openhltest version %s' % version)
            # except Exception as e:
            #     logging.getLogger(HttpTransport.LOGGER_NAME).warn("openhltest not installed using pip, unable to determine version")

    def console_log(self, switch = True):
        handler = logging.StreamHandler(sys.stdout)
        if True == switch:
            formatter = logging.Formatter(fmt='%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            formatter.converter = time.gmtime
            handler.setFormatter(formatter)
            try:
                logging.getLogger(HttpTransport.LOGGER_NAME).addHandler(handler)
            except Exception as e:
                print(e)
        else:
            try:
                logging.getLogger(HttpTransport.LOGGER_NAME).removeHandler(handler)
            except Exception as e:
                print(e)

    @property
    def trace(self):
        """bool: Trace all requests and responses."""
        return self._trace
    @trace.setter
    def trace(self, value):
        self._trace = value

    def _get(self, target):
        response = self._send_recv('GET', target.url)
        return self._populate_target(response, target)

    def _create(self, parent, target, arg_dict):
        object_key = '%s:%s' % (target.YANG_MODULE, target.YANG_CLASS)
        payload = { object_key: {} }
        for key in arg_dict.keys():
            if key == 'self':
                continue
            #payload[object_key][key] = arg_dict[key]
            payload[object_key] = [{key: arg_dict[key]}]
        location = self._send_recv('POST', parent.url, payload)
        return self._get(target)

    def _update(self, url, payload):
        return self._send_recv('PATCH', url, payload)

    def _delete(self, url):
        return self._send_recv('DELETE', url)

    def _execute(self, url, payload):
        return self._send_recv('POST', url, payload)

    def set_debug_level(self):
        logging.getLogger(HttpTransport.LOGGER_NAME).setLevel(logging.DEBUG)

    def set_warn_level(self):
        logging.getLogger(HttpTransport.LOGGER_NAME).setLevel(logging.WARN)

    def set_info_level(self):
        logging.getLogger(HttpTransport.LOGGER_NAME).setLevel(logging.INFO)

    def info(self, message):
        """Add an INFO level message to the logging handlers
        """
        logging.getLogger(HttpTransport.LOGGER_NAME).info(message)

    def warn(self, message):
        """Add a WARN level message to the logging handlers
        """
        logging.getLogger(HttpTransport.LOGGER_NAME).warn(message)

    def debug(self, message):
        """Add a DEBUG level message to the logging handlers
        """
        logging.getLogger(HttpTransport.LOGGER_NAME).debug(message)

    def _print_trace(self, * args):
        if self.trace is True:
            print('%s %s' % (int(time.time()), ' '.join(args)))
 
    def _value_trim(self, node):
        if isinstance(node, dict):
            for key in node.keys():
                if isinstance(node[key], dict):
                    self._value_trim(node[key])
                else:
                    if isinstance(node[key], str) and len( node[key]) > 1024:
                        node[key] = node[key][0:1023] + '...'
        
    def _log_request(self, method, url, headers, payload):
        message = '%s: %s' % (method, url)
        for key in headers.keys():
           message += '\n%s: %s' % (key, headers[key])
        if payload is not None:
            trimed_payload = copy.deepcopy(payload)
            if isinstance(trimed_payload, str):
                trimed_payload = json.loads( trimed_payload, object_hook=_ascii_encode_dict)
            self._value_trim( trimed_payload)
            message += "\n" + json.dumps(trimed_payload, indent=4)
        self.info(message)

    def _log_response(self, response):
        message = '%s %s' % (response.status_code, response.reason)
        for key in response.headers.keys():
            message += '\n%s: %s' % (key, response.headers[key])
        if response.content is not None and len(response.content) != 0:
            if response.headers.get('Content-Type', '') == 'application/json':
                trimed_content = copy.deepcopy(response.content)
                if isinstance(trimed_content, str):
                    trimed_content = json.loads( trimed_content, object_hook=_ascii_encode_dict)
                self._value_trim( trimed_content)
                message += "\n" + json.dumps(trimed_content, indent=4)
        self.info(message)

    def _send_recv(self, method, url, payload=None, fid=None, file_content=None):
        headers = self._headers
        if url.startswith(self._scheme) == False:
            url = '%s/%s' % (self._connection, url.strip('/'))

        if payload is not None:
            headers['Content-Type'] = 'application/json'
            if isinstance(payload, dict) is True:
                payload = json.dumps(payload)
            self._log_request( method, url, headers, payload)
            response = requests.request(method, url, data=payload, headers=headers, verify=self._verify_cert)
        elif method == 'POST' and fid is not None:
            headers['Content-Type'] = 'application/octet-stream'
            if fid.__class__.__name__ == 'BufferedReader':
                headers['Content-Length'] = os.fstat(fid.raw.fileno()).st_size
                self._log_request( method, url, headers, fid.raw)
                response = requests.request(method, url, data=fid.raw, headers=headers, verify=self._verify_cert)
            else:                            
                self._log_request( method, url, headers, fid)
                response = requests.request(method, url, data=fid, headers=headers, verify=self._verify_cert)
        elif method == 'POST' and file_content is not None:
            headers['Content-Type'] = 'application/octet-stream'
            self._log_request( method, url, headers, json.dumps(file_content))
            response = requests.request(method, url, data=json.dumps(file_content), headers=headers, verify=self._verify_cert)
        else:
            self._log_request( method, url, headers, None)
            response = requests.request(method, url, data=None, headers=headers, verify=self._verify_cert)

        while(response.status_code == 202):
            time.sleep(1)
            location = response.headers['Location']
            if location.startswith('/') is True:
                location = '%s%s' % (self._connection, location)
            #self._print_trace('GET', location)
            response = requests.request('GET', location, verify=self._verify_cert)
        self._log_response(response)
            
        if response.status_code == 201:
            return response.headers['Location']
        elif response.status_code == 204:
            return None
        elif str(response.status_code).startswith('2') is True:
            if response.headers.get('Content-Type'):
                if 'application/json' in response.headers['Content-Type']:
                    #self._print_trace("\t cotent: %s" % response.json())
                    return response.json()
            return None
        elif response.status_code == 400:
            raise BadRequestError(response)
        elif response.status_code == 404:
            raise NotFoundError(response)
        elif response.status_code == 409:
            raise AlreadyExistsError(response)
        else:
            raise ServerError(response)

    def _populate_target(self, payload, target):
        payload = payload['%s:%s' % (target.YANG_MODULE, target.YANG_CLASS)]
        if isinstance(payload, list):
            if len(payload) > 1 :
                target_list = []
                for item in payload:
                    target_item = target._create_sibling(item[target.YANG_KEY])
                    target_item._values = item
                    target_list.append(target_item)
                return target_list
            else :
                target._values = payload[0] 
        else:
            target._values = payload
        return target

