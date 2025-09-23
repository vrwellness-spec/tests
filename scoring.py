
# Complete Scale Definitions and Scoring Logic for MCMI-III

SCALE_DEFINITIONS = {
    # Modifying Indices
    'Y': {
        'true': [32, 51, 57, 59, 80, 82, 88, 97, 137, 172],
        'false': [20, 35, 40, 69, 104, 112, 123, 141, 142, 148, 151]
    },
    'Z': {
        'true': [1, 4, 8, 15, 22, 24, 30, 34, 36, 37, 44, 55, 56, 58, 62, 63, 70, 74, 75, 76, 83, 84, 86, 99, 111, 123, 128, 133, 134, 142, 145, 150, 171]
    },
    # Clinical Personality Pattern Scales
    '1': {
        'true': {1: [4, 38, 48, 101, 142, 156, 167], 2: [10, 27, 46, 92, 105, 148, 165]},
        'false': {1: [32, 57]}
    },
    '2A': {
        'true': {1: [47, 48, 146, 148, 151, 158], 2: [18, 40, 69, 84, 99, 127, 141, 174]},
        'false': {1: [57, 80]}
    },
    '2B': {
        'true': {1: [24, 43, 83, 86, 142, 148, 154], 2: [20, 25, 47, 112, 123, 133, 145, 151]}
    },
    '3': {
        'true': {1: [47, 56, 84, 120, 133, 141, 151], 2: [16, 35, 45, 73, 94, 108, 135, 169]},
        'false': {1: [82]}
    },
    '4': {
        'true': {2: [12, 21, 32, 51, 57, 80, 88]},
        'false': {1: [10, 24, 27, 48, 69, 92, 99, 123, 127, 174]}
    },
    '5': {
        'true': {1: [21, 38, 57, 80, 88, 116], 2: [5, 26, 31, 67, 85, 93, 144, 159]},
        'false': {1: [35, 40, 47, 69, 84, 86, 94, 99, 141, 169]}
    },
    '6A': {
        'true': {1: [7, 13, 14, 21, 41, 52, 93, 122, 136], 2: [17, 38, 53, 101, 113, 139, 166]},
        'false': {1: [172]}
    },
    '6B': {
        'true': {1: [7, 13, 17, 33, 36, 39, 41, 49, 53, 79, 93, 96, 166], 2: [9, 14, 28, 64, 87, 95, 116]}
    },
    '7': {
        'true': {2: [2, 29, 59, 82, 97, 114, 137, 172]},
        'false': {1: [7, 14, 22, 41, 53, 72, 101, 139, 166]}
    },
    '8A': {
        'true': {1: [6, 42, 83, 98, 122, 133, 166], 2: [7, 15, 22, 36, 50, 60, 79, 115, 126]}
    },
    '8B': {
        'true': {1: [18, 24, 25, 35, 40, 98, 148, 169], 2: [19, 43, 70, 90, 104, 122, 161]}
    },
    'S': {
        'true': {1: [69, 99, 102, 134, 141, 148, 151], 2: [8, 48, 71, 76, 117, 138, 156, 158, 162]}
    },
    'C': {
        'true': {1: [7, 22, 122, 135, 161, 166, 171], 2: [30, 41, 72, 83, 98, 120, 134, 142, 154]}
    },
    'P': {
        'true': {1: [8, 48, 60, 63, 115, 138, 158, 159], 2: [6, 33, 42, 49, 89, 103, 146, 167, 175]}
    },
    'A': {
        'true': {1: [40, 61, 76, 108, 109, 135, 145, 149], 2: [58, 75, 124, 147, 164, 170]}
    },
    'H': {
        'true': {1: [1, 75, 107, 111, 130, 145, 148], 2: [4, 11, 37, 55, 74]}
    },
    'N': {
        'true': {1: [22, 41, 51, 83, 117, 134, 166, 170], 2: [3, 54, 96, 106, 125]}
    },
    'D': {
        'true': {1: [15, 25, 55, 83, 104, 141, 142, 148], 2: [24, 56, 62, 86, 111, 130]}
    },
    'B': {
        'true': {1: [14, 41, 64, 93, 101, 113, 122, 139, 166], 2: [52, 77, 100, 131, 152]},
        'false': {2: [23]}
    },
    'T': {
        'true': {1: [7, 21, 38, 41, 53, 101, 113, 139], 2: [13, 39, 66, 91, 118, 136]}
    },
    'R': {
        'true': {1: [62, 76, 83, 123, 133, 142, 147, 148, 151, 154, 164], 2: [109, 129, 149, 160, 173]}
    },
    'SS': {
        'true': {1: [22, 56, 72, 76, 83, 117, 134, 142, 148, 151, 162], 2: [34, 61, 68, 78, 102, 168]}
    },
    'CC': {
        'true': {1: [4, 34, 55, 74, 104, 111, 130, 142, 148, 149, 154], 2: [1, 44, 107, 128, 150, 171]}
    },
    'PP': {
        'true': {1: [5, 38, 49, 67, 89, 103, 138, 159, 175], 2: [63, 119, 140, 153]}
    }
}

