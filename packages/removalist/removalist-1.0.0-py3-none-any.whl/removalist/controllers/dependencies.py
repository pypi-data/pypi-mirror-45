from sys import exit
from os import getcwd
from cement import Controller, ex
from .helpers.loader import yaml as loader_yaml
from .helpers.data import repository as data_repository
from .helpers.data import name as data_name
from .helpers.data import version as data_version
from .helpers.git import clone as git_clone
from .helpers.git import checkout as git_checkout


class Dependencies(Controller):
    class Meta:
        label = 'dependencies'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(
        help='install dependencies',
        arguments=[
            (['-f', '--file'],
             {'help': 'custom requirements file',
              'action': 'store',
              'dest': 'file',
              'default': 'requirements'}),
        ]
    )
    def install(self):
        requirements = loader_yaml(self.app.pargs.file)

        if requirements is None:
            self.app.log.error("cannot load {}.".format(self.app.pargs.file))
            exit(1)

        for requirement in requirements:
            repository = data_repository(requirement)
            name = data_name(requirement)
            version = data_version(requirement)

            if repository is None:
                self.app.log.warning("missing repository key, skipping")
                continue

            if name is None:
                self.app.log.warning("missing name key, skipping")
                continue

            path = "{}/{}".format(getcwd(), self.app.config.get(
                'removalist',
                'dependencies_path')
            )
            self.app.log.info("installing {}@{}".format(
                name,
                version or "master")
            )
            git_clone(path, name, repository)

            if version is not None:
                git_checkout(path, name, version)
