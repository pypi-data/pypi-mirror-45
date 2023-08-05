"""This module gives a way to access the configuration of a locally installed
instance of Snips, a Snips assistant and a Snips skill.

Classes:

- :class:`.AppConfig`: Gives access to the configuration of a Snips app,
  stored in an INI file.
- :class:`.AssistantConfig`: Gives access to the configuration of a Snips
  assistant, stored in a JSON file.
- :class:`.MQTTAuthConfig`: Represents the authentication settings for a
  connection to an MQTT broker.
- :class:`.MQTTConfig`: Represents the configuration for a connection to an
  MQTT broker.
- :class:`.MQTTTLSConfig`: Represents the TLS settings for a connection to an
  MQTT broker.
- :class:`.SnipsConfig`: Gives access to the configuration of a locally
  installed instance of Snips, stored in a TOML file.
"""

from collections import UserDict
from configparser import ConfigParser
import json
from pathlib import Path

from snipskit.exceptions import AssistantConfigNotFoundError, \
    SnipsConfigNotFoundError
from snipskit.tools import find_path
import toml

SEARCH_PATH_SNIPS = ['/etc/snips.toml', '/usr/local/etc/snips.toml']
SEARCH_PATH_ASSISTANT = ['/usr/share/snips/assistant/assistant.json',
                         '/usr/local/share/snips/assistant/assistant.json']

DEFAULT_BROKER = 'localhost:1883'


class AppConfig(ConfigParser):
    """This class gives access to the configuration of a Snips app as a
    :class:`configparser.ConfigParser` object.

    Attributes:
        filename (str): The filename of the configuration file.

    Example:
        >>> config = AppConfig()  # Use default file config.ini
        >>> config['secret']['api-key']
        'foobar'
        >>> config['secret']['api-key'] = 'barfoo'
        >>> config.write()
    """

    def __init__(self, filename=None):
        """Initialize an :class:`.AppConfig` object.

        Args:
            filename (optional): A filename for the configuration file. If the
                filename is not specified, the default filename 'config.ini'
                in the current directory is chosen.
        """

        ConfigParser.__init__(self)

        if not filename:
            filename = 'config.ini'

        self.filename = filename

        config_path = Path(filename)

        with config_path.open('rt') as config:
            self.read_file(config)

    def write(self, *args, **kwargs):
        """Write the current configuration to the app's configuration file.

        If this method is called without any arguments, the configuration is
        written to the :attr:`filename` attribute of this object.

        If this method is called with any arguments, they are forwarded to the
        :meth:`configparser.ConfigParser.write` method of its superclass.
        """
        if len(args) + len(kwargs):
            super().write(*args, **kwargs)
        else:
            with Path(self.filename).open('wt') as config:
                super().write(config)


class AssistantConfig(UserDict):
    """This class gives access to the configuration of a Snips assistant as a
    :class:`dict`.

    Attributes:
        filename (str): The filename of the configuration file.

    Example:
        >>> assistant = AssistantConfig('/opt/assistant/assistant.json')
        >>> assistant['language']
        'en'
    """

    def __init__(self, filename=None):
        """Initialize an :class:`.AssistantConfig` object.

        Args:
            filename (str, optional): The path of the assistant's configuration
                file.

                If the argument is not specified, the configuration file is
                searched for in the following locations, in this order:

                - /usr/share/snips/assistant/assistant.json
                - /usr/local/share/snips/assistant/assistant.json

        Raises:
            :exc:`FileNotFoundError`: If the specified filename doesn't exist.

            :exc:`.AssistantConfigNotFoundError`: If there's no assistant
                configuration found in the search path.

            :exc:`json.JSONDecodeError`: If the assistant's configuration
                file doesn't have a valid JSON syntax.

        Examples:
            >>> assistant = AssistantConfig()  # default configuration
            >>> assistant2 = AssistantConfig('/opt/assistant/assistant.json')
        """
        if filename:
            self.filename = filename
            assistant_file = Path(filename)
        else:
            self.filename = find_path(SEARCH_PATH_ASSISTANT)

            if not self.filename:
                raise AssistantConfigNotFoundError()

            assistant_file = Path(self.filename)

        # Open the assistant's file. This raises FileNotFoundError if the
        # file doesn't exist.
        with assistant_file.open('rt') as json_file:
            # Create a dict with our configuration.
            # This raises JSONDecodeError if the file doesn't have a
            # valid JSON syntax.
            UserDict.__init__(self, json.load(json_file))


