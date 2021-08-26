import traceback

from aws_xray_sdk import global_sdk_config
from aws_xray_sdk.core import AWSXRayRecorder
from aws_xray_sdk.core.models.dummy_entities import DummySegment, DummySubsegment
from aws_xray_sdk.core.models.subsegment import Subsegment
from contextlib import contextmanager
from functools import partial, update_wrapper

LAMBDA_NAMESPACE = 'lambda'
COWORKS_NAMESPACE = 'coworks'


class XRayContextManager:
    NAME = 'xray'

    def __init__(self, app, recorder, name=NAME):
        super().__init__(app, name)
        self.recorder = recorder
        app.log.debug(f"initializing xray context manager at {name}")

        @app.before_first_activation
        def capture_routes(event, context):
            try:
                for path, route in app.routes.items():
                    for method, entry in route.items():
                        view_function = entry.view_function
                        cws_function = view_function.__cws_func__

                        def captured(_view_function, *args, **kwargs):
                            subsegment = recorder.current_subsegment()
                            if subsegment:
                                # TODO event and global should be taken from global
                                subsegment.put_metadata('event', event, LAMBDA_NAMESPACE)
                                subsegment.put_metadata('context', context, LAMBDA_NAMESPACE)
                                subsegment.put_annotation('service', app.name)
                                subsegment.put_metadata('query_params', app.current_request.query_params,
                                                        COWORKS_NAMESPACE)
                                if app.current_request.raw_body:
                                    subsegment.put_metadata('json_body', app.current_request.json_body,
                                                            COWORKS_NAMESPACE)
                            response = _view_function(*args, **kwargs)
                            if subsegment:
                                subsegment.put_metadata('response', response, COWORKS_NAMESPACE)
                            return response

                        def captured_entry(_cws_function, *args, **kwargs):
                            subsegment = recorder.current_subsegment()
                            if subsegment:
                                subsegment.put_metadata('args', args, COWORKS_NAMESPACE)
                                subsegment.put_metadata('kwargs', kwargs, COWORKS_NAMESPACE)
                            response = _cws_function(*args, **kwargs)
                            if subsegment:
                                subsegment.put_metadata('response', response, COWORKS_NAMESPACE)
                            return response

                        wrapped_fun = update_wrapper(partial(captured, view_function), view_function)
                        entry.view_function = recorder.capture(view_function.__name__)(wrapped_fun)

                        wrapped_fun = update_wrapper(partial(captured_entry, cws_function), cws_function)
                        entry.view_function.__cws_func__ = recorder.capture(cws_function.__name__)(wrapped_fun)
            except Exception:
                app.log.error("Cannot set xray context manager : are you using xray_recorder?")
                raise

        @app.handle_exception
        def capture_exception(event, context, e):
            try:
                app.log.error(f"Event: {event}")
                app.log.error(f"Context: {context}")
                app.log.error(f"Exception: {str(e)}")
                app.log.error(traceback.print_exc())
                subsegment = recorder.current_subsegment
                if subsegment:
                    subsegment.put_annotation('service', app.name)
                    subsegment.add_exception(e, traceback.extract_stack())
            finally:
                return {
                    'headers': {},
                    'multiValueHeaders': {},
                    'statusCode': 500,
                    'body': "Exception in microservice, see logs in XRay for more details",
                    'error': str(e)
                }

    @staticmethod
    def capture(recorder):
        """Decorator to trace function calls on XRay."""

        if not issubclass(recorder.__class__, AWSXRayRecorder):
            raise TypeError(f"recorder is not an AWSXRayRecorder {type(recorder)}")

        def decorator(function):
            def captured(*args, **kwargs):
                subsegment = recorder.current_subsegment()
                if subsegment:
                    subsegment.put_metadata(f'{function.__name__}.args', args, COWORKS_NAMESPACE)
                    subsegment.put_metadata(f'{function.__name__}.kwargs', kwargs, COWORKS_NAMESPACE)
                response = function(*args, **kwargs)
                if subsegment:
                    subsegment.put_metadata(f'{function.__name__}.response', response, COWORKS_NAMESPACE)
                return response

            wrapped_fun = update_wrapper(captured, function)
            return recorder.capture(function.__name__)(wrapped_fun)

        return decorator

    @contextmanager
    def __call__(self) -> Subsegment:
        """Traces any dictionnary defined by the keyword arguments."""
        subsegment = self.recorder.current_subsegment()
        if subsegment:
            subsegment = DummySubsegment(DummySegment(global_sdk_config.DISABLED_ENTITY_NAME))

        yield subsegment
