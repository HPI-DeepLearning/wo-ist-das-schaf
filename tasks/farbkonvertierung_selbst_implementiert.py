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
    if min_value == max_value:
        h = 0
    elif max_value == r:
        h = 60 * ((g - b) / (max_value - min_value))
    elif max_value == g:
        h = 60 * (2 + ((b - r) / (max_value - min_value)))
    else:
        h = 60 * (4 + ((r - g) / (max_value - min_value)))

    if h < 0:
        h = h + 360
    return h


def rgb_to_hsv(r, g, b):
    """
        Eingabe: Der Wert im RGB Farbmodell (Wertebereiche: r+g+b: 0-255)
        Ausgabe: Ein Tupel mit der in den HSV Farbmodell konvertierten Farbe (Wertebreiche: h: 0-360, s+v: 0-100)
        Ihr könnt eure Implementierung auf diesen Algorithmus basieren:
            https://de.wikipedia.org/wiki/HSV-Farbraum#Umrechnung_RGB_in_HSV/HSL
    """
    # Normalisierung
    # Wir müssen die Werte vom Bereich 0 bis 255 in den Bereich 0 bis 1 bringen
    # return 0, 0, 0
    r = r / 255
    g = g / 255
    b = b / 255

    # Bestimmung des Minimal- und Maximalwerts
    min_value = min(r, g, b)
    max_value = max(r, g, b)

    # Berechnung von h anhand der Position im Farbkreis
    h = calculate_h(r, g, b, min_value, max_value)

    # Berechnung von s
    if max_value == 0:
        s = 0
    else:
        s = (max_value - min_value) / max_value

    # Berechnung von v
    v = max_value

    # Skalierung der Werte
    # h ist schon im richtigen Bereich
    # s und v von 0 bis nach 0 bis 100
    s = s * 100
    v = v * 100
    return int(h), int(s), int(v)


if __name__ == "__main__":
    # Einfache Tests
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