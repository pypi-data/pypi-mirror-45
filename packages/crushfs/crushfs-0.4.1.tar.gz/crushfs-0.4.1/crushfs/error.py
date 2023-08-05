class CrushFsFileNotFoundError(Exception):
    pass


class CrushFsDownloadObjectError(Exception):
    def __init__(self, response):
        self.message = f'{response.status_code}: {response.data.decode()}'

    def __str__(self):
        return f'{type(self)}: {self.message}'


class CrushFsUploadObjectError(Exception):
    def __init__(self, response):
        self.message = f'{response.status_code}: {response.data.decode()}'

    def __str__(self):
        return f'{type(self)}: {self.message}'


class CrushFsCombineObjectsError(Exception):
    def __init__(self, response):
        self.message = f'{response.status_code}: {response.data.decode()}'

    def __str__(self):
        return f'{type(self)}: {self.message}'