def calculate_raw_scores(responses):
    raw_scores = {}
    for scale, definition in SCALE_DEFINITIONS.items():
        score = 0
        if 'true' in definition:
            true_def = definition['true']
            if isinstance(true_def, dict):
                for weight, items in true_def.items():
                    for item in items:
                        if responses.get(str(item)) is True:
                            score += weight
            elif isinstance(true_def, list):
                for item in true_def:
                    if responses.get(str(item)) is True:
                        score += 1

        if 'false' in definition:
            false_def = definition['false']
            if isinstance(false_def, dict):
                for weight, items in false_def.items():
                    for item in items:
                        if responses.get(str(item)) is False:
                            score += weight
            elif isinstance(false_def, list):
                for item in false_def:
                    if responses.get(str(item)) is False:
                        score += 1
        raw_scores[scale] = score

    scale_x_components = ['1', '2A', '2B', '3', '4', '6A', '6B', '7', '8A', '8B']
    raw_scores['X'] = sum(raw_scores.get(s, 0) for s in scale_x_components) + int(raw_scores.get('5', 0) * 2/3)
    
    return raw_scores

def convert_scale_x_raw_to_br(raw_score):
    conversion_table = {
        **{i: 0 for i in range(0, 38)},
        39: 2, 40: 3, 41: 5, 42: 6, 43: 8, 44: 9, 45: 11, 46: 12, 47: 14, 48: 15, 49: 17, 50: 18, 51: 20, 52: 21, 53: 23,
        54: 24, 55: 26, 56: 27, 57: 29, 58: 30, 59: 32, 60: 33, 61: 35, 62: 36, 63: 37, 64: 37, 65: 38, 66: 39, 67: 39, 68: 40, 69: 41, 70: 41, 71: 42,
        72: 43, 73: 43, 74: 44, 75: 45, 76: 45, 77: 46, 78: 47, 79: 47, 80: 48, 81: 49, 82: 49, 83: 50, 84: 51, 85: 51, 86: 52, 87: 53, 88: 53, 89: 54,
        90: 55, 91: 55, 92: 56, 93: 57, 94: 57, 95: 58, 96: 59, 97: 59, 98: 60, 99: 61, 100: 61, 101: 62, 102: 63, 103: 63, 104: 64, 105: 65, 106: 65,
        107: 66, 108: 67, 109: 67, 110: 68, 111: 69, 112: 69, 113: 70, 114: 71, 115: 71, 116: 72, 117: 73, 118: 73, 119: 74, 120: 74, 121: 75, 122: 75,
        123: 75, 124: 76, 125: 76, 126: 76, 127: 77, 128: 77, 129: 77, 130: 78, 131: 78, 132: 78, 133: 79, 134: 79, 135: 79, 136: 80, 137: 80, 138: 80,
        139: 81, 140: 81, 141: 81, 142: 82, 143: 82, 144: 82, 145: 83, 146: 83, 147: 84, 148: 84, 149: 85, 150: 85, 151: 86, 152: 86, 153: 87, 154: 88,
        155: 88, 156: 89, 157: 89, 158: 90, 159: 90, 160: 91, 161: 92, 162: 92, 163: 93, 164: 93, 165: 94, 166: 94, 167: 95, 168: 95, 169: 96, 170: 96,
        171: 97, 172: 97, 173: 98, 174: 99, 175: 100, 176: 100, 177: 100, 178: 100
    }
    if raw_score < 0: return 0
    return conversion_table.get(raw_score, 100)

