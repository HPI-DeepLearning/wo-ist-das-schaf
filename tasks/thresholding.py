import numpy as np


def threshold(image, min_values, max_values):
    """
        Berechne den Threshold eines Bildes, welches aus aus drei Kanälen besteht.
        Wir arbeiten hier mit den Kanälen Hue, Saturatio und Value.

        Shape des Bildes: [höhe, breite, Anzahl der Kanäle]
        min_values: Array mit jeweils einer Zahl für den Minimalwert pro Farbkanal
        max_values: Array mit jeweils einer Zahl für den Maximalwert pro Farbkanal

        Rückgabe:
        Ein Array, wo jeder Pixel den Wert 0 oder 1 hat.
        Ein Pixel bekommt den Wert 1, wenn der Wert in allen Kanälen zwischen dem minimum und dem maximum liegt, ansonsten wird er 0.
        Beispiel: Wir haben ein Bild mit zwei Pixeln und folgende Werte für Minimal- und Maximalwert:
        image: [[100, 150, 80], [0, 20, 100]]
        min_values: [40, 10, 50]
        max_values: [110, 200, 120]

        Ausgabe der Funktion: [1, 0].

        Wir geben also ein Bild mit nur einem Kanal zurück!
    """
    return image
