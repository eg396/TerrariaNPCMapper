class Group:
    def __init__(self, biome, happiness, characters=None):
        self.biome = biome
        # Default to empty list if no characters passed
        self.happiness = 1 if happiness is None else happiness
        self.characters = characters if characters is not None else []

    def get_info(self):
        return [
            self.biome,
            self.happiness,
            [char.get_info() for char in self.characters]
        ]
    
    def __str__(self):
        lines = [f"Group - Happiness: {self.happiness:.2f}"]
        lines.append("Characters:")
        for char in self.characters:
            lines.append(f"- {char.name}")
        lines.append(f"Biome: {self.biome if self.biome else 'None'}")
        return "\n".join(lines)