import unittest

from hydrosdk.sdk import Model, Signature, Application

DEV_ENDPOINT = "https://dev.k8s.hydrosphere.io"

class ModelSpec(unittest.TestCase):
    def test_model_creation(self):
        model = Model()\
            .with_name("sdk-model")\
            .with_runtime("hydrosphere/serving-runtime-python-3.6:dev")\
            .with_payload(['/Users/bulat/Documents/dev/hydrosphere/serving/example/models/claims_model/src'])
        print(model)
        model.compile()
        print(model.inner_model.__dict__)

    def test_model_apply(self):
        signature = Signature().with_name("claim")\
            .with_input("client_profile", "float64", [112], "numerical")\
            .with_output("amount", "int64", "scalar", "real")

        model = Model() \
            .with_name("sdk-model") \
            .with_runtime("hydrosphere/serving-runtime-python-3.6:dev") \
            .with_payload(['/Users/bulat/Documents/dev/hydrosphere/serving/example/models/claims_model/src'])\
            .with_signature(signature)

        result = model.apply(DEV_ENDPOINT)
        print(model.inner_model.__dict__)
        print(result)

    def test_singular_application_apply(self):
        signature = Signature().with_name("claim") \
            .with_input("client_profile", "float64", [112], "numerical") \
            .with_output("amount", "int64", "scalar", "real") \

        model = Model() \
            .with_name("sdk-model") \
            .with_runtime("hydrosphere/serving-runtime-python-3.6:dev") \
            .with_payload(['/Users/bulat/Documents/dev/hydrosphere/serving/example/models/claims_model/src']) \
            .with_signature(signature)

        app = Application.singular("sdk-app", model)
        result = app.apply(DEV_ENDPOINT)
        print(app.compiled)
        print(result)
