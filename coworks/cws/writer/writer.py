import inspect
import pathlib
from abc import ABC, abstractmethod
import sys

from jinja2 import Environment, PackageLoader, select_autoescape, TemplateNotFound


class WriterError(Exception):
    ...


class Writer(ABC):

    def __init__(self, app=None, name=None):
        self.output = sys.stdout
        self.error = sys.stderr
        self.name = name

        #: A list of functions that will be called before or after the export command.
        self.before_funcs = []
        self.after_funcs = []

        if app is not None:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        if 'writers' not in app.extensions:
            app.extensions['writers'] = {}
        app.extensions['writers'][self.name] = self

    def export(self, output=None, error=None, variables=None, **kwargs):
        """ Called when the export command of the Coworks CLI is called.
        :param output: output stream.
        :param error: error stream.
        :param variables: user defined variables.
        :param kwargs: environment parameters for export.
        :return: None
        """
        if output is not None:
            self.output = open(output, 'w+') if type(output) is str else output
        if error is not None:
            self.error = open(error, 'w+') if type(error) is str else error

        variables = variables or {}
        variables.setdefault('workspace', 'dev')

        for func in self.before_funcs:
            func(variables=variables, **kwargs)

        self._export_header(variables=variables, **kwargs)
        self._export_content(variables=variables, **kwargs)

        for func in self.after_funcs:
            func(variables=variables, **kwargs)

    def before_export(self, f):
        """Registers a function to be run before the export command.
        :param f: function called before the export commaand
        :return: None

        May be used as a decorator.

        The function will be called without any arguments and its return value is ignored.
        """

        self.after_funcs.append(f)
        return f

    def after_export(self, f):
        """Registers a function to be run after the export command.
        :param f: function called after the export commaand
        :return: None

        May be used as a decorator.

        The function will be called without any arguments and its return value is ignored.
        """

        self.after_funcs.append(f)
        return f

    def _export_header(self, **kwargs):
        ...

    @abstractmethod
    def _export_content(self, **kwargs):
        """ Main export function.
        :param kwargs: Environment parameters for export.
        :return: None.

        Abstract method which must be redefined in any subclass. The content should be written in self.output.
        """

    def _format(self, content):
        return content


class TemplateWriter(Writer):

    def __init__(self, app=None, name=None, data=None, template_filenames=None, env=None):
        super().__init__(app, name)
        self.data = data or {}
        self.template_filenames = template_filenames or self.default_template_filenames
        self.env = env or Environment(
            loader=PackageLoader("coworks.cws.writer"),
            autoescape=select_autoescape(['html', 'xml'])
        )

    @property
    @abstractmethod
    def default_template_filenames(self):
        ...

    def _export_content(self, module_name='app', handler_name='app', project_dir='.', variables=None, **kwargs):
        module_path = module_name.split('.')
        data = {
            'writer': self,
            'project_dir': project_dir,
            'module': module_name,
            'module_path': pathlib.PurePath(*module_path),
            'module_dir': pathlib.PurePath(*module_path[:-1]),
            'module_file': module_path[-1],
            'handler': handler_name,
            'app': self.app,
            'ms_name': self.app.ms_name,
            'app_configs': self.app.configs,
            'variables': variables,
        }
        data.update(self.data)
        try:
            for template_filename in self.template_filenames:
                template = self.env.get_template(template_filename)
                print(self._format(template.render(**data)), file=self.output)
        except TemplateNotFound as e:
            raise WriterError(f"Cannot find template {str(e)}")
        except Exception as e:
            raise WriterError(e)


class ListWriter(TemplateWriter):

    def __init__(self, app=None, name='list', **kwargs):
        super().__init__(app, name, **kwargs)

    @property
    def default_template_filenames(self):
        return ['list.j2']

    def _export_header(self, **kwargs):
        pass


class OpenApiWriter(TemplateWriter):
    """Export the microservice in swagger format."""

    def __init__(self, app=None, name='openapi', **kwargs):
        super().__init__(app, name, **kwargs)

    @property
    def default_template_filenames(self):
        return ['openapi.yml']

    def _export_header(self, **kwargs):
        print("# Do NOT edit this file as it is auto-generated by cws\n", file=self.output)

    @property
    def pathes(self):
        pathes = {}
        for route, entry in self.app.routes.items():
            entries = {}
            for method, infos in entry.items():
                func = self.app.entries[route]
                fullargspec = inspect.getfullargspec(func[1])
                args = fullargspec.args[1:]
                defaults = fullargspec.defaults or []
                len_defaults = len(defaults)
                entry = {
                    'description': func.__doc__,
                    'parameters': []
                }
                for index, arg in enumerate(args[1:-len_defaults]):
                    entry['parameters'].append({
                        'name': f"_{index}:{arg}",
                        'in': 'path',
                    })
                for arg in args[-len_defaults:]:
                    entry['parameters'].append({
                        'name': arg,
                        'in': 'query',
                    })
                for varkw in fullargspec.varkw or []:
                    entry['parameters'].append({
                        'name': varkw,
                        'in': 'query',
                    })
                entries[method.lower()] = entry
            pathes[route] = entries
        return pathes


def reduce_not_none(data):
    """Remove all entries where value is None."""
    return dict((k, v) for k, v in data.items() if v is not None)
