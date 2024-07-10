class WynnIngredientValue:

    def __init__(self, min_value: int, max_value: int, boost: int = 0) -> None:
        """ Constructor of `IngredientValue`

        Args:
            min_value (int): Ingredient minimum value
            max_value (int): Ingredient maximum value
            boost (int, optional): Ingredient boost value. Defaults to 0.
        """
        self._boost = boost
        self._min_value = min_value
        self._max_value = max_value
        self._check_params()

    @property
    def min_value(self) -> int:
        """ Ingredient minimum value """
        return self._min_value

    @property
    def max_value(self) -> int:
        """ Ingredient maximum value """
        return self._max_value

    @property
    def boost(self) -> int:
        """ Ingredient boost value """
        return self._boost

    def _check_params(self) -> None:
        """ Check if the parameters are valid

        Args:
            min_value (int): Ingredient minimum value
            max_value (int): Ingredient maximum value
            boost (int): Ingredient boost value

        Raises:
            ValueError: If minimum value is greater than maximum value or boost is negative
        """
        if self._min_value > self._max_value or self._boost < 0:
            raise ValueError("Minimum value cannot be greater than maximum value")
