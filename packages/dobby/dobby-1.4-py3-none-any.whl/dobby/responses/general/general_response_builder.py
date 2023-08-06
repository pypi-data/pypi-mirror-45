import json

from dobby.responses.general.runtime_exception import RuntimeException


class GeneralResponseBuilder:
    """A base class for all result builders"""

    def __init__(self):
        # TODO: do we need any kind of extra steps here?
        pass

    def create_response(self, result):
        result_as_json = json.dumps(result.__dict__)
        print(result_as_json)
        if result.failed:
            print('Received a failed result! Throwing an exception!')
            print(result.message)
            raise RuntimeException(result_as_json)
        return True

