def Score(cards):
    varos = VarosPont(cards)
    ut = UtPont(cards)
    kolostor = KolostorPont(cards)
    befejezett_tabla = 10 if len(cards) == 40 else 0

    print(f"\nVáros pont: {varos}\nÚt pont: {ut}\nKolostor pont: {kolostor}\nBefejezett pálya pont: {befejezett_tabla}\n-----------------\nÖsszesen: {varos+ut+kolostor+befejezett_tabla}")

    print("\n\
A városok értéke annyiszor 2 pont, ahány kártyából áll.                  X\n\
Egy befejezett városért plusz 5 pont jár.                                X\n\
Az utak értéke annyiszor 1 pont, ahány kártyából áll.                    ✓\n\
Egy befejezett útért plusz 2 pont jár.                                   ✓\n\
A kolostor kártya annyi pontot ér, ahány szomszédja van (max. 8).        ✓\n\
Ha a játék úgy ért véget, hogy betelt a játéklap, akkor plusz 10 pont.   ✓")

    return varos+ut+kolostor+befejezett_tabla

def VarosPont(cards):
    megvizsgalt, vizsgalandok, befejezett = [], [], 0

    for kartya in cards:
        if 'v' in kartya.sides:
            vizsgalandok.append(kartya)
            befejezett += 1

            while len(vizsgalandok) > 0:
                vizsgalando = vizsgalandok.pop(0)

                if vizsgalando not in megvizsgalt:

                    megvizsgalt.append(vizsgalando)

                    szomszedok, befejezett = VarosSzomszedok(cards, vizsgalando.pos, befejezett)
                    for card in szomszedok:
                        if card not in megvizsgalt:
                            vizsgalandok.append(card)

    return len(megvizsgalt)*2 + befejezett * 5

def VarosSzomszedok(cards, pos, befejezett):
    szomszedok, temp = [], []

    temp = list(filter(lambda x: x.pos == (pos[0]-1, pos[1]) and x.sides[1] == 'v', cards))
    if len(temp) > 0: szomszedok.append(temp[0])

    temp = list(filter(lambda x: x.pos == (pos[0], pos[1]-1) and x.sides[2] == 'v', cards))
    if len(temp) > 0: szomszedok.append(temp[0])

    temp = list(filter(lambda x: x.pos == (pos[0]+1, pos[1]) and x.sides[3] == 'v', cards))
    if len(temp) > 0: szomszedok.append(temp[0])

    temp = list(filter(lambda x: x.pos == (pos[0], pos[1]+1) and x.sides[0] == 'v', cards))
    if len(temp) > 0: szomszedok.append(temp[0])

    return szomszedok, befejezett


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
    megvizsgalt, befejezett_lista = [], []

    for kartya in cards:
        if kartya.sides.count('u') > 2 or ('u' in kartya.sides and kartya.sides[4] in ['v', 'k', 'c']):
            for sorrend in [[1, 2, 4, 3], [2, 3, 1, 4], [3, 4, 2, 1], [4, 3, 2, 1]]:
                befejezett_lista = Bejar(kartya, befejezett_lista, cards, sorrend)

    utak = len(list(filter(lambda x: 'u' in x.sides, cards)))
    lezart_utak = len([pos for sublist in befejezett_lista for pos in sublist])

    return utak + lezart_utak * 2

def UtSzomszedok(cards, pos, sorrend):
    szomszedok, temp = [], []

    for i in sorrend:
        if i == 1:
            temp = list(filter(lambda x: x.pos == (pos[0] - 1, pos[1]) and x.sides[1] == 'u', cards))
            if len(temp) > 0: szomszedok.append(temp[0])
        elif i == 2:
            temp = list(filter(lambda x: x.pos == (pos[0], pos[1] - 1) and x.sides[2] == 'u', cards))
            if len(temp) > 0: szomszedok.append(temp[0])
        elif i == 3:
            temp = list(filter(lambda x: x.pos == (pos[0] + 1, pos[1]) and x.sides[3] == 'u', cards))
            if len(temp) > 0: szomszedok.append(temp[0])
        elif i == 4:
            temp = list(filter(lambda x: x.pos == (pos[0], pos[1] + 1) and x.sides[0] == 'u', cards))
            if len(temp) > 0: szomszedok.append(temp[0])

    return szomszedok

def BenneVan(megvizsgalt, befejezett_lista):

    if any(all(pos in megvizsgalt for pos in sublist) for sublist in befejezett_lista):
        pass
    elif not any(all(pos in sublist for pos in megvizsgalt) for sublist in befejezett_lista):
        befejezett_lista.append(megvizsgalt)

    return befejezett_lista

def Bejar(kartya, befejezett_lista, cards, sorrend):
    vizsgalandok, megvizsgalt = [kartya], []

    while len(vizsgalandok) > 0:
        vizsgalando = vizsgalandok.pop()

        if vizsgalando not in megvizsgalt:

            megvizsgalt.append(vizsgalando)

            if vizsgalando != kartya and (vizsgalando.sides.count('u') > 2 or ('u' in vizsgalando.sides and vizsgalando.sides[4] in ['v', 'k', 'c'])):
                befejezett_lista = BenneVan(megvizsgalt, befejezett_lista)
                break

            for card in UtSzomszedok(cards, vizsgalando.pos, sorrend):
                if card not in megvizsgalt:
                    vizsgalandok.append(card)

    return befejezett_lista
