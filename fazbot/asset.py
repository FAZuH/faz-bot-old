from pathlib import Path


class Asset:
    """Class for reading, storing, and writing files stored in 'asset' directory."""

    def __init__(self, path: str | Path) -> None:
        self._dir = Path(path) if isinstance(path, str) else path
        self._files: dict[Path, bytes] = {}

    def read_all(self) -> None:
        """Reads all files in `path`, and stores it into `_files`"""
        file_paths = list(self._dir.glob("**/*"))
        for fp in file_paths:
            with open(fp, "rb") as opened_file:
                self._files[fp] = opened_file.read()

    def write_all(self) -> None:
        """Writes all data in `_files` to their respective file path"""
        for fp, data in self._files.items():
            with open(fp, "wb") as opened_file:
                opened_file.write(data)

    def write(self, key: str) -> None:
        """Writes a data in `_files` by `key` to their respective file path
        Args:
            key (str): The file name to write.
        """
        fp = self.get_fp_by_key(key)
        with open(fp, "wb") as opened_file:
            opened_file.write(self.files[fp])

    def get(self, key: str) -> bytes:
        fp = self.get_fp_by_key(key)
        return self.files[fp]

    def set(self, key: str, data: bytes) -> None:
        fp = self.get_fp_by_key(key)
        self.files[fp] = data

    def get_fp_by_key(self, key: str) -> Path:
        for fp in self._files:
            # Strict search
            if key == fp.stem:
                return fp
        else:
            # Less strict search
            for fp in self._files:
                if key in fp.name:
                    return fp
            else:
                raise KeyError("Asset with key {key} not found")

    @property
    def files(self) -> dict[Path, bytes]:
        return self._files

