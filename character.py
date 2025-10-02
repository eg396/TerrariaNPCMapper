class Character:
    def __init__(self, name, liked_biome=None, disliked_biome=None, 
                 loved_npc=None, liked_npc=None, disliked_npc=None, hated_npc=None):
        self.name = name
        self.liked_biome = liked_biome
        self.disliked_biome = disliked_biome
        self.loved_npc = loved_npc
        self.liked_npc = liked_npc
        self.disliked_npc = disliked_npc
        self.hated_npc = hated_npc

    def get_info(self):
        return [
            self.name,
            self.liked_biome,
            self.disliked_biome,
            self.loved_npc,
            self.liked_npc,
            self.disliked_npc,
            self.hated_npc
        ]
    
    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Liked Biome: {', '.join(self.liked_biome) if self.liked_biome else 'None'}\n"
            f"Disliked Biome: {', '.join(self.disliked_biome) if self.disliked_biome else 'None'}\n"
            f"Loved NPC(s): {', '.join(self.loved_npc) if self.loved_npc else 'None'}\n"
            f"Liked NPC(s): {', '.join(self.liked_npc) if self.liked_npc else 'None'}\n"
            f"Disliked NPC(s): {', '.join(self.disliked_npc) if self.disliked_npc else 'None'}\n"
            f"Hated NPC(s): {', '.join(self.hated_npc) if self.hated_npc else 'None'}"
        )