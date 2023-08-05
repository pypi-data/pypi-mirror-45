import json
import os
import logging

from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.utils.helper import is_async_span

logger = logging.getLogger(__name__)


class CustomInstrumentation(AbstractInstrumentedModule):
    """
    Custom instrumentation support
    to be able to let user do custom instrumentation without code changes,
    we provide this custom instrumenation module to instrument
    specific class method provider by the user in their config file
    """
    name = "custom_instrumentation"
    instrumentations = []
    instrument_list = []

    def get_instrument_list(self, config_file=None):
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file) as json_file:
                    data = json.load(json_file)
                    self.instrumentations = data.get('instrumentation', [])

                    for instrumentation in self.instrumentations:
                        class_name = instrumentation.get('class')
                        method_name = instrumentation.get('method')
                        method = class_name and "{}.{}".format(class_name, method_name) or method_name
                        self.instrument_list.append((instrumentation.get('module'), method))

            except Exception:
                logger.warning('Unable to read stackify json file.')

        return self.instrument_list

    def call(self, module, method, wrapped, instance, args, kwargs):
        extra_data = {
            "type": "Python",
        }
        class_name, method_name = method.split('.')
        span_type = 'custom.{}.{}'.format(class_name, method_name)

        instrumentations = [i for i in self.instrumentations if i.get('class') == class_name and i.get('method') == method_name]
        if instrumentations:
            instrumentation = instrumentations[0]
            if instrumentation.get('trackedFunction'):
                extra_data['tracked_func'] = instrumentation.get('trackedFunctionName', '{ClassName}.{MethodName}').format(
                    ClassName=class_name,
                    MethodName=method_name,
                )

            extra_data.update(instrumentation.get('extra', {}))

        with CaptureSpan('custom', span_type, extra_data, leaf=False, is_async=is_async_span()):
            return wrapped(*args, **kwargs)