def convert_raw_to_br_all_scales(raw_scores):
    br_conversion_tables = {
        '1': {0: 0, 1: 12, 2: 24, 3: 36, 4: 48, 5: 60, 6: 62, 7: 64, 8: 66, 9: 68, 10: 70, 11: 72, 12: 75, 13: 78, 14: 81, 15: 85, 16: 89, 17: 93, 18: 97, 19: 101, 20: 105, 21: 109, 22: 112, 23: 115},
        '2A': {0: 0, 1: 12, 2: 24, 3: 36, 4: 48, 5: 60, 6: 63, 7: 67, 8: 71, 9: 75, 10: 77, 11: 79, 12: 81, 13: 83, 14: 85, 15: 88, 16: 91, 17: 94, 18: 97, 19: 100, 20: 103, 21: 106, 22: 109, 23: 112, 24: 115},
        '2B': {0: 0, 1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 65, 8: 70, 9: 75, 10: 77, 11: 79, 12: 81, 13: 83, 14: 85, 15: 89, 16: 92, 17: 96, 18: 99, 19: 103, 20: 106, 21: 109, 22: 112, 23: 115},
        '3': {0: 0, 1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 65, 8: 70, 9: 75, 10: 78, 11: 81, 12: 83, 13: 85, 14: 87, 15: 89, 16: 91, 17: 94, 18: 97, 19: 100, 20: 103, 21: 106, 22: 109, 23: 112, 24: 115},
        '4': {0: 0, 1: 4, 2: 8, 3: 12, 4: 16, 5: 20, 6: 24, 7: 28, 8: 32, 9: 36, 10: 40, 11: 44, 12: 48, 13: 51, 14: 54, 15: 57, 16: 60, 17: 63, 18: 66, 19: 69, 20: 72, 21: 75, 22: 79, 23: 83, 24: 88},
        '5': {0: 0, 1: 5, 2: 10, 3: 15, 4: 20, 5: 25, 6: 30, 7: 35, 8: 40, 9: 44, 10: 48, 11: 52, 12: 56, 13: 60, 14: 63, 15: 67, 16: 71, 17: 75, 18: 85, 19: 89, 20: 93, 21: 97, 22: 101, 23: 105, 24: 110, 25: 115},
        '6A': {0: 0, 1: 12, 2: 26, 3: 36, 4: 48, 5: 60, 6: 62, 7: 64, 8: 66, 9: 69, 10: 71, 11: 73, 12: 75, 13: 79, 14: 82, 15: 85, 16: 89, 17: 92, 18: 96, 19: 99, 20: 103, 21: 106, 22: 109, 23: 112, 24: 115},
        '6B': {0: 0, 1: 12, 2: 26, 3: 36, 4: 48, 5: 60, 6: 62, 7: 64, 8: 66, 9: 68, 10: 69, 11: 70, 12: 71, 13: 72, 14: 73, 15: 74, 16: 75, 17: 78, 18: 80, 19: 83, 20: 85, 21: 90, 22: 95, 23: 100, 24: 105, 25: 110, 26: 115},
        '7': {0: 0, 1: 4, 2: 8, 3: 12, 4: 16, 5: 20, 6: 24, 7: 28, 8: 32, 9: 36, 10: 39, 11: 42, 12: 45, 13: 48, 14: 51, 15: 54, 16: 57, 17: 60, 18: 63, 19: 66, 20: 69, 21: 72, 22: 75, 23: 79, 24: 83, 25: 87},
        '8A': {0: 0, 1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 62, 8: 64, 9: 66, 10: 68, 11: 70, 12: 72, 13: 75, 14: 77, 15: 79, 16: 81, 17: 83, 18: 85, 19: 89, 20: 93, 21: 97, 22: 101, 23: 105, 24: 110, 25: 115},
        '8B': {0: 0, 1: 20, 2: 40, 3: 60, 4: 63, 5: 66, 6: 69, 7: 72, 8: 75, 9: 78, 10: 80, 11: 82, 12: 85, 13: 88, 14: 91, 15: 94, 16: 97, 17: 100, 18: 103, 19: 106, 20: 109, 21: 112, 22: 115},
        'S': {0: 0, 1: 20, 2: 40, 3: 60, 4: 62, 5: 64, 6: 66, 7: 67, 8: 68, 9: 69, 10: 70, 11: 71, 12: 72, 13: 73, 14: 74, 15: 75, 16: 78, 17: 81, 18: 85, 19: 90, 20: 95, 21: 99, 22: 103, 23: 107, 24: 111, 25: 115},
        'C': {0: 0, 1: 12, 2: 24, 3: 36, 4: 48, 5: 60, 6: 63, 7: 66, 8: 69, 9: 72, 10: 75, 11: 77, 12: 79, 13: 81, 14: 83, 15: 85, 16: 88, 17: 91, 18: 94, 19: 97, 20: 100, 21: 103, 22: 106, 23: 109, 24: 112, 25: 115},
        'P': {0: 0, 1: 15, 2: 30, 3: 45, 4: 60, 5: 61, 6: 63, 7: 64, 8: 66, 9: 67, 10: 69, 11: 70, 12: 72, 13: 73, 14: 75, 15: 77, 16: 79, 17: 81, 18: 83, 19: 85, 20: 90, 21: 95, 22: 100, 23: 105, 24: 110, 25: 115},
        'A': {0: 0, 1: 20, 2: 40, 3: 60, 4: 75, 5: 77, 6: 79, 7: 81, 8: 83, 9: 85, 10: 87, 11: 89, 12: 91, 13: 94, 14: 97, 15: 100, 16: 103, 17: 106, 18: 109, 19: 112, 20: 115},
        'H': {0: 0, 1: 15, 2: 30, 3: 45, 4: 60, 5: 62, 6: 64, 7: 66, 8: 68, 9: 70, 10: 72, 11: 73, 12: 74, 13: 75, 14: 80, 15: 85, 16: 100, 17: 115},
        'N': {0: 0, 1: 12, 2: 24, 3: 36, 4: 48, 5: 60, 6: 63, 7: 66, 8: 69, 9: 72, 10: 75, 11: 80, 12: 85, 13: 90, 14: 95, 15: 100, 16: 105, 17: 110, 18: 115},
        'D': {0: 0, 1: 12, 2: 24, 3: 36, 4: 48, 5: 60, 6: 62, 7: 64, 8: 66, 9: 69, 10: 72, 11: 75, 12: 78, 13: 80, 14: 82, 15: 85, 16: 91, 17: 97, 18: 103, 19: 109, 20: 115},
        'B': {0: 0, 1: 20, 2: 40, 3: 60, 4: 63, 5: 67, 6: 71, 7: 75, 8: 77, 9: 80, 10: 83, 11: 85, 12: 88, 13: 91, 14: 95, 15: 99, 16: 103, 17: 107, 18: 111, 19: 115},
        'T': {0: 0, 1: 20, 2: 40, 3: 62, 4: 65, 5: 69, 6: 71, 7: 73, 8: 75, 9: 77, 10: 79, 11: 81, 12: 85, 13: 90, 14: 95, 15: 100, 16: 105, 17: 110, 18: 115},
        'R': {0: 0, 1: 15, 2: 30, 3: 45, 4: 60, 5: 62, 6: 63, 7: 65, 8: 66, 9: 68, 10: 69, 11: 71, 12: 73, 13: 75, 14: 77, 15: 79, 16: 81, 17: 83, 18: 85, 19: 95, 20: 105, 21: 115},
        'SS': {0: 0, 1: 15, 2: 30, 3: 45, 4: 60, 5: 62, 6: 64, 7: 66, 8: 67, 9: 68, 10: 69, 11: 70, 12: 71, 13: 72, 14: 73, 15: 74, 16: 75, 17: 79, 18: 82, 19: 85, 20: 93, 21: 100, 22: 108, 23: 115},
        'CC': {0: 0, 1: 15, 2: 30, 3: 45, 4: 60, 5: 65, 6: 70, 7: 75, 8: 78, 9: 81, 10: 85, 11: 87, 12: 89, 13: 91, 14: 93, 15: 95, 16: 97, 17: 99, 18: 101, 19: 103, 20: 106, 21: 109, 22: 112, 23: 115},
        'PP': {0: 0, 1: 30, 2: 60, 3: 62, 4: 65, 5: 68, 6: 70, 7: 72, 8: 75, 9: 80, 10: 85, 11: 90, 12: 95, 13: 100, 14: 105, 15: 110, 16: 115},
        'Y': {0: 0, 1: 5, 2: 10, 3: 15, 4: 20, 5: 25, 6: 30, 7: 35, 8: 39, 9: 43, 10: 47, 11: 51, 12: 55, 13: 59, 14: 63, 15: 67, 16: 71, 17: 75, 18: 80, 19: 85, 20: 93, 21: 100},
        'Z': {0: 0, 1: 18, 2: 35, 3: 38, 4: 40, 5: 42, 6: 45, 7: 47, 8: 49, 9: 52, 10: 54, 11: 56, 12: 59, 13: 61, 14: 63, 15: 66, 16: 68, 17: 70, 18: 73, 19: 75, 20: 76, 21: 78, 22: 79, 23: 81, 24: 82, 25: 84, 26: 85, 27: 88, 28: 90, 29: 92, 30: 94, 31: 96, 32: 98, 33: 100}
    }
    br_scores = {}
    for scale, raw_score in raw_scores.items():
        if scale == 'X':
            br_scores[scale] = convert_scale_x_raw_to_br(raw_score)
            continue
        if scale in br_conversion_tables:
            conversion_table = br_conversion_tables[scale]
            if raw_score in conversion_table:
                br_scores[scale] = conversion_table[raw_score]
            else:
                max_raw = max(conversion_table.keys())
                br_scores[scale] = 115 if raw_score > max_raw else 0
        else:
            br_scores[scale] = 0
    return br_scores

