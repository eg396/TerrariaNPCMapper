# Terraria NPC Mapper

This was a side project I just did in a day because 1) I have too much free time and 2) I asked myself the important question of "What if I wasted my time to programatically figure out what the best groupings for my Terraria NPCs were?" 

# How to install and run

simply unpack the files and open them up in your favorite IDE (I personally use VS Code). Then navigate to main.py and run the program! You can choose to do it from your terminal if you'd like; this is a throwaway project so it doesn't really matter how you do it.

# How to add NPCs

In the "characters.txt" file, there's a bunch of characters listed out - I'll have the vanilla NPCs added for you, so if you want to add any other characters you'll have to do it yourself. The proper formatting for characters is the following:

- Name
- Liked and loved biomes
- Disliked and hated biomes
- Loved NPCs
- Liked NPCs
- Disliked NPCs
- Hated NPCs

# How does it work?

The algorithm here is greedy - as in, I am neglecting more refined methods of searching for connections between NPCs, and decided to just brute-force it by searching for the best possible connection and then moving on. Priority is first given to NPCs that 'love' each other, and is afterwards just looking for the strongest connections. Groups cannot be larger than 4; if there are leftover NPCs then the algorithm will deal with this by shortening the group size to 3 for a few groups until there is no leftover.