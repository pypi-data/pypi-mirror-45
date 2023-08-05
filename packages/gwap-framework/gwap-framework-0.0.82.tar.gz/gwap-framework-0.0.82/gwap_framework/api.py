from flask_restful import Api


class GwapApi(Api):

    def handle_error(self, e):
        for val in self.app.error_handler_spec.values():
            for handler in val.values():
                registered_error_handlers = list(filter(lambda x: isinstance(e, x), handler.keys()))
                if len(registered_error_handlers) > 0:
                    raise e

        return super().handle_error(e)
