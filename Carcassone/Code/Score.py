from itertools import permutations

SORRENDEK = list(permutations([0, 1, 2, 3], 4))

def Score(cards):
    varos = VarosPont(cards)
    ut = UtPont(cards)
    kolostor = KolostorPont(cards)
    befejezett_tabla = 10 if len(cards) == 40 else 0

    return varos + ut + kolostor + befejezett_tabla


def VarosPont(cards):
    varos_lista, varos_reszek = [], 0

    for kartya in cards:
        if 'v' in kartya.sides:
            if kartya.sides[-1] in ['v', 'c']:
                varos_lista = VarosBejar(kartya, varos_lista, cards)
                varos_reszek += 1
            else:
                for index in range(4):
                    if kartya.sides[index] == 'v':
                        varos_lista = VarosBejar(kartya, varos_lista, cards, index)
                        varos_reszek += 1

    return varos_reszek * 2 + len([pos for sublist in Ellenorzes(varos_lista) for pos in sublist]) * 5

def VarosBejar(kartya, varos_lista, cards, kezdo_irany = None):
    megvizsgalt, vizsgalandok = [], [kartya]

    while len(vizsgalandok) > 0:
        vizsgalando = vizsgalandok.pop(0)

        if vizsgalando not in megvizsgalt:

            megvizsgalt.append(vizsgalando)

            szomszedok, kezdo_irany = VarosSzomszedok(cards, vizsgalando.pos, kezdo_irany)
            for card in szomszedok:
                if card not in megvizsgalt:
                    vizsgalandok.append(card)

    if len(megvizsgalt) == 1 or not any(all(pos in megvizsgalt for pos in sublist) for sublist in varos_lista):
        varos_lista.append(megvizsgalt)

    return varos_lista

def VarosSzomszedok(cards, pos, irany):
    szomszedok = []

    if irany == None:
        temp = list(filter(lambda x: x.pos == (pos[0], pos[1] - 1) and x.sides[2] == 'v', cards))
        if len(temp) > 0: szomszedok.append(temp[0])

        temp = list(filter(lambda x: x.pos == (pos[0] + 1, pos[1]) and x.sides[3] == 'v', cards))
        if len(temp) > 0: szomszedok.append(temp[0])

        temp = list(filter(lambda x: x.pos == (pos[0], pos[1] + 1) and x.sides[0] == 'v', cards))
        if len(temp) > 0: szomszedok.append(temp[0])

        temp = list(filter(lambda x: x.pos == (pos[0] - 1, pos[1]) and x.sides[1] == 'v', cards))
        if len(temp) > 0: szomszedok.append(temp[0])

    elif irany == 0:
        temp = list(filter(lambda x: x.pos == (pos[0], pos[1] - 1) and x.sides[2] == 'v', cards))
        if len(temp) > 0: szomszedok.append(temp[0])

    elif irany == 1:
        temp = list(filter(lambda x: x.pos == (pos[0] + 1, pos[1]) and x.sides[3] == 'v', cards))
        if len(temp) > 0: szomszedok.append(temp[0])

    elif irany == 2:
        temp = list(filter(lambda x: x.pos == (pos[0], pos[1] + 1) and x.sides[0] == 'v', cards))
        if len(temp) > 0: szomszedok.append(temp[0])

    elif irany == 3:
        temp = list(filter(lambda x: x.pos == (pos[0] - 1, pos[1]) and x.sides[1] == 'v', cards))
        if len(temp) > 0: szomszedok.append(temp[0])

    if len(szomszedok) > 0 and szomszedok[0].sides[-1] not in ['v', 'c']:
        irany = -1
    else:
        irany = None

    return szomszedok, irany

def Ellenorzes(varos_lista):
    rossz_varos_indexek= []
    varos_koord_lista = [kartya.pos for varos in varos_lista for kartya in varos]

    for index, varos in enumerate(varos_lista):

        for kartya in varos:
            if len(varos) == 1:
                rossz_varos_indexek.append(index)
                break

            if kartya.sides[0] == 'v' and (kartya.pos_x, kartya.pos_y-1) not in varos_koord_lista:
                rossz_varos_indexek.append(index)
                break

            if kartya.sides[1] == 'v' and (kartya.pos_x+1, kartya.pos_y) not in varos_koord_lista:
                rossz_varos_indexek.append(index)
                break

            if kartya.sides[2] == 'v' and (kartya.pos_x, kartya.pos_y+1) not in varos_koord_lista:
                rossz_varos_indexek.append(index)
                break

            if kartya.sides[3] == 'v' and (kartya.pos_x-1, kartya.pos_y) not in varos_koord_lista:
                rossz_varos_indexek.append(index)
                break

    return [varos_lista[index] for index in range(len(varos_lista)) if index not in rossz_varos_indexek]


def KolostorPont(cards):
    pont = 0

    for kartya in cards:
        if kartya.sides[4] == 'k':

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j == 0: continue
                    if len(list(filter(lambda x: x.pos == (kartya.pos[0]+j, kartya.pos[1]+i), cards))) > 0:
                        pont += 1

    return pont


def UtPont(cards):
    befejezett_lista = []

    for kartya in cards:
        if kartya.sides.count('u') > 2 or ('u' in kartya.sides and kartya.sides[4] in ['v', 'k', 'c']):
            for sorrend in SORRENDEK:
                befejezett_lista = UtBejar(kartya, befejezett_lista, cards, sorrend)

    utak = len(list(filter(lambda x: 'u' in x.sides, cards)))
    lezart_utak = len([pos for sublist in befejezett_lista for pos in sublist])

    return utak + lezart_utak * 2

def UtBejar(kartya, befejezett_lista, cards, sorrend):
    vizsgalandok, megvizsgalt = [kartya], []

    while len(vizsgalandok) > 0:
        vizsgalando = vizsgalandok.pop()

        if vizsgalando not in megvizsgalt:

            megvizsgalt.append(vizsgalando)

            if vizsgalando != kartya and (vizsgalando.sides.count('u') > 2 or ('u' in vizsgalando.sides and vizsgalando.sides[4] in ['v', 'k', 'c'])):

                if any(all(pos in megvizsgalt for pos in sublist) for sublist in befejezett_lista):
                    pass
                elif not any(all(pos in sublist for pos in megvizsgalt) for sublist in befejezett_lista):
                    befejezett_lista.append(megvizsgalt)
                break

            for card in UtSzomszedok(cards, vizsgalando.pos, sorrend):
                if card not in megvizsgalt:
                    vizsgalandok.append(card)

    return befejezett_lista

def UtSzomszedok(cards, pos, sorrend):
    szomszedok = []

    for i in sorrend:
        if i == 0:
            temp = list(filter(lambda x: x.pos == (pos[0]-1, pos[1]) and x.sides[1] == 'u', cards))
        elif i == 1:
            temp = list(filter(lambda x: x.pos == (pos[0], pos[1]-1) and x.sides[2] == 'u', cards))
        elif i == 2:
            temp = list(filter(lambda x: x.pos == (pos[0]+1, pos[1]) and x.sides[3] == 'u', cards))
        elif i == 3:
            temp = list(filter(lambda x: x.pos == (pos[0], pos[1]+1) and x.sides[0] == 'u', cards))
        if len(temp) > 0:
            szomszedok.append(temp[0])

    return szomszedok
