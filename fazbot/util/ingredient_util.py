from decimal import Decimal


class IngredientUtil:

    def __init__(self, base_probability: Decimal | float, loot_quality: int = 0, loot_bonus: int = 0):
        self._base_probability = Decimal(base_probability) if isinstance(base_probability, (float, int)) else base_probability
        self._loot_quality = loot_quality
        self._loot_bonus = loot_bonus
        self._loot_boost = loot_quality + loot_bonus
        self._boosted_probability = self._compute_boosted_probability(self._base_probability, self._loot_boost)

    @property
    def base_probability(self) -> Decimal:
        return self._base_probability

    @property
    def boosted_probability(self) -> Decimal:
        return self._boosted_probability

    @property
    def loot_quality(self) -> int:
        return self._loot_quality

    @property
    def loot_bonus(self) -> int:
        return self._loot_bonus

    @property
    def loot_boost(self) -> int:
        return self._loot_boost

    @staticmethod
    def _compute_boosted_probability(base_probability: Decimal, loot_boost: int) -> Decimal:
        return base_probability * Decimal((loot_boost + 100) / 100)
