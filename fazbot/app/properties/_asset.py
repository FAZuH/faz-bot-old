from pathlib import Path


class Asset:

    def __init__(self, asset_directory: str) -> None:
        self._dir = Path(asset_directory)
        self._files: dict[Path, bytes] = {}

    def read_all(self) -> None:
        """Reads all files in asset directory."""
        file_paths = list(self._dir.glob("**/*"))
        for fp in file_paths:
            with open(fp, "rb") as opened_file:
                self._files[fp] = opened_file.read()

    def write_all(self) -> None:
        """Write all in-memory file data to their respective file paths on disk.

        Raises:
            IOError: If an error occurs while writing to any of the files.

        """
        for fp, data in self._files.items():
            with open(fp, "wb") as opened_file:
                opened_file.write(data)

    def write(self, key: str) -> None:
        """Write the in-memory data associated with the specified key to its respective file path on disk.

        Args:
            key (str): The file name to write.

        Raises:
            KeyError: If the key does not exist in assets dictionary.
            IOError: If an error occurs while writing to the file.

        """
        fp = self._get_fp_by_key(key)
        with open(fp, "wb") as opened_file:
            opened_file.write(self.files[fp])

    def get(self, key: str) -> bytes:
        """Retrieve the in-memory data associated with the specified key.

        Args:
            key (str): The key associated with the file data to retrieve.

        Returns:
            bytes: The binary data associated with the specified key.

        Raises:
            KeyError: If the key does not exist in the `files` dictionary.
        """
        fp = self._get_fp_by_key(key)
        return self.files[fp]

    def set(self, key: str, data: bytes) -> None:
        """Store the given binary data in memory associated with the specified key.

        Args:
            key (str): The key associated with the file data to store.
            data (bytes): The binary data to store in memory.
        """
        fp = self._get_fp_by_key(key)
        self.files[fp] = data

    def _get_fp_by_key(self, key: str) -> Path:
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
                raise KeyError(f"Asset with key {key} not found")

    @property
    def files(self) -> dict[Path, bytes]:
        """Get the dictionary storing in-memory file data.

        Returns:
            dict[Path, bytes]: The dictionary containing file paths as keys and their associated binary data as values.
        """
        return self._files
