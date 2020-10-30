import colorsys


def skaliere_zu_float(wert, maximaler_wert):
    return wert / maximaler_wert


def skaliere_zu_int(wert, maximaler_wert):
    return int(round(wert * maximaler_wert))


def hsv_to_rgb(h, s, v):
    """
        Eingabe: Der Wert im HSV Farbmodell (Wertebreiche: h: 0-360, s+v: 0-100)
        Ausgabe: Ein Tupel mit der in den RGB Farbmodell konvertierten Farbe (Wertebereiche: r+g+b: 0-255)
        Findet eine Bibliothek im Internet, mit der ihr die Farbkonvertierung durchführen könnt.
        Sucht doch mal bei Google ;)
    """
    r, g, b = colorsys.hsv_to_rgb(skaliere_zu_float(h, 360),
                                  skaliere_zu_float(s, 100),
                                  skaliere_zu_float(v, 100))

    return skaliere_zu_int(r, 255), skaliere_zu_int(g, 255), skaliere_zu_int(b, 255)


def rgb_to_hsv(r, g, b):
    """
        Eingabe: Der Wert im RGB Farbmodell (Wertebereiche: r+g+b: 0-255)
        Ausgabe: Ein Tupel mit der in den HSV Farbmodell konvertierten Farbe (Wertebreiche: h: 0-360, s+v: 0-100)
        Findet eine Bibliothek im Internet, mit der ihr die Farbkonvertierung durchführen könnt.
        Sucht doch mal bei Google ;)
    """
    h, s, v = colorsys.rgb_to_hsv(skaliere_zu_float(r, 255), skaliere_zu_float(g, 255), skaliere_zu_float(b, 255))
    return skaliere_zu_int(h, 360), skaliere_zu_int(s, 100), skaliere_zu_int(v, 100)


def rgb_to_hexa(r, g, b):
    r_hex = hex(r)[2:]
    if len(r_hex) == 1:
        r_hex = "0" + r_hex

    g_hex = hex(g)[2:]
    if len(g_hex) == 1:
        g_hex = "0" + g_hex

    b_hex = hex(b)[2:]
    if len(b_hex) == 1:
        b_hex = "0" + b_hex

    return "#" + r_hex + g_hex + b_hex


if __name__ == "__main__":
    # Einfache Tests

    number_hex_pairs = (
        ((0, 0, 0), "#000000"),
        ((0, 0, 255), "#0000ff"),
        ((255, 255, 255), "#ffffff"),
        ((120, 168, 17), "#78a811"),
        ((7, 6, 11), "#07060b"),
    )

    for rgb, hex_value in number_hex_pairs:
        result = rgb_to_hexa(*rgb)
        if not result == hex_value:
            print(f"Fehler: RGB={rgb} sollte in Hexadezimal '{hex_value}' sein. Stattdessen war das Ergebnis: '{result}'")


    def are_arrays_equal(a1, a2, tol=2):
        return all([abs(x - y) <= tol for x, y in zip(a1, a2)])

    rgb_hsv_pairs = (
        ((255, 0, 0), (0, 100, 100)),
        ((255, 255, 255), (0, 0, 100)),
        ((0, 0, 255), (240, 100, 100)),
        ((72, 236, 133), (142, 70, 93)),
        ((123, 200, 128), (124, 39, 78)),
        ((217, 19, 177), (312, 91, 85))
    )

    for rgb, hsv in rgb_hsv_pairs:
        test_hsv = rgb_to_hsv(*rgb)
        if not are_arrays_equal(hsv, test_hsv):
            print(f"Fehler: Für RGB={rgb} sollte HSV={hsv} herauskommen. Stattdessen war das Ergebnis: {test_hsv}")
        test_rgb = hsv_to_rgb(*hsv)
        if not are_arrays_equal(rgb, test_rgb):
            print(f"Fehler: Für HSV={hsv} sollte RGB={rgb} herauskommen. Stattdessen war das Ergebnis: {test_rgb}")
