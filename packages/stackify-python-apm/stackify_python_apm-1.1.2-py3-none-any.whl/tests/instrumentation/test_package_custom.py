import json
import os
from unittest import TestCase

from stackifyapm.base import Client
from stackifyapm.traces import get_transaction
from stackifyapm.instrumentation import register
from stackifyapm.instrumentation import control

from tests.instrumentation.fixtures.module_test import CustomClassOne
from tests.instrumentation.fixtures.module_test import CustomClassTwo
from tests.instrumentation.fixtures.module_test import CustomClassThree
from tests.instrumentation.fixtures.module_test import CustomClassFour
from tests.instrumentation.fixtures.module_test import CustomClassFive


STACKIFY_JSON_FILE = 'stackify.json'

CONFIG = {
    "SERVICE_NAME": "service_name",
    "ENVIRONMENT": "production",
    "HOSTNAME": "sample_host",
    "FRAMEWORK_NAME": "framework",
    "FRAMEWORK_VERSION": "1.0",
    "APPLICATION_NAME": "sample_application",
    "BASE_DIR": "path/to/application/",
    "CONFIG_FILE": STACKIFY_JSON_FILE,
}

INSTRUMENTATION = {
    "instrumentation": [{
        "class": "CustomClassOne",
        "method": "custom_method_one",
        "module": "tests.instrumentation.fixtures.module_test"
    }, {
        "class": "CustomClassTwo",
        "method": "custom_method_two",
        "module": "tests.instrumentation.fixtures.module_test",
        "trackedFunction": False
    }, {
        "class": "CustomClassThree",
        "method": "custom_method_three",
        "module": "tests.instrumentation.fixtures.module_test",
        "trackedFunction": True
    }, {
        "class": "CustomClassFour",
        "method": "custom_method_four",
        "module": "tests.instrumentation.fixtures.module_test",
        "trackedFunction": True,
        "trackedFunctionName": "{ClassName}#{MethodName}"
    }, {
        "class": "CustomClassFive",
        "method": "custom_method_five",
        "module": "tests.instrumentation.fixtures.module_test",
        "trackedFunction": True,
        "trackedFunctionName": "Tracked Function {ClassName}#{MethodName}",
        "extra": {
            "custom_key": "custom value"
        }
    }]
}


class CustomInstrumentationTest(TestCase):
    def setUp(self):
        with open(STACKIFY_JSON_FILE, 'w') as json_file:
            json.dump(INSTRUMENTATION, json_file)

        self.client = Client(CONFIG)
        register._cls_registers = {
            "stackifyapm.instrumentation.packages.custom.CustomInstrumentation",
        }
        control.instrument(config_file=self.client.get_application_info().get('config_file'))
        self.client.begin_transaction("transaction_test")

    def tearDown(self):
        control.uninstrument(config_file=self.client.get_application_info().get('config_file'))
        os.remove(STACKIFY_JSON_FILE)

    def test_basic_custom_instrumentation(self):
        CustomClassOne().custom_method_one()

        self.assert_span(call='custom.CustomClassOne.custom_method_one')

    def test_custom_instrumentation_with_tracked_function_false(self):
        CustomClassTwo().custom_method_two()

        self.assert_span(call='custom.CustomClassTwo.custom_method_two')

    def test_custom_instrumentation_with_tracked_function_true(self):
        CustomClassThree().custom_method_three()

        self.assert_span(
            call='custom.CustomClassThree.custom_method_three',
            tracked_func='CustomClassThree.custom_method_three',
        )

    def test_custom_instrumentation_with_tracked_function_and_name(self):
        CustomClassFour().custom_method_four()

        self.assert_span(
            call='custom.CustomClassFour.custom_method_four',
            tracked_func='CustomClassFour#custom_method_four',
        )

    def test_custom_instrumentation_with_tracked_function_and_name_and_extra(self):
        CustomClassFive().custom_method_five()

        self.assert_span(
            call='custom.CustomClassFive.custom_method_five',
            tracked_func='Tracked Function CustomClassFive#custom_method_five',
            extra=True
        )

    def assert_span(self, call=None, tracked_func=None, extra=None):
        transaction = get_transaction()
        assert transaction
        assert transaction.get_spans()

        span = transaction.get_spans()[0]
        span_data = span.to_dict()

        assert span_data['reqBegin']
        assert span_data['reqEnd']
        assert span_data['transaction_id']
        assert span_data['call'] == call
        assert span_data['props']
        assert span_data['props']['CATEGORY'] == 'Python'
        if tracked_func:
            assert span_data['props']['TRACKED_FUNC'] == tracked_func

        if extra:
            assert span_data['props']['CUSTOM_KEY'] == "custom value"