# --- Disclosure Adjustment Tables (Table 1 from MCMI-III Manual) ---
# Based on Scale X RAW score (not BR score)
# Format: raw_score: (1st-BR_adjustment, S-PP_adjustment)
# NOTE: This adjustment is based on the Scale X RAW score (not the BR score)
DISCLOSURE_ADJUSTMENT = {
    # Raw scores 0-33: +20 for Clinical Personality Patterns (1-8B), +10 for Severe Personality Pathology (S-PP)
    **{i: (20, 10) for i in range(0, 34)},
    
    # Specific adjustments for raw scores 34-179 based on official MCMI-III Table 1
    34: (20, 10), 35: (20, 10), 36: (20, 10), 37: (19, 10),
    38: (18, 10), 39: (17, 9), 40: (17, 9), 41: (16, 9), 42: (15, 8), 43: (14, 8),
    44: (13, 7), 45: (13, 7), 46: (12, 7), 47: (11, 6), 48: (10, 6), 49: (9, 5), 
    50: (9, 5), 51: (8, 5), 52: (7, 4), 53: (6, 4), 54: (5, 3), 55: (5, 3), 
    56: (4, 3), 57: (3, 2), 58: (2, 2), 59: (1, 1), 60: (1, 1),
    
    # Raw scores 61-123: No adjustment (normal range)
    **{i: (0, 0) for i in range(61, 124)},
    
    # Specific adjustments for raw scores 124-179 based on official MCMI-III Table 1
    124: (-1, -1), 125: (-1, -1), 126: (-1, -1), 127: (-2, -2), 128: (-2, -2), 
    129: (-3, -2), 130: (-3, -2), 131: (-3, -2), 132: (-4, -3), 133: (-4, -3), 
    134: (-5, -3), 135: (-5, -3), 136: (-5, -3), 137: (-6, -4), 138: (-6, -4), 
    139: (-7, -4), 140: (-7, -4), 141: (-7, -4), 142: (-8, -5), 143: (-8, -5), 
    144: (-9, -5), 145: (-9, -5), 146: (-9, -5), 147: (-10, -6), 148: (-10, -6), 
    149: (-11, -6), 150: (-11, -6), 151: (-11, -6), 152: (-12, -7), 153: (-12, -7), 
    154: (-13, -7), 155: (-13, -7), 156: (-13, -7), 157: (-14, -8), 158: (-14, -8), 
    159: (-15, -8), 160: (-15, -8), 161: (-15, -8), 162: (-16, -9), 163: (-16, -9), 
    164: (-17, -9), 165: (-17, -9), 166: (-17, -9), 167: (-18, -10), 168: (-18, -10), 
    169: (-19, -10), 170: (-19, -10), 171: (-19, -10), 172: (-20, -11), 173: (-20, -11), 
    174: (-20, -11), 175: (-20, -11), 176: (-20, -11), 177: (-20, -11), 178: (-20, -11), 
    179: (-20, -11)
}

