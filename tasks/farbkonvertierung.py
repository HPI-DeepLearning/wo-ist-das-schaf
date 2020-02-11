def hsv_to_rgb(h, s, v):
    """
        Eingabe: Der Wert im HSV Farbmodell (Wertebreiche: h: 0-360, s+v: 0-100)
        Ausgabe: Ein Tupel mit der in den RGB Farbmodell konvertierten Farbe (Wertebereiche: r+g+b: 0-255)
        Findet eine Bibliothek im Internet, mit der ihr die Farbkonvertierung durchführen könnt.
        Sucht doch mal bei Google ;)
    """
    return 0, 0, 0


def rgb_to_hsv(r, g, b):
    """
        Eingabe: Der Wert im RGB Farbmodell (Wertebereiche: r+g+b: 0-255)
        Ausgabe: Ein Tupel mit der in den HSV Farbmodell konvertierten Farbe (Wertebreiche: h: 0-360, s+v: 0-100)
        Findet eine Bibliothek im Internet, mit der ihr die Farbkonvertierung durchführen könnt.
        Sucht doch mal bei Google ;)
    """
    return 0, 0, 0


def rgb_to_hexa(r, g, b):
    """
        Eingabe: Der Wert im RGB Farbraum
        Ausgabe: Ein String mit der aktuellen Farbe als Hexadezimale Zahl
        Beispiel:
            Schwarz hat den Wert (0, 0, 0) in RGB, also wäre die Ausgabe #000000
            Weiß hat den Wert (255, 255, 255) in RGB, also wäre die Ausgabe #ffffff

        Hilfe: https://www.programiz.com/python-programming/methods/built-in/hex
    """
    return "#000000"


if __name__ == "__main__":
    # Einfache Tests

    number_hex_pairs = (
        ((0, 0, 0), "#000000"),
        ((0, 0, 255), "#0000ff"),
        ((255, 255, 255), "#ffffff"),
        ((120, 168, 17), "#78a811"),
        ((7, 6, 11), "#07060b"),
    )

    for rgb, hex in number_hex_pairs:
        result = rgb_to_hexa(*rgb)
        if not result == hex:
            print(f"Fehler: RGB={rgb} sollte in Hexadezimal '{hex}' sein. Stattdessen war das Ergebnis: '{result}'")


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
