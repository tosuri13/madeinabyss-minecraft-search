BLOCK_MAPPING = {
    0: (1, 0),  # Stone
    1: (2, 0),  # Grass Block
    2: (3, 0),  # Dirt
    3: (4, 0),  # Cobblestone
    4: (7, 0),  # Bedrock
    5: (12, 0),  # Sand
    6: (13, 0),  # Gravel
    7: (82, 0),  # Clay
    8: (110, 0),  # Mycelium
    9: (208, 0),  # Grass Path
    10: (212, 0),  # Frosted Ice
    11: (79, 0),  # Ice
    12: (80, 0),  # Snow Block
    13: (174, 0),  # Packed Ice
    14: (78, 0),  # Snow Layer
    15: (172, 0),  # Terracotta
    16: (5, 0),  # Oak Wood Planks
    17: (5, 1),  # Spruce Wood Planks
    18: (5, 2),  # Birch Wood Planks
    19: (5, 3),  # Jungle Wood Planks
    20: (5, 4),  # Acacia Wood Planks
    21: (5, 5),  # Dark Oak Wood Planks
    22: (17, 0),  # Oak Log
    23: (17, 1),  # Spruce Log
    24: (17, 2),  # Birch Log
    25: (17, 3),  # Jungle Log
    26: (162, 0),  # Acacia Log
    27: (162, 1),  # Dark Oak Log
    28: (47, 0),  # Bookshelf
    29: (58, 0),  # Crafting Table
    30: (170, 0),  # Hay Bale
    31: (216, 0),  # Bone Block
    32: (14, 0),  # Gold Ore
    33: (15, 0),  # Iron Ore
    34: (16, 0),  # Coal Ore
    35: (21, 0),  # Lapis Lazuli Ore
    36: (56, 0),  # Diamond Ore
    37: (73, 0),  # Redstone Ore
    38: (129, 0),  # Emerald Ore
    39: (153, 0),  # Nether Quartz Ore
    40: (41, 0),  # Block of Gold
    41: (42, 0),  # Block of Iron
    42: (173, 0),  # Block of Coal
    43: (22, 0),  # Lapis Lazuli Block
    44: (57, 0),  # Block of Diamond
    45: (152, 0),  # Block of Redstone
    46: (133, 0),  # Block of Emerald
    47: (155, 0),  # Block of Quartz
    48: (24, 0),  # Sandstone
    49: (24, 1),  # Chiseled Sandstone
    50: (24, 2),  # Smooth Sandstone
    51: (179, 0),  # Red Sandstone
    52: (179, 1),  # Chiseled Red Sandstone
    53: (179, 2),  # Smooth Red Sandstone
    54: (45, 0),  # Bricks
    55: (98, 0),  # Stone Bricks
    56: (98, 1),  # Mossy Stone Bricks
    57: (98, 2),  # Cracked Stone Bricks
    58: (98, 3),  # Chiseled Stone Bricks
    59: (48, 0),  # Mossy Cobblestone
    60: (49, 0),  # Obsidian
    61: (155, 1),  # Chiseled Quartz Block
    62: (155, 2),  # Pillar Quartz Block
    63: (139, 0),  # Cobblestone Wall
    64: (44, 0),  # Stone Slab
    65: (44, 1),  # Sandstone Slab
    66: (44, 2),  # Wooden Slab
    67: (44, 3),  # Cobblestone Slab
    68: (44, 4),  # Brick Slab
    69: (44, 5),  # Stone Brick Slab
    70: (44, 6),  # Nether Brick Slab
    71: (44, 7),  # Quartz Slab
    72: (126, 0),  # Wooden Slab (Oak)
    73: (126, 1),  # Wooden Slab (Spruce)
    74: (126, 2),  # Wooden Slab (Birch)
    75: (126, 3),  # Wooden Slab (Jungle)
    76: (126, 4),  # Wooden Slab (Acacia)
    77: (126, 5),  # Wooden Slab (Dark Oak)
    78: (182, 0),  # Red Sandstone Slab
    79: (205, 0),  # Purpur Slab
    80: (53, 0),  # Oak Stairs
    81: (67, 0),  # Cobblestone Stairs
    82: (108, 0),  # Brick Stairs
    83: (109, 0),  # Stone Brick Stairs
    84: (114, 0),  # Nether Brick Stairs
    85: (128, 0),  # Sandstone Stairs
    86: (134, 0),  # Spruce Stairs
    87: (135, 0),  # Birch Stairs
    88: (136, 0),  # Jungle Stairs
    89: (156, 0),  # Quartz Stairs
    90: (163, 0),  # Acacia Stairs
    91: (164, 0),  # Dark Oak Stairs
    92: (180, 0),  # Red Sandstone Stairs
    93: (203, 0),  # Purpur Stairs
    94: (43, 0),  # Double Stone Slab
    95: (125, 0),  # Double Wooden Slab
    96: (35, 0),  # White Wool
    97: (35, 1),  # Orange Wool
    98: (35, 2),  # Magenta Wool
    99: (35, 3),  # Light Blue Wool
    100: (35, 4),  # Yellow Wool
    101: (35, 5),  # Lime Wool
    102: (35, 6),  # Pink Wool
    103: (35, 7),  # Gray Wool
    104: (35, 8),  # Light Gray Wool
    105: (35, 9),  # Cyan Wool
    106: (35, 10),  # Purple Wool
    107: (35, 11),  # Blue Wool
    108: (35, 12),  # Brown Wool
    109: (35, 13),  # Green Wool
    110: (35, 14),  # Red Wool
    111: (35, 15),  # Black Wool
    112: (171, 0),  # White Carpet
    113: (171, 1),  # Orange Carpet
    114: (171, 2),  # Magenta Carpet
    115: (171, 3),  # Light Blue Carpet
    116: (171, 4),  # Yellow Carpet
    117: (171, 5),  # Lime Carpet
    118: (171, 6),  # Pink Carpet
    119: (171, 7),  # Gray Carpet
    120: (171, 8),  # Light Gray Carpet
    121: (171, 9),  # Cyan Carpet
    122: (171, 10),  # Purple Carpet
    123: (171, 11),  # Blue Carpet
    124: (171, 12),  # Brown Carpet
    125: (171, 13),  # Green Carpet
    126: (171, 14),  # Red Carpet
    127: (171, 15),  # Black Carpet
    128: (20, 0),  # Glass
    129: (95, 0),  # White Stained Glass
    130: (95, 1),  # Orange Stained Glass
    131: (95, 2),  # Magenta Stained Glass
    132: (95, 3),  # Light Blue Stained Glass
    133: (95, 4),  # Yellow Stained Glass
    134: (95, 5),  # Lime Stained Glass
    135: (95, 6),  # Pink Stained Glass
    136: (95, 7),  # Gray Stained Glass
    137: (95, 8),  # Light Gray Stained Glass
    138: (95, 9),  # Cyan Stained Glass
    139: (95, 10),  # Purple Stained Glass
    140: (95, 11),  # Blue Stained Glass
    141: (95, 12),  # Brown Stained Glass
    142: (95, 13),  # Green Stained Glass
    143: (95, 14),  # Red Stained Glass
    144: (95, 15),  # Black Stained Glass
    145: (102, 0),  # Glass Pane
    146: (160, 0),  # White Stained Glass Pane
    147: (160, 1),  # Orange Stained Glass Pane
    148: (160, 2),  # Magenta Stained Glass Pane
    149: (160, 3),  # Light Blue Stained Glass Pane
    150: (160, 4),  # Yellow Stained Glass Pane
    151: (160, 5),  # Lime Stained Glass Pane
    152: (160, 6),  # Pink Stained Glass Pane
    153: (160, 7),  # Gray Stained Glass Pane
    154: (160, 8),  # Light Gray Stained Glass Pane
    155: (160, 9),  # Cyan Stained Glass Pane
    156: (160, 10),  # Purple Stained Glass Pane
    157: (160, 11),  # Blue Stained Glass Pane
    158: (160, 12),  # Brown Stained Glass Pane
    159: (160, 13),  # Green Stained Glass Pane
    160: (159, 0),  # White Stained Terracotta
    161: (159, 1),  # Orange Stained Terracotta
    162: (159, 2),  # Magenta Stained Terracotta
    163: (159, 3),  # Light Blue Stained Terracotta
    164: (159, 4),  # Yellow Stained Terracotta
    165: (159, 5),  # Lime Stained Terracotta
    166: (159, 6),  # Pink Stained Terracotta
    167: (159, 7),  # Gray Stained Terracotta
    168: (159, 8),  # Light Gray Stained Terracotta
    169: (159, 9),  # Cyan Stained Terracotta
    170: (159, 10),  # Purple Stained Terracotta
    171: (159, 11),  # Blue Stained Terracotta
    172: (159, 12),  # Brown Stained Terracotta
    173: (159, 13),  # Green Stained Terracotta
    174: (159, 14),  # Red Stained Terracotta
    175: (159, 15),  # Black Stained Terracotta
    176: (235, 0),  # White Glazed Terracotta
    177: (236, 0),  # Orange Glazed Terracotta
    178: (237, 0),  # Magenta Glazed Terracotta
    179: (238, 0),  # Light Blue Glazed Terracotta
    180: (239, 0),  # Yellow Glazed Terracotta
    181: (240, 0),  # Lime Glazed Terracotta
    182: (241, 0),  # Pink Glazed Terracotta
    183: (242, 0),  # Gray Glazed Terracotta
    184: (243, 0),  # Light Gray Glazed Terracotta
    185: (244, 0),  # Cyan Glazed Terracotta
    186: (245, 0),  # Purple Glazed Terracotta
    187: (246, 0),  # Blue Glazed Terracotta
    188: (247, 0),  # Brown Glazed Terracotta
    189: (248, 0),  # Green Glazed Terracotta
    190: (249, 0),  # Red Glazed Terracotta
    191: (250, 0),  # Black Glazed Terracotta
    192: (251, 0),  # White Concrete
    193: (251, 1),  # Orange Concrete
    194: (251, 2),  # Magenta Concrete
    195: (251, 3),  # Light Blue Concrete
    196: (251, 4),  # Yellow Concrete
    197: (251, 5),  # Lime Concrete
    198: (251, 6),  # Pink Concrete
    199: (251, 7),  # Gray Concrete
    200: (251, 8),  # Light Gray Concrete
    201: (251, 9),  # Cyan Concrete
    202: (251, 10),  # Purple Concrete
    203: (251, 11),  # Blue Concrete
    204: (251, 12),  # Brown Concrete
    205: (251, 13),  # Green Concrete
    206: (251, 14),  # Red Concrete
    207: (251, 15),  # Black Concrete
    208: (252, 0),  # White Concrete Powder
    209: (252, 1),  # Orange Concrete Powder
    210: (252, 2),  # Magenta Concrete Powder
    211: (252, 3),  # Light Blue Concrete Powder
    212: (252, 4),  # Yellow Concrete Powder
    213: (252, 5),  # Lime Concrete Powder
    214: (252, 6),  # Pink Concrete Powder
    215: (252, 7),  # Gray Concrete Powder
    216: (252, 8),  # Light Gray Concrete Powder
    217: (252, 9),  # Cyan Concrete Powder
    218: (252, 10),  # Purple Concrete Powder
    219: (252, 11),  # Blue Concrete Powder
    220: (252, 12),  # Brown Concrete Powder
    221: (252, 13),  # Green Concrete Powder
    222: (252, 14),  # Red Concrete Powder
    223: (252, 15),  # Black Concrete Powder
    224: (87, 0),  # Netherrack
    225: (88, 0),  # Soul Sand
    226: (89, 0),  # Glowstone
    227: (112, 0),  # Nether Brick
    228: (113, 0),  # Nether Brick Fence
    229: (214, 0),  # Nether Wart Block
    230: (215, 0),  # Red Nether Brick
    231: (213, 0),  # Magma Block
    232: (123, 0),  # Redstone Lamp (inactive)
    233: (124, 0),  # Redstone Lamp (active)
    234: (165, 0),  # Slime Block
    235: (101, 0),  # Iron Bars
    236: (84, 0),  # Jukebox
    237: (25, 0),  # Note Block
    238: (23, 0),  # Dispenser
    239: (116, 0),  # Enchanting Table
    240: (121, 0),  # End Stone
    241: (206, 0),  # End Stone Bricks
    242: (201, 0),  # Purpur Block
    243: (202, 0),  # Purpur Pillar
    244: (168, 0),  # Prismarine
    245: (168, 1),  # Prismarine Bricks
    246: (168, 2),  # Dark Prismarine
    247: (169, 0),  # Sea Lantern
    248: (103, 0),  # Melon Block
    249: (86, 0),  # Pumpkin
    250: (91, 0),  # Jack o'Lantern
    251: (198, 0),  # End Rod
    252: (85, 0),  # Oak Fence
    253: (188, 0),  # Spruce Fence
    254: (189, 0),  # Birch Fence
    255: (218, 0),  # Observer
}

REVERSE_BLOCK_MAPPING = {
    (id, data): byte_val for byte_val, (id, data) in BLOCK_MAPPING.items()
}
