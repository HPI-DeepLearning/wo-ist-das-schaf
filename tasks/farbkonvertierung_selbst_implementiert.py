def hsv_to_rgb(h, s, v):
    """
        Eingabe: Der Wert im HSV Farbmodell (Wertebreiche: h: 0-360, s+v: 0-100)
        Ausgabe: Ein Tupel mit der in den RGB Farbmodell konvertierten Farbe (Wertebereiche: r+g+b: 0-255)
        Ihr könnt eure Implementierung auf diesen Algorithmus basieren:
            https://de.wikipedia.org/wiki/HSV-Farbraum#Umrechnung_HSV_in_RGB
    """
    # s und v auf den Bereich 0 bis 1 bringen
    # Eingabewerte sind im Bereich von 0 bis 100
    s = s / 100
    v = v / 100

    # Bestimmung des Grundfarbenintervalls und des Werts im Intervall
    h_i = int(h // 60)
    f = (h / 60 - h_i)

    # Bestimmung der Hilfswerte
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))

    # Konstruktion des Farbkreises zur Bestimmung der Farbe im RGB Farbraum
    farbkreis = (
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    )

    # Bestimmung der RGB Werte
    rgb = farbkreis[h_i % 6]

    # Skalierung der Farbwere vom Bereich 0 bis 1 in den Bereich 0 bis 255
    rgb = tuple(int(k * 255) for k in rgb)
    return rgb


def calculate_h(r, g, b, min_value, max_value):
    # Hilfsfunktion für die RGB nach HSV Berechnung
    return 0


def rgb_to_hsv(r, g, b):
    """
        Eingabe: Der Wert im RGB Farbmodell (Wertebereiche: r+g+b: 0-255)
        Ausgabe: Ein Tupel mit der in den HSV Farbmodell konvertierten Farbe (Wertebreiche: h: 0-360, s+v: 0-100)
        Ihr könnt eure Implementierung auf diesen Algorithmus basieren:
            https://de.wikipedia.org/wiki/HSV-Farbraum#Umrechnung_RGB_in_HSV/HSL
    """
    # Normalisierung
    # Wir müssen die Werte vom Bereich 0 bis 255 in den Bereich 0 bis 1 bringen

    # Bestimmung des Minimal- und Maximalwerts

    # Berechnung von h anhand der Position im Farbkreis

    # Berechnung von s

    # Berechnung von v

    # Skalierung der Werte
    # h ist schon im richtigen Bereich
    # s und v von 0 bis nach 0 bis 100
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

    def assert_arrays_equal(a1, a2, tol=2):
        assert all([abs(x - y) <= tol for x, y in zip(a1, a2)]), "{} != {}".format(a1, a2)

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
        assert_arrays_equal(hsv, test_hsv)
        test_rgb = hsv_to_rgb(*hsv)
        assert_arrays_equal(rgb, test_rgb)
