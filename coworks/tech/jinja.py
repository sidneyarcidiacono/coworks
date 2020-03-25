import jinja2
import fs
import fs.errors
import urllib.parse
import cgi

from coworks import TechMicroService
from chalice import Response
from requests_toolbelt.multipart import decoder


class S3FSLoader(jinja2.BaseLoader):
    """ The following code comes from https://github.com/althonos/jinja2-fsloader.git
    I use the library fs-s3fs instead of fs in order to make it work with s3 buckets.

    Per default the template encoding is ``'utf-8'`` which can be changed by setting the `encoding` parameter to
    something else. The `use_syspath` parameter can be opted in to provide Jinja2 the system path to the query
    if it exist, otherwise it will only return the internal filesystem path. The optional `fs_filter` parameter is
    a list of wildcard patterns like ``['*.html', '*.tpl']``. If present, only the matching files in the
    filesystem will be loaded as templates. """

    def __init__(self, template_fs, encoding='utf-8', use_syspath=False, fs_filter=None):
        self.filesystem = fs.open_fs(template_fs)
        self.use_syspath = use_syspath
        self.encoding = encoding
        self.fs_filter = fs_filter

    def get_source(self, environment, template):
        if not self.filesystem.isfile(template):
            raise jinja2.TemplateNotFound(template)
        try:
            mtime = self.filesystem.getdetails(template).modified
            def reload():
                return self.filesystem.getdetails(template).modified > mtime
        except fs.errors.MissingInfoNamespace:
            def reload():
                return True
        with self.filesystem.open(template, encoding=self.encoding) as input_file:
            source = input_file.read()
        if self.use_syspath:
            if self.filesystem.hassyspath(template):
                return source, self.filesystem.getsyspath(template), reload
            elif self.filesystem.hasurl(template):
                return source, self.filesystem.geturl(template), reload
        return source, template, reload

    def list_templates(self):
        found = set()
        for file in self.filesystem.walk.files(filter=self.fs_filter):
            found.add(fs.path.relpath(file))
        return sorted(found)


class JinjaRenderMicroservice(TechMicroService):
    """ Render a jinja template to html
        Templates can be sent to the microservice in 3 differents ways :
            - send files in multipart/form-data body
            - put template content in url
            - put templates in a s3 bucket and give bucket name to the microservice """

    def post_render(self, template_name):
        """ render one template from templates given in multipart/form-data body
            pass jinja context in query_params """
        content_type = self.current_request.headers.get('content-type')
        multipart_decoder = decoder.MultipartDecoder(self.current_request.raw_body, content_type)
        templates = {}
        for part in multipart_decoder.parts:
            headers = {k.decode('utf-8'): v.decode('utf-8') for k, v in part.headers.items()}
            content = part.content.decode('utf-8')
            _, content_disposition_params = cgi.parse_header(headers['Content-Disposition'])
            filename = content_disposition_params['filename']
            templates[filename] = content
        context = self.current_request.query_params
        env = jinja2.Environment(loader=jinja2.DictLoader(templates))
        template = env.get_template(template_name)
        render = template.render(**context)
        response = Response(body=render,
                            status_code=200,
                            headers={'Content-Type': 'text/html'})
        return response

    def get_render_(self, template):
        """ render template which content is given in url
        pass jinja context in query_params """
        template = urllib.parse.unquote_plus(template)
        context = self.current_request.query_params
        env = jinja2.Environment(loader=jinja2.DictLoader({'index.html': template}))
        template = env.get_template('index.html')
        render = template.render(**context)
        response = Response(body=render,
                            status_code=200,
                            headers={'Content-Type': 'text/html'})
        return response

    def get_render__(self, bucket, template_name):
        """ render template stored on s3
        pass jinja context in query_params """
        bucket = urllib.parse.unquote_plus(bucket)
        template_name = urllib.parse.unquote_plus(template_name)
        context = self.current_request.query_params
        env = jinja2.Environment(loader=S3FSLoader(bucket))
        template = env.get_template(template_name)
        render = template.render(**context)
        response = Response(body=render,
                            status_code=200,
                            headers={'Content-Type': 'text/html'})
        return response
