from sys import exit
from cement import Controller, ex
from .helpers.loader import json as loader_json
from .helpers.data import root as data_root
from .helpers.data import dependencies as data_dependencies
from .helpers.data import merge as data_merge
from .helpers.serializer import json as serializer_json


class Template(Controller):
    class Meta:
        label = 'template'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(
        help='compile template',
        arguments=[
            ([],
             {'help': 'removalist template to compile',
              'action': 'store',
              'dest': 'template'}),
        ]
    )
    def compile(self):
        name = self.app.pargs.template
        data = {}

        while name is not None:
            try:
                self.app.log.info("merging {}.".format(name))
                template = loader_json(name)
                name = data_root(template)
                data = data_merge(data, template)
            except TypeError:
                self.app.log.error("cannot load {}.".format(name))
                exit(1)

        dependencies = data_dependencies(data)
        for dependency in dependencies:
            try:
                self.app.log.info("merging {}.".format(dependency))
                node = loader_json(dependency)
                data = data_merge(node, data)
            except TypeError:
                self.app.log.error("cannot load {}.".format(dependency))
                exit(1)

        serializer_json(data)
