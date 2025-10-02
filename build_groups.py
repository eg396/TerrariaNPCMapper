from group import Group
from itertools import combinations
import random
from copy import deepcopy

groups = []
ungrouped = set()

def compute_group_happiness(group_chars, include_biome=False):
    """
    Compute total happiness of a group.
    Base score = 1 per character.
    Loved NPCs = +0.5, liked NPCs = +0.2
    Disliked = -0.2, Hated = -0.5
    Optionally include biome overlap weight (+0.1 per overlap)
    """
    happiness = 0.0
    for char in group_chars:
        char_score = 1.00 # base happiness
        for other in group_chars:
            if other == char:
                continue
            if other.name in char.loved_npc:
                char_score += 0.5
            elif other.name in char.liked_npc:
                char_score += 0.2
            elif other.name in char.disliked_npc:
                char_score -= 0.2
            elif other.name in char.hated_npc:
                char_score -= 0.5

        if include_biome:
            for other in group_chars:
                if other == char:
                    continue
                overlap = set(char.liked_biome) & set(other.liked_biome)
                char_score += 0.1 * len(overlap)

        happiness += char_score
    return happiness / len(group_chars)  # average happiness


def build_groups(characters, include_biome=True, iterations=100):
    """
    Build groups from a list of characters.
    Runs multiple iterations with different random seeds to find the highest
    average happiness outcome.
    """
    global groups, ungrouped

    best_groups = None
    best_avg_happiness = -float("inf")

    for i in range(iterations):
        random_seed = random.randint(0, 1_000_000)
        random.seed(random_seed)

        # Reset globals for this iteration
        groups = []
        ungrouped = list(characters)
        random.shuffle(ungrouped)

        # Phase 1: Love-based groups
        make_love_groups()

        # Phase 2: Fill existing groups
        fill_groups(include_biome=include_biome)

        # Phase 3: Form new groups
        form_new_groups(include_biome=include_biome)

        # Compute average happiness for this iteration
        total_happiness = sum(g.happiness for g in groups)
        avg_happiness = total_happiness / len(groups) if groups else 0

        # Keep the best iteration
        print(f"Iteration {i+1}/{iterations} - Avg Happiness: {avg_happiness:.4f} with seed {random_seed}")
        if avg_happiness > best_avg_happiness:
            best_avg_happiness = avg_happiness
            # Deepcopy to store independent group objects
            best_groups = deepcopy(groups)

    # Set globals to the best iteration
    groups = best_groups
    ungrouped = set(c for g in groups for c in g.characters)  # optional: leftover handling

    return groups

def make_love_groups():
    """
    Create groups of 2 based on mutual love.
    If both characters share a liked biome, assign that biome to the group.
    Modifies the global 'groups' and 'ungrouped'.
    """
    global groups, ungrouped

    handled = set()  # Tracks characters already paired in this function

    for char in list(ungrouped):  # list() allows modification during iteration
        if char in handled:
            continue

        for other in list(ungrouped):
            if other == char or other in handled:
                continue

            # Mutual love check
            if char.name in other.loved_npc and other.name in char.loved_npc:
                
                # Biome check will be later
                group_biome = None

                # Create the group of size 2
                group = Group(biome=group_biome, happiness=2, characters=[char, other])
                groups.append(group)

                # Remove these characters from ungrouped and mark as handled
                ungrouped.remove(char)
                ungrouped.remove(other)
                handled.update([char, other])

                break  # Move to next char after forming a group

def fill_groups(include_biome=True):
    """
    Greedy filling for groups under 4 members.
    Operates on global 'groups' and 'ungrouped'.
    """
    global groups, ungrouped

    for group in groups:
        while len(group.characters) < 4 and ungrouped:

            best_candidate = None
            best_increase = -float("inf")

            for candidate in ungrouped:
                temp_group = group.characters + [candidate]
                happiness_with_biome = compute_group_happiness(temp_group, include_biome=include_biome)
                current_happiness = compute_group_happiness(group.characters, include_biome=include_biome)
                increase = happiness_with_biome - current_happiness

                if increase > best_increase:
                    best_increase = increase
                    best_candidate = candidate

            if best_candidate:
                group.characters.append(best_candidate)
                group.happiness = compute_group_happiness(group.characters, include_biome=include_biome)
                ungrouped.remove(best_candidate)
            else:
                break  # No good candidates left

def form_new_groups(include_biome=True):
    """
    Phase 3: Form new groups from remaining ungrouped characters.
    Operates on global 'groups' and 'ungrouped'.
    Minimum group size = 3, maximum = 4.
    """
    global groups, ungrouped

    while len(ungrouped) >= 3:  # minimum group size
        best_group = None
        best_score = -float("inf")

        # Try all possible group sizes 3-4
        sizes_to_try = []
        if len(ungrouped) % 4 == 0:
            sizes_to_try.append(4)
        elif len(ungrouped) % 4 < 4:
            sizes_to_try.append(3)
        for size in sizes_to_try:
            for candidate_group in combinations(ungrouped, size):
                score = compute_group_happiness(candidate_group, include_biome=include_biome)
                if score > best_score:
                    best_score = score
                    best_group = candidate_group

        # Form the best-scoring group
        if best_group:
            for char in best_group:
                ungrouped.remove(char)
            groups.append(Group(biome=None, happiness=best_score, characters=list(best_group)))

            if len(ungrouped) < 3:
                break  # Not enough left for another group

    # Handle leftover single NPCs (<3)
    if ungrouped:
        leftover = list(ungrouped)
        print(f"Leftover NPCs that couldn't form a group: {[c.name for c in leftover]}")