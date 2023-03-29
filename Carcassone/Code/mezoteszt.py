def Placeable(selected_card, location, placed_cards):  # selected_card egy card class, location egy számpár [2, 3], placed_cards pedig egy lista a lerakott kártya classek helyéről
    matrix = []
    temp_row = []
    for x in range(8):
        for y in range(5):
            temp_row.append(" ")
        matrix.append(temp_row)
        temp_row = []

    if len(placed_cards) > 0:
        for card in placed_cards:
            matrix[card.pos_x][card.pos_y] = card

        # az if megvizsgálja mind a 4 oldalát a selected_cardnak
        if (location[0] - 1 < 0 or matrix[location[0] - 1][location[1]] == " " or selected_card.sides[0] == matrix[location[0] - 1][location[1]].sides[2]) and \
                (location[1] + 1 > 5 or matrix[location[0]][location[1] + 1] == " " or selected_card.sides[1] == matrix[location[0]][location[1] + 1].sides[3]) and \
                (location[0] + 1 > 8 or matrix[location[0] + 1][location[1]] == " " or selected_card.sides[2] == matrix[location[0] + 1][location[1]].sides[0]) and \
                (location[1] - 1 < 0 or matrix[location[0]][location[1] - 1] == " " or selected_card.sides[3] == matrix[location[0]][location[1] - 1].sides[1]):
            return True
        else:
            return False
    else:
        return True
