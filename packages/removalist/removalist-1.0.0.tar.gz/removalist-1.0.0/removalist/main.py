
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import RemovalistError
from .controllers.base import Base
from .controllers.dependencies import Dependencies
from .controllers.template import Template

CONFIG = init_defaults('removalist')
CONFIG['removalist']['dependencies_path'] = '.dependencies'
CONFIG['removalist']['template_extension'] = 'rcl'


class Removalist(App):
    """Removalist for Hashicorp Packer primary application."""

    class Meta:
        label = 'removalist'
        config_defaults = CONFIG
        close_on_exit = True
        config_handler = 'yaml'
        config_file_suffix = '.yml'
        log_handler = 'colorlog'
        output_handler = 'jinja2'
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]
        handlers = [
            Base,
            Dependencies,
            Template
        ]


class RemovalistTest(TestApp, Removalist):
    """A sub-class of Removalist that is better suited for testing."""

    class Meta:
        label = 'removalist'


def main():
    with Removalist() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except RemovalistError as e:
            print('RemovalistError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
