def hsv_to_rgb(h, s, v):
    """
        Eingabe: Der Wert im HSV Farbraum
        Ausgabe: Ein Tupel mit der in den RGB Farbraum konvertierten Farbe
        Ihr könnt eure Implementierung auf diesen Algorithmus basieren:
            https://de.wikipedia.org/wiki/HSV-Farbraum#Umrechnung_HSV_in_RGB
    """
    # Wenn ihr selber implementiert, dann nehmt die nächste Zeile raus, sonst passiert nichts ;)
    return h, s, v

    # s und v auf den Bereich 0 bis 1 bringen
    # Eingabewerte sind im Bereich von 0 bis 100
    # s =
    # v =

    # Bestimmung des Grundfarbenintervalls und des Werts im Intervall
    # h_i =
    # f =

    # Bestimmung der Hilfswerte
    # p =
    # q =
    # t =

    # Konstruktion des Farbkreises zur Bestimmung der Farbe im RGB Farbraum
    # farbkreis = (
    #     (v, t, p),
    #     # ...
    # )

    # Bestimmung der RGB Werte
    # rgb = farbkreis[h_i % 6]

    # Skalierung der Farbwere vom Bereich 0 bis 1 in den Bereich 0 bis 255
    # rgb =
    # return rgb


def calculate_h(r, g, b, min_value, max_value):
    pass


def rgb_to_hsv(r, g, b):
    """
        Eingabe: Der Wert im RGB Farbraum
        Ausgabe: Ein Tupel mit der in den HSV Farbraum konvertierten Farbe
        Ihr könnt eure Implementierung auf diesem Algorithmus basieren:
            https://de.wikipedia.org/wiki/HSV-Farbraum#Umrechnung_RGB_in_HSV/HSL
    """
    # Wenn ihr selber implementiert, dann nehmt die nächste Zeile raus, sonst passiert nichts ;)
    return r, g, b

    # Normalisierung
    # Wir müssen die Werte vom Bereich 0 bis 255 in den Bereich 0 bis 1 bringen
    # r =
    # g =
    # b =

    # Bestimmung des Minimal- und Maximalwerts
    # min_value =
    # max_value =

    # Berechnung von h anhand der Position im Farbkreis
    # h = calculate_h(r, g, b, min_value, max_value)

    # Berechnung von s

    # Berechnung von v
    # v =

    # Skalierung der Werte
    # h ist schon im richtigen Bereich
    # s und v von 0 bis 1 nach 0 bis 100
    # s =
    # v =
    # return int(h), int(s), int(v)


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
