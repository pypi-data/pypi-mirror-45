

from typing import Any, List, Union
import configparser


class ConfigParser(configparser.RawConfigParser):
    """Our specialization of ConfigParser."""

    def __init__(self, our_file: Union[str, bool]):
        """Create the ConfigParser.

        `our_file` is True if this config file is specifically for coverage,
        False if we are examining another config file (tox.ini, setup.cfg)
        for possible settings.
        """

        configparser.RawConfigParser.__init__(self)
        self.section_prefixes = "" if our_file else ["testml:"]

    def read(self, filenames, **kwargs) -> List:
        """

        Parameters
        ----------
        filenames :
        kwargs :

        Returns
        -------

        """
        kwargs['encoding'] = "utf-8"
        return configparser.RawConfigParser.read(self, filenames, **kwargs)

    def has_option(self, section: str, option: str) -> bool:
        """

        Parameters
        ----------
        section : str
            The section of the config file
        option :

        Returns
        -------

        """
        real_section = self.section_prefixes + section
        has = configparser.RawConfigParser.has_option(self, real_section, option)
        if has:
            return has
        return False

    def has_section(self, section: str) -> Union[bool, str]:
        """

        Parameters
        ----------
        section : str
            The section of the config file

        Returns
        -------
        bool
            Section exists or not

        """
        real_section = self.section_prefixes + section
        has = configparser.RawConfigParser.has_section(self, real_section)
        if has:
            return real_section
        return False

    def options(self, section: str) -> dict:
        """

        Parameters
        ----------
        section : str
            The section of the config file

        Returns
        -------
        Configuration : dict
            The extracted configuration from our config file

        """

        real_section = self.section_prefixes + section
        if configparser.RawConfigParser.has_section(self, real_section):
            return configparser.RawConfigParser.options(self, real_section)
        raise configparser.NoSectionError

    def get(self, section: str, option: str, *args, **kwargs) -> Union[str, int, List]:
        """
        Get a value, replacing environment variables also.

        The arguments are the same as `RawConfigParser.get`, but in the found
        value, ``$WORD`` or ``${WORD}`` are replaced by the value of the
        environment variable ``WORD``.

        Returns the finished value.


        Parameters
        ----------
        section : str
            The section of the config file
        option : str
            The option of a specific section
        args :
        kwargs :

        Returns
        -------

        """
        real_section = self.section_prefixes + section
        if configparser.RawConfigParser.has_option(self, real_section, option):
            return configparser.RawConfigParser.get(self, real_section, option, *args, **kwargs)
        else:
            raise configparser.NoSectionError

    def getlist(self, section: str, option: str) -> List[str]:
        """
        Read a list of strings.

        The value of `section` and `option` is treated as a comma- and newline-
        separated list of strings.  Each value is stripped of whitespace.

        Returns the list of strings.


        Parameters
        ----------
        section : str
            The section of the config file
        option : str
            The option of a specific section

        Returns
        -------

        """

        value_list = self.get(section, option)
        values = []
        for value_line in value_list.split('\n'):
            for value in value_line.split(','):
                value = value.strip()
                if value:
                    values.append(value)
        return values

    def set(self, section: str, option: str, value: Union[str, List, int, None] = None) -> Any:
        """
        Set the value of a section's option

        Parameters
        ----------
        section : str
            The section of the config file
        option : str
            The option of a specific section
        value :  Union[str, List, int, None]
            The value to be set for a section, option pair

        Returns
        -------
        value

        """

        real_section = self.section_prefixes + section
        configparser.RawConfigParser.set(self, real_section, real_section, value)
        return value