class MQTTAuthConfig:
    """This class represents the authentication settings for a connection to an
    MQTT broker.

    .. versionadded:: 0.6.0

    Attributes:
        username (str): The username to authenticate to the MQTT broker. `None`
            if there's no authentication.
        password (str): The password to authenticate to the MQTT broker. Can be
            `None`.
    """

    def __init__(self, username=None, password=None):
        """Initialize a :class:`.MQTTAuthConfig` object.

        Args:
            username (str, optional): The username to authenticate to the MQTT
                broker. `None` if there's no authentication.
            password (str, optional): The password to authenticate to the MQTT
                broker. Can be `None`.

        All arguments are optional.
        """
        self.username = username
        self.password = password

    @property
    def enabled(self):
        """Check whether authentication is enabled.

        Returns:
            bool: True if the username is not `None`.
        """
        return self.username is not None


class MQTTTLSConfig:
    """This class represents the TLS settings for a connection to an MQTT
    broker.

    .. versionadded:: 0.6.0

    Attributes:
        hostname (str, optional): The TLS hostname of the MQTT broker.
            `None` if no TLS is used.
        ca_file (str, optional): Path to the Certificate Authority file.
            Can be `None`.
        ca_path (str, optional): Path to the Certificate Authority files.
            Can be `None`.
        client_key (str, optional): Path to the private key file. Can be
           `None`.
        client_cert (str, optional): Path to the client certificate file.
            Can be `None`.
        disable_root_store (bool, optional): Whether the TLS root store is
            disabled.
    """

    def __init__(self, hostname=None, ca_file=None, ca_path=None,
                 client_key=None, client_cert=None, disable_root_store=False):
        """Initialize a :class:`.MQTTTLSConfig` object.

        Args:
            hostname (str, optional): The TLS hostname of the MQTT broker.
                `None` if no TLS is used.
            ca_file (str, optional): Path to the Certificate Authority
                file. Can be `None`.
            ca_path (str, optional): Path to the Certificate Authority
                files. Can be `None`.
            client_key (str, optional): Path to the private key file. Can
                be `None`.
            client_cert (str, optional): Path to the client certificate
                file. Can be `None`.
            disable_root_store (bool, optional): Whether the TLS root store
                is disabled. Defaults to `False`.

        All arguments are optional.
        """
        self.hostname = hostname
        self.ca_file = ca_file
        self.ca_path = ca_path
        self.client_key = client_key
        self.client_cert = client_cert
        self.disable_root_store = disable_root_store

    @property
    def enabled(self):
        """Check whether TLS is enabled.

        Returns:
            bool: True if the hostname is not `None`.
        """
        return self.hostname is not None


class MQTTConfig:
    """This class represents the configuration for a connection to an
    MQTT broker.

    .. versionadded:: 0.4.0

    Attributes:
        broker_address (str, optional): The address of the MQTT broker, in the
            form 'host:port'.
        auth (:class:`.MQTTAuthConfig`, optional): The authentication
            settings (username and password) for the MQTT broker.
        tls (:class:`.MQTTTLSConfig`, optional): The TLS settings for the MQTT
            broker.

    """
    def __init__(self, broker_address='localhost:1883', auth=None, tls=None):
        """Initialize a :class:`.MQTTConfig` object.

        Args:
            broker_address (str, optional): The address of the MQTT broker, in
                the form 'host:port'.
            auth (:class:`.MQTTAuthConfig`, optional): The authentication
                settings (username and password) for the MQTT broker. Defaults
                to a default :class:`.MQTTAuthConfig` object.
            tls (:class:`.MQTTTLSConfig`, optional): The TLS settings for the
                MQTT broker. Defaults to a default :class:`.MQTTTLSConfig`
                object.

        All arguments are optional.
        """
        self.broker_address = broker_address

        if auth is None:
            self.auth = MQTTAuthConfig()
        else:
            self.auth = auth

        if tls is None:
            self.tls = MQTTTLSConfig()
        else:
            self.tls = tls