# --- A/D Adjustment Tables (Table 2 from MCMI-III Manual) ---
# Table 2: Non-Inpatient, or Inpatient and Axis I Duration of More Than Four Weeks
AD_ADJUSTMENT_TABLE_2 = {
    # 2B, 8B, C adjustments
    '2B_8B_C': {
        0: -1, 1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1,
        10: -2, 11: -2, 12: -2, 13: -2, 14: -2, 15: -3, 16: -3, 17: -3, 18: -3, 19: -3,
        20: -4, 21: -4, 22: -4, 23: -4, 24: -4, 25: -5, 26: -5, 27: -5, 28: -5, 29: -5,
        30: -6, 31: -6, 32: -6, 33: -6, 34: -6, 35: -7, 36: -7, 37: -7, 38: -7, 39: -7,
        40: -8, 41: -8, 42: -8, 43: -8, 44: -8, 45: -9, 46: -9, 47: -9, 48: -9, 49: -9,
        50: -10, 51: -10, 52: -10, 53: -10, 54: -10, 55: -11, 56: -11, 57: -11, 58: -11, 59: -11,
        60: -12, 61: -12, 62: -12, 63: -12, 64: -12, 65: -13, 66: -13, 67: -13, 68: -13, 69: -13,
        70: -14, 71: -14, 72: -14, 73: -14, 74: -14, 75: -15, 76: -15, 77: -15, 78: -15, 79: -15, 80: -15
    },
    # 2A, S adjustments
    '2A_S': {
        0: -1, 1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1,
        9: -1, 10: -1, 11: -1, 12: -1, 13: -1, 14: -1, 15: -1,
        16: -2, 17: -2, 18: -2, 19: -2, 20: -2, 21: -2, 22: -2, 23: -2,
        24: -3, 25: -3, 26: -3, 27: -3, 28: -3, 29: -3, 30: -3, 31: -3,
        32: -4, 33: -4, 34: -4, 35: -4, 36: -4, 37: -4, 38: -4, 39: -4,
        40: -5, 41: -5, 42: -5, 43: -5, 44: -5, 45: -5, 46: -5, 47: -5,
        48: -6, 49: -6, 50: -6, 51: -6, 52: -6, 53: -6, 54: -6, 55: -6,
        56: -7, 57: -7, 58: -7, 59: -7, 60: -7, 61: -7, 62: -7, 63: -7,
        64: -8, 65: -8, 66: -8, 67: -8, 68: -8, 69: -8, 70: -8, 71: -8,
        72: -9, 73: -9, 74: -9, 75: -9, 76: -9, 77: -9, 78: -9, 79: -9, 80: -10
    }
}

