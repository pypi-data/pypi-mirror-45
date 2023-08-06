from cement import Controller
from cement.utils.version import get_version_banner
from ..core.version import get_version

VERSION_BANNER = """
Add Dependencies and Extensions for Hashicorp Packer %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'
        description = 'Add Dependencies and Extensions for Hashicorp Packer'
        arguments = [
            (['-v', '--version'],
             {'action': 'version',
              'version': VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()
