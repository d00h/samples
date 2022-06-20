import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Tuple


@dataclass
class GooglePlayProfile:

    device_id: str
    package_name: str
    client_id: str
    client_secret: str

    @classmethod
    def from_dict(cls, country, data: dict):
        try:
            return cls(
                device_id=data['DEVICE_ID'],
                package_name=data['PACKAGE_NAME'],
                client_id=data['CLIENT_ID'],
                client_secret=data['CLIENT_SECRET'],
            )
        except KeyError as ex:
            print(data)
            raise KeyError(f'require GOOGLEPLAY_{country}_{ex.args[0]}')

    @classmethod
    def parse_env(cls, data: dict) -> Iterable[Tuple[str, 'GooglePlayProfile']]:
        regex = re.compile(r"^GOOGLEPLAY_([^_]+)_(.*)$", re.MULTILINE)
        parsed = defaultdict(dict)
        for key, value in data.items():
            match = regex.match(key)
            if match:
                country = match.group(1)
                varname = match.group(2)
                parsed[country][varname] = value

        for country, country_data in parsed.items():
            yield country, cls.from_dict(country, country_data)


TEST_ENV = {
    "TRASH": 1,
    "GOOGLEPLAY_SOME_DEVICE_ID": 1,
    "GOOGLEPLAY_SOME_PACKAGE_NAME": 2,
    "GOOGLEPLAY_SOME_CLIENT_ID": 3,
    "GOOGLEPLAY_SOME_CLIENT_SECRET": 4,

    "GOOGLEPLAY_OTHER_DEVICE_ID": 1,
    "GOOGLEPLAY_OTHER_PACKAGE_NAME": 2,
    "GOOGLEPLAY_OTHER_CLIENT_ID": 3,
    "GOOGLEPLAY_OTHER_CLIENT_SECRET": 4,
}


google_profiles = list(GooglePlayProfile.parse_env(TEST_ENV))

print(google_profiles)
