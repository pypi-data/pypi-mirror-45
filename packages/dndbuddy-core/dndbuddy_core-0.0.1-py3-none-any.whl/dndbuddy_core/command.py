
import abc


class Command(abc.ABC):
    """Abstract class to standardize commands"""

    @classmethod
    def __call__(cls, inp):
        """Returns whether given input ran this command"""
        match = cls.match(inp)
        if match:
            cls.run(inp)
        return match

    @abc.abstractstaticmethod
    def match(inp):
        """Returns whether given input matches this command"""
        pass

    @abc.abstractstaticmethod
    def run(inp):
        """Runs this command with the given input"""
        pass
