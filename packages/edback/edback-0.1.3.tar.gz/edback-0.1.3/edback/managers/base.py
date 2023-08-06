import os


class Manager:
    def __init__(self, _base_path=None):
        if _base_path is None:
            _base_path = os.path.join(os.getenv('HOME'), '.edback')

        self._base_path = _base_path
        self._exists_or_create()

        self._initialize_variables()
        self._load()

    def __del__(self):
        self._save()

    def _exists_or_create(self):
        if not os.path.exists(self.base_path):
            os.mkdir(self._base_path, 0o700)

    def _initialize_variables(self):
        pass

    @property
    def base_path(self):
        return self._base_path

    def _save(self):
        raise NotImplementedError()

    def _load(self):
        raise NotImplementedError()
