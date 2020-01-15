def hsv_to_rgb(h, s, v):
    """
        Eingabe: Der Wert im HSV Farbmodell
        Ausgabe: Ein Tupel mit der in den RGB Farbmodell konvertierten Farbe
    """
    return 0, 0, 0


def rgb_to_hsv(r, g, b):
    """
        Eingabe: Der Wert im RGB Farbmodell
        Ausgabe: Ein Tupel mit der in den HSV Farbmodell konvertierten Farbe
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
