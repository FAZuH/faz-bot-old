CRAFTCHANCE_ARGS = {
    "aliases": ["cc"],
    "brief": "Calculates crafted roll probabilities",
    "description": "Takes any number of ingredients as inputs. improved with help from afterfive",
    "help": (
        "**Ingredient input syntax:**\n"
        "- <min>,<max>,[efficiency]\n\n*"
        "*Input examples:**\n"
        "- 1,5 1,5,25\n"
        "- 1,2,50 1,2,50 1,2,50 1,2,50\n"
        "- 1,3 1,3"
    )
}
CONVERT_ARGS = {
    "aliases": ["cnv"],
    "brief": "Convert emeralds",
    "description": "Converts input emeralds into a common emerald format",
    "help": (
        "**Emeralds input syntax:**\n"
        "- Orderless (in integers or decimals)\n"
        "- Takes numbers that ends with \"x\" as amount (supports fractions)\n"
        "- Takes numbers that ends with \"stx\" as stacks\n"
        "- Takes numbers that ends with \"le\" as liquid emeralds\n"
        "- Takes numbers that ends with \"eb\" as emerald blocks\n"
        "- Takes numbers that ends with \"e\" as emeralds\n\n"
        "**Input examples:**\n"
        "- 2x 1stx 1le 1eb 1e\n"
        "- 2stx 100le 100eb\n"
        "- 1/3x 1000eb"
    )
}
INGCHANCE_ARGS = {
    "aliases": ["ic"],
    "brief": "Calculates ingredient drop chance",
    "help": (
        "**Arguments input syntax:**\n"
        "- Orderless (in integers or decimals)\n"
        "- Takes first word in the input as base ingredient drop chance (supports fraction and percentage)"
        "- Takes numbers that ends with \"lb\" as loot bonus\n"
        "- Takes numbers that ends with \"lq\" as loot quality\n\n"
        "**Input examples:**\n"
        "- 1/200 700lb\n"
        "- 0.0005% 600lb 100lq"
    )
}