def calculate_all_scores(responses):
    raw_scores = calculate_raw_scores(responses)
    br_scores = convert_raw_to_br_all_scales(raw_scores)
    
    adjustments = {scale: 0 for scale in raw_scores.keys()}
    disclosure_adjustments = {scale: 0 for scale in raw_scores.keys()}
    ad_adjustments = {scale: 0 for scale in raw_scores.keys()}
    final_scores = br_scores.copy()

    # Step 1: Disclosure Adjustment (based on Scale X RAW score)
    # Step 1-1: In Table 1, locate the BR score range that contains the respondent's Scale X raw score
    # Step 1-2: Find the adjustments that correspond to the respondent's raw score on Scale X
    # Step 1-3: Apply the 1st-BR adjustment to BR scores for Scales 1-8B. Apply the S-PP adjustment to BR scores for Scales S-PP
    
    raw_x = raw_scores.get('X', 0)
    x_adj, spp_adj = DISCLOSURE_ADJUSTMENT.get(raw_x, (0, 0))

    # Define scale categories as per MCMI-III manual
    personality_pattern_scales = ['1', '2A', '2B', '3', '4', '5', '6A', '6B', '7', '8A', '8B']
    severe_pathology_scales = ['S', 'C', 'PP']

    # Apply 1st-BR adjustment to Clinical Personality Pattern scales (1-8B)
    for scale in personality_pattern_scales:
        if scale in final_scores:
            disclosure_adjustments[scale] = x_adj
            final_scores[scale] += x_adj
    
    # Apply S-PP adjustment to Severe Personality Pathology scales (S, C, P)
    for scale in severe_pathology_scales:
        if scale in final_scores:
            disclosure_adjustments[scale] = spp_adj
            final_scores[scale] += spp_adj
    
    # Apply S-PP adjustment to Clinical Syndromes scales (A, H, N, D, B, T, R)
    clinical_syndromes_scales = ['A', 'H', 'N', 'D', 'B', 'T', 'R']
    for scale in clinical_syndromes_scales:
        if scale in final_scores:
            disclosure_adjustments[scale] = spp_adj
            final_scores[scale] += spp_adj
    
    # Apply S-PP adjustment to Severe Clinical Syndromes scales (SS, CC, PP)
    severe_clinical_syndromes_scales = ['SS', 'CC', 'PP']
    for scale in severe_clinical_syndromes_scales:
        if scale in final_scores:
            disclosure_adjustments[scale] = spp_adj
            final_scores[scale] += spp_adj

    # A/D Adjustment (Anxiety + Dysthymia)
    # Based on MCMI-III manual: A/D adjustment uses Scale A (Anxiety) and Scale D (Dysthymia)
    ad_value = raw_scores.get('A', 0) + raw_scores.get('D', 0)
    
    # Apply A/D adjustments to scales 2B, 8B, and C using 2B_8B_C table
    scales_2b_8b_c = ['2B', '8B', 'C']
    for scale in scales_2b_8b_c:
        if scale in final_scores:
            # Use 2B_8B_C adjustment table for these specific scales
            ad_adj = AD_ADJUSTMENT_TABLE_2['2B_8B_C'].get(ad_value, 0)
            ad_adjustments[scale] = ad_adj
            final_scores[scale] += ad_adj
    
    # Apply A/D adjustments to scales 2A and S using 2A_S table
    scales_2a_s = ['2A', 'S']
    for scale in scales_2a_s:
        if scale in final_scores:
            # Use 2A_S adjustment table for these specific scales
            ad_adj = AD_ADJUSTMENT_TABLE_2['2A_S'].get(ad_value, 0)
            ad_adjustments[scale] = ad_adj
            final_scores[scale] += ad_adj

    # Denial/Complaint Adjustment
    # Step 4-1: Determine which Clinical Personality Patterns scale has the highest BR score
    # Clinical Personality Patterns scales: 1, 2A, 2B, 3, 4, 5, 6A, 6B, 7, 8A, 8B
    clinical_personality_scales = ['1', '2A', '2B', '3', '4', '5', '6A', '6B', '7', '8A', '8B']
    dc_adjustments = {scale: 0 for scale in raw_scores.keys()}
    
    # Get BR scores for Clinical Personality Patterns scales after disclosure and A/D adjustments
    clinical_br_scores = {}
    for scale in clinical_personality_scales:
        if scale in final_scores:
            clinical_br_scores[scale] = final_scores[scale]
    
    if clinical_br_scores:
        # Find the highest BR score among Clinical Personality Patterns scales
        highest_br_score = max(clinical_br_scores.values())
        highest_scales = [scale for scale, score in clinical_br_scores.items() if score == highest_br_score]
        
        # Step 4-2: Apply Denial/Complaint adjustment based on highest ranked scale
        # If highest ranked scale is 6A, 6B, 2A, 8A, 7, 4, 5, 3, 1 - adjustment value is 8
        # If highest ranked scale is anything else - no adjustment is made
        adjustment_scales_8_point = ['6A', '6B', '2A', '8A', '7', '4', '5', '3', '1']
        
        # Check if any of the highest scoring scales qualify for 8-point adjustment
        needs_adjustment = any(scale in adjustment_scales_8_point for scale in highest_scales)
        
        if needs_adjustment:
            # Step 4-3: Add 8-point adjustment to highest ranking scales 4, 5, and 7
            target_scales = ['4', '5', '7']
            for scale in target_scales:
                if scale in final_scores:
                    dc_adjustments[scale] = 8
                    final_scores[scale] += 8

    # After the adjustments are applied, any BR values that are less than 0 should be changed to 0,
    # and any BR values that are greater than 115 should be changed to 115
    for scale in final_scores:
        final_scores[scale] = max(0, min(115, final_scores[scale]))
        adjustments[scale] = disclosure_adjustments.get(scale, 0) + ad_adjustments.get(scale, 0) + dc_adjustments.get(scale, 0)

    detailed_breakdown = [
        {
            'scale': scale, 
            'raw': raw_scores.get(scale, 0), 
            'br': br_scores.get(scale, 0), 
            'disclosure_adj': disclosure_adjustments.get(scale, 0), 
            'ad_adj': ad_adjustments.get(scale, 0) if ad_adjustments.get(scale, 0) != 0 else '', 
            'dc_adj': dc_adjustments.get(scale, 0) if dc_adjustments.get(scale, 0) != 0 else '',
            'total_adj': adjustments.get(scale, 0), 
            'final': final_scores.get(scale, 0),
            'ad_value': ad_value,  # Add A/D value for debugging
            'blank_spaces': '',  # Keep blank for individual rows
            'adjustment_debug': f"[{scale}: {ad_adjustments.get(scale, 0)}]" if ad_adjustments.get(scale, 0) != 0 else '',  # Show adjustment per scale only if adjusted
            'has_ad_adjustment': ad_adjustments.get(scale, 0) != 0,  # Flag to identify adjusted scales
            'has_dc_adjustment': dc_adjustments.get(scale, 0) != 0   # Flag to identify DC adjusted scales
        }
        for scale in sorted(raw_scores.keys(), key=lambda x: (len(x), x))
    ]
    
    # Add A/D adjustment summary information
    ad_summary = {
        'ad_value': ad_value,
        'ad_calculation': f"A+D = {raw_scores.get('A', 0)} + {raw_scores.get('D', 0)} = {ad_value}",
        'adjusted_scales': [scale for scale in ad_adjustments.keys() if ad_adjustments[scale] != 0],
        'adjustment_reason': f"A/D adjustment applied to scales: {', '.join([scale for scale in ad_adjustments.keys() if ad_adjustments[scale] != 0])}"
    }

    validity_report = assess_profile_validity(responses, raw_scores)

    return {
        'detailed_breakdown': detailed_breakdown,
        'ad_summary': ad_summary,
        'validity_report': validity_report
    }

