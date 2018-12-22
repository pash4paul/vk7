from vk7.utils import make_execute_method, make_execute_code, get_logger
from vk7.vk_api import VkApi

logger = get_logger(__name__)


class Vk(VkApi):
    def __init__(self, *args, verbose: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self._methods = {attr: getattr(self, attr) for attr in dir(self) if callable(getattr(self, attr))}
        self._verbose = verbose

    def _items_iterator(self, method, **kwargs):
        max_api_calls = 25

        total = 100
        offset = 0
        count = 100

        prev_offset = 0

        while offset < total:
            methods = []
            for _ in range(max_api_calls):
                methods.append(make_execute_method(method, **kwargs, count=count, offset=offset))
                offset += count

            code = make_execute_code(methods)

            if self._verbose:
                logger.info('{} get items from {} to {}'.format(method, prev_offset, offset))
                prev_offset = offset

            for response in self.execute(code=code)['response']:
                total = response['count']
                for item in response['items']:
                    yield item

    def groups_getMembers(self, group_id: int, fields: str):
        return self._items_iterator('groups.getMembers', group_id=group_id, fields=fields)

    def wall_get(self, owner_id: int):
        return self._items_iterator('wall.get', owner_id=owner_id)
