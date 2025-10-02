
from copy import deepcopy

biomes = ["Forest", "Underground", "Cavern", "Underworld", "Snow", "Desert", "Ocean", "Jungle", "Mushroom", "Corruption", "Crimson", "Hallow"]

def match_biomes(groups):
    """
    Assign the best biome to each group based on member preferences.
    - Start with base happiness 1.0 per group.
    - For each character:
        +0.2 if they like the biome
        -0.2 if they don't like the biome
    - Assign the biome that yields the highest score.
    """

    for group in groups:
        best_biomes = []
        best_score = -float("inf")

        for biome in biomes:
            temp_score = 1.0  # base happiness for the group
            for char in group.characters:
                if biome in char.liked_biome:
                    temp_score += 0.2
                else:
                    temp_score -= 0.2

            if temp_score > best_score:
                best_score = temp_score
                best_biomes = [biome]
            elif temp_score == best_score:
                best_biomes.append(biome)

        group.biome = best_biomes