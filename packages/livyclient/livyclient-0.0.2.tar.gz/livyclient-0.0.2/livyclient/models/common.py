import re


class Version:
    def __init__(self, version: str) -> None:
        match = re.match(r'(\d+)\.(\d+)\.(\d+)(\S*)$', version)
        if match is None:
            raise ValueError(f'Invalid version string {version!r}')
        self.major, self.minor, self.dot, self.extension = match.groups()

    def __eq__(self, other):
        return (
                isinstance(other, Version) and
                self.major == other.major and
                self.minor == other.minor and
                self.dot == other.dot
        )

    def __lt__(self, other):
        if self.major < other.major:
            return True
        elif self.major == other.major:
            if self.minor < other.minor:
                return True
            elif self.minor == other.minor:
                return self.dot < other.dot
            else:
                return False
        else:
            return False
