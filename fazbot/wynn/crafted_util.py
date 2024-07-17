from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from fazbot.wynn import IngredientField


class CraftedUtil:

    def __init__(self, ingredients: list[IngredientField]):
        self._ingredients = ingredients

        self._ing_prob_dists = []
        self._crafted_roll_min = np.int32(0)
        self._crafted_roll_max = np.int32(0)
        self._craft_probs = {}

        self._calculate_ingredient_probabilities()
        self._calculate_crafted_probabilities()

    @property
    def crafted_roll_min(self) -> np.int32:
        assert isinstance(self._crafted_roll_min, np.number)
        return self._crafted_roll_min

    @property
    def crafted_roll_max(self) -> np.int32:
        assert isinstance(self._crafted_roll_max, np.number)
        return self._crafted_roll_max

    @property
    def craft_probs(self) -> dict[int, Decimal]:
        assert isinstance(self._craft_probs, dict)
        return self._craft_probs

    @property
    def ingredients(self) -> list[IngredientField]:
        return self._ingredients


    def _calculate_ingredient_probabilities(self):
        """ Gets ingredient_rolls_list and ingredient_probDist_list from command arguments """
        for ing in self._ingredients:
            ing_stat_eff = (ing.boost + 100) * 0.01

            # Calculate ingredient probability distribution
            ing_base_values = np.linspace(ing.min_value, ing.max_value, 101)
            ing_rolls_boosted = \
                np.floor(np.round(ing_base_values) * ing_stat_eff).astype(int) - \
                np.floor(ing.min_value * ing_stat_eff).astype(int)
            ingredient_rolls_occurrences = np.bincount(ing_rolls_boosted)
            ingredient_prob_dist = ingredient_rolls_occurrences / 101

            # Assign values into class attributes
            self._ing_prob_dists.append(ingredient_prob_dist)
            self._crafted_roll_min += np.floor(ing.min_value * ing_stat_eff)
            self._crafted_roll_max += np.floor(ing.max_value * ing_stat_eff)

    def _calculate_crafted_probabilities(self):
        # Calculate crafted roll probabilities
        convolution = [1]
        for prob_dist in self._ing_prob_dists:
            convolution = np.convolve(convolution, prob_dist)

        # Build ingredients_probabilities dictionary
        crafted_rolls = np.linspace(self.crafted_roll_min, self.crafted_roll_max, len(convolution))
        for roll, crafted_roll_chance in zip(crafted_rolls, convolution):
            if crafted_roll_chance == 0:
                continue
            self.craft_probs[int(roll)] = Decimal(crafted_roll_chance)