class SnipsConfig(UserDict):
    """This class gives access to a snips.toml configuration file as a
    :class:`dict`.

    Attributes:
        filename (str): The filename of the configuration file.
        mqtt (:class:`.MQTTConfig`): The MQTT options of the Snips
            configuration.

    Example:
        >>> snips = SnipsConfig()
        >>> snips['snips-hotword']['audio']
        ['default@mqtt', 'bedroom@mqtt']
    """

    def __init__(self, filename=None):
        """Initialize a :class:`.SnipsConfig` object.

        The :attr:`mqtt` attribute is initialized with the MQTT connection
        settings from the configuration file, or the default value
        'localhost:1883' for the broker address if the settings are not
        specified.

        Args:
            filename (str, optional): The full path of the config file. If
                the argument is not specified, the file snips.toml is searched
                for in the following locations, in this order:

                - /etc/snips.toml
                - /usr/local/etc/snips.toml

        Raises:
            :exc:`FileNotFoundError`: If :attr:`filename` is specified but
                doesn't exist.

            :exc:`.SnipsConfigNotFoundError`: If there's no snips.toml found
                in the search path.

            :exc:`TomlDecodeError`: If :attr:`filename` doesn't have a valid
                TOML syntax.

        Examples:
            >>> snips = SnipsConfig()  # Tries to find snips.toml.
            >>> snips_local = SnipsConfig('/usr/local/etc/snips.toml')
        """
        if filename:
            if not Path(filename).is_file():
                raise FileNotFoundError('{} not found'.format(filename))
            self.filename = filename
        else:
            self.filename = find_path(SEARCH_PATH_SNIPS)
            if not self.filename:
                raise SnipsConfigNotFoundError()

        # Create a dict with our configuration.
        # This raises TomlDecodeError if the file doesn't have a valid TOML
        # syntax.
        UserDict.__init__(self, toml.load(self.filename))

        # Now find all the MQTT options in the configuration file and use
        # sensible defaults for options that aren't specified.
        try:
            # Basic MQTT connection settings.
            broker_address = self['snips-common'].get('mqtt', DEFAULT_BROKER)

            # MQTT authentication
            username = self['snips-common'].get('mqtt_username', None)
            password = self['snips-common'].get('mqtt_password', None)

            # MQTT TLS configuration
            tls_hostname = self['snips-common'].get('mqtt_tls_hostname', None)
            tls_ca_file = self['snips-common'].get('mqtt_tls_cafile', None)
            tls_ca_path = self['snips-common'].get('mqtt_tls_capath', None)
            tls_client_key = self['snips-common'].get('mqtt_tls_client_key',
                                                      None)
            tls_client_cert = self['snips-common'].get('mqtt_tls_client_cert',
                                                       None)
            tls_disable_root_store = self['snips-common'].get('mqtt_tls_disable_root_store',
                                                              False)

            # Store the MQTT connection settings in an MQTTConfig object.
            self.mqtt = MQTTConfig(broker_address,
                                   MQTTAuthConfig(username, password),
                                   MQTTTLSConfig(tls_hostname, tls_ca_file,
                                                 tls_ca_path, tls_client_key,
                                                 tls_client_cert,
                                                 tls_disable_root_store))
        except KeyError:
            # The 'snips-common' section isn't in the configuration file, so we
            # use a sensible default: 'localhost:1883'.
            self.mqtt = MQTTConfig()
