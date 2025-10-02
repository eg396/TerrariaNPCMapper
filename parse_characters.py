from character import Character

def parse_characters(file_path, include_outliers=False):
    characters = []
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]  # remove empty lines

    # Each character has 7 lines
    for i in range(0, len(lines), 7):
        block = lines[i:i+7]
        if len(block) < 7:
            print(f"Warning: incomplete character block at lines {i+1}-{i+7}")
            continue

        name = block[0]

        # Check if the character is an outlier
        if not include_outliers and name in ["Princess", "Santa Claus", "Jungle Tyrant"]:
            continue

        # Characters might not have disliked biomes or loved and hated NPCs
        # Convert "None" to None to handle absence
        for j in [3, 6]:
            if block[j] == "None":
                block[j] = None

        # handle all NPC fields
        # Convert single entries to list for consistency
        liked_biome = block[1].split(",") if "," in block[1] else [block[1]]
        disliked_biome = block[2].split(",") if "," in block[2] else [block[2]]
        liked_npc = block[4].split(",") if "," in block[4] else [block[4]]
        disliked_npc = block[5].split(",") if "," in block[5] else [block[5]]

        # Loved and hated NPCs are a bit special as they can be None, single, or multiple entries
        loved_npc = block[3].split(",") if block[3] and "," in block[3] else ([block[3]] if block[3] else [])
        hated_npc = block[6].split(",") if block[6] and "," in block[6] else ([block[6]] if block[6] else [])

        # Remove outliers from lists if present
        # redundant code! I don't care
        if not include_outliers:
            for npc_list in [loved_npc, liked_npc, disliked_npc, hated_npc]:
                if "Princess" in npc_list:
                    npc_list.remove("Princess")
                if "Santa Claus" in npc_list:
                    npc_list.remove("Santa Claus")
                if "Jungle Tyrant" in npc_list:
                    npc_list.remove("Jungle Tyrant")

        # Create Character object
        character = Character(
            name=name,
            liked_biome=liked_biome,
            disliked_biome=disliked_biome,
            loved_npc=loved_npc,
            liked_npc=liked_npc,
            disliked_npc=disliked_npc,
            hated_npc=hated_npc
        )
        characters.append(character)

    return characters