# --- Validity Scales ---
def calculate_scale_v_invalidity(responses):
    invalidity_items = [65, 110, 157]
    raw_score = 0
    for item in invalidity_items:
        if responses.get(str(item)) is True:
            raw_score += 1
    return raw_score

def calculate_scale_w_inconsistency(responses):
    inconsistency_pairs = [(1, 4), (1, 4), (8, 14), (4, 3), (6, 6), (13, 66), (65, 133), (20, 112), (20, 112), (22, 83), (24, 15), (25, 56), (25, 56), (27, 92), (32, 84), (35, 84), (35, 84), (39, 118), (39, 118), (41, 166), (44, 86), (44, 150), (48, 92), (49, 146), (52, 152), (55, 130), (57, 80), (61, 76), (62, 56), (68, 162), (69, 99), (70, 104), (72, 142), (74, 107), (77, 131), (91, 136), (91, 136), (108, 135), (109, 164), (123, 128), (129, 173), (133, 145), (147, 149), (160, 164), (160, 173)]
    raw_score = 0
    for item1, item2 in inconsistency_pairs:
        if str(item1) in responses and str(item2) in responses:
            if responses[str(item1)] != responses[str(item2)]:
                raw_score += 1
    return raw_score

def get_validity_interpretation(v_score, w_score):
    interpretations = []
    if v_score == 0: interpretations.append("Scale V: Valid - No obvious invalidity")
    elif v_score == 1: interpretations.append("Scale V: Questionable - Minor invalidity concerns")
    else: interpretations.append("Scale V: Invalid - Profile may be unreliable")
    if w_score <= 5: interpretations.append("Scale W: Consistent - Acceptable consistency")
    elif w_score <= 10: interpretations.append("Scale W: Moderately Inconsistent - Some response inconsistency")
    elif w_score <= 15: interpretations.append("Scale W: Highly Inconsistent - Significant inconsistency")
    else: interpretations.append("Scale W: Very Inconsistent - Profile reliability questionable")
    return interpretations

def determine_overall_validity(v_score, w_score, x_raw=None):
    if v_score >= 2: return "INVALID - Scale V indicates random or careless responding"
    if w_score > 15: return "INVALID - Scale W indicates excessive inconsistency"
    if x_raw is not None and (x_raw < 34 or x_raw > 178): return "QUESTIONABLE - Extreme disclosure level may affect validity"
    if w_score > 10: return "QUESTIONABLE - Moderate inconsistency present"
    if v_score == 1: return "ACCEPTABLE - Minor validity concerns"
    return "VALID - Profile appears reliable and valid"

def assess_profile_validity(responses, raw_scores):
    v_score = calculate_scale_v_invalidity(responses)
    w_score = calculate_scale_w_inconsistency(responses)
    x_raw = raw_scores.get('X')
    return {
        'scale_v_raw': v_score,
        'scale_w_raw': w_score,
        'scale_x_raw': x_raw,
        'interpretations': get_validity_interpretation(v_score, w_score),
        'overall_validity': determine_overall_validity(v_score, w_score, x_raw)
    }
