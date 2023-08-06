"""Support for dealing with ARP information."""
from cement import Controller, ex

from penin.core.arp import create_arp_ping


class Arp(Controller):
    """Representation of all ARP-related commands."""

    class Meta:
        """Metadata for the ARP commands."""

        label = "arp"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(help="execute an ARP ping",
        arguments=[
            (
                ["destination"],
                {
                    "help": "destination for the request",
                },
            )
        ],
    )
    def ping(self):
        """Execute an ARP ping."""
        result = create_arp_ping(self.app.pargs.destination)
        print(result)
        data = {"result": result}
        self.app.render(data, "default.jinja2")
