from mpmath import mp
import re
from datetime import datetime

def finde_geburtsdatum_in_pi(geburtsdatum, geburtszeit=None, max_stellen=1_000_000):
    """
    Sucht ein Geburtsdatum (und optional Geburtszeit) in den Nachkommastellen von Pi.
    
    Parameter:
    - geburtsdatum (str): Datum im Format DD.MM.YYYY (z.B. "15.03.1990")
    - geburtszeit (str, optional): Zeit im Format HH.MM (z.B. "14.30")
    - max_stellen (int): Maximale Anzahl der Pi-Nachkommastellen zum Durchsuchen
    
    Rückgabe:
    - Dictionary mit Position und verschiedenen Veranschaulichungen
    """
    
    # Validierung des Datums
    try:
        datum_obj = datetime.strptime(geburtsdatum, "%d.%m.%Y")
    except ValueError:
        return {"fehler": "Ungültiges Datumsformat. Bitte DD.MM.YYYY verwenden."}
    
    # Suchstring erstellen (ohne Punkte)
    suchstring = geburtsdatum.replace(".", "")
    
    if geburtszeit:
        # Validierung der Zeit
        if not re.match(r'^\d{2}\.\d{2}$', geburtszeit):
            return {"fehler": "Ungültiges Zeitformat. Bitte HH.MM verwenden."}
        suchstring += geburtszeit.replace(".", "")
    
    # Pi mit den gewünschten Nachkommastellen berechnen
    mp.dps = max_stellen + 100  # etwas mehr für Genauigkeit
    pi_str = str(mp.pi)
    
    # Nur die Nachkommastellen (nach dem Punkt)
    nachkommastellen = pi_str.split('.')[1]
    
    # Suche nach dem String
    position = nachkommastellen.find(suchstring)
    
    if position == -1:
        return {
            "gefunden": False,
            "suchstring": suchstring,
            "nachricht": f"Die Zahlenfolge '{suchstring}' wurde in den ersten {max_stellen} Nachkommastellen von Pi nicht gefunden.",
            "tipp": "Versuche es mit mehr Nachkommastellen (erhöhe max_stellen)."
        }
    
    # Ergebnisse zusammenstellen
    ergebnis = {
        "gefunden": True,
        "suchstring": suchstring,
        "position": position,
        "laenge": len(suchstring)
    }
    
    # Verschiedene Veranschaulichungen
    
    # 1. Zeit zum Schreiben
    sekunden_pro_ziffer = 2  # Annahme: 2 Sekunden pro Ziffer schreiben
    zeit_sekunden = position * sekunden_pro_ziffer
    stunden = zeit_sekunden // 3600
    minuten = (zeit_sekunden % 3600) // 60
    
    ergebnis["schreib_dauer"] = (
        f"Wenn du eine Ziffer pro {sekunden_pro_ziffer} Sekunden schreibst, würdest du "
        f"{stunden:.0f} Stunden und {minuten:.0f} Minuten brauchen, um bis zu deinem Geburtsdatum zu kommen."
    )
    
    # 2. Buchseiten (50 Zeilen à 80 Zeichen pro Seite)
    ziffern_pro_seite = 50 * 80
    seite = position // ziffern_pro_seite + 1
    zeile = (position % ziffern_pro_seite) // 80 + 1
    
    ergebnis["buch_position"] = (
        f"In einem Buch mit 80 Zeichen pro Zeile und 50 Zeilen pro Seite würdest du "
        f"dein Geburtsdatum auf Seite {seite}, Zeile {zeile} finden."
    )
    
    # 3. Wanderung
    meter_pro_ziffer = 0.003  # 3mm pro Ziffer
    strecke_meter = position * meter_pro_ziffer
    strecke_km = strecke_meter / 1000
    
    if strecke_km < 1:
        ergebnis["wanderung"] = (
            f"Wenn jede Ziffer 3mm groß wäre, müsstest du {strecke_meter:.1f} Meter laufen "
            f"(etwa {strecke_meter/1.5:.0f} Schritte)."
        )
    else:
        ergebnis["wanderung"] = (
            f"Wenn jede Ziffer 3mm groß wäre, müsstest du {strecke_km:.2f} km laufen "
            f"(etwa {strecke_km/5:.1f} Stunden Fußweg)."
        )
    
    # 4. Kontext anzeigen (die gefundene Stelle in Pi)
    start = max(0, position - 10)
    ende = min(len(nachkommastellen), position + len(suchstring) + 10)
    kontext = nachkommastellen[start:ende]
    
    # Markiere die gefundene Stelle
    markierung_start = position - start
    markierung_ende = markierung_start + len(suchstring)
    kontext_markiert = (
        kontext[:markierung_start] + 
        f"[{kontext[markierung_start:markierung_ende]}]" + 
        kontext[markierung_ende:]
    )
    
    ergebnis["kontext"] = f"...{kontext_markiert}..."
    ergebnis["pi_position"] = f"3,{nachkommastellen[:position]}[{suchstring}]..."
    
    return ergebnis


# Beispielnutzung
if __name__ == "__main__":
    print("=" * 70)
    print("PI GEBURTSDATUM FINDER")
    print("=" * 70)
    
    # Beispiel 1: Nur Datum
    print("\n📅 Beispiel 1: Nur Geburtsdatum. Gib dein Geburtsdatum im Format DD.MM.YYY ein:")
    print("\n")
    message = input("Gib dein Geburtsdatum im Format DD.MM.YYY ein:")
    ergebnis1 = finde_geburtsdatum_in_pi(message)
    
    if ergebnis1.get("gefunden"):
        print(f"\n✅ Gefunden! Deine Zahlenfolge: {ergebnis1['suchstring']}")
        print(f"📍 Position: An Stelle {ergebnis1['position']} nach dem Komma")
        print(f"\n🔍 In Pi: {ergebnis1['kontext']}")
        print(f"\n⏱️  {ergebnis1['schreib_dauer']}")
        print(f"\n📖 {ergebnis1['buch_position']}")
        print(f"\n🚶 {ergebnis1['wanderung']}")
    else:
        print(f"\n❌ {ergebnis1['nachricht']}")
    
    # Beispiel 2: Datum und Zeit
    print("\n" + "=" * 70)
    print("\n📅 Beispiel 2: Geburtsdatum mit Uhrzeit")
    ergebnis2 = finde_geburtsdatum_in_pi("01.01.2000", "12.30")
    
    if ergebnis2.get("gefunden"):
        print(f"\n✅ Gefunden! Deine Zahlenfolge: {ergebnis2['suchstring']}")
        print(f"📍 Position: An Stelle {ergebnis2['position']} nach dem Komma")
        print(f"\n🔍 In Pi: {ergebnis2['kontext']}")
        print(f"\n⏱️  {ergebnis2['schreib_dauer']}")
        print(f"\n📖 {ergebnis2['buch_position']}")
        print(f"\n🚶 {ergebnis2['wanderung']}")
    else:
        print(f"\n❌ {ergebnis2['nachricht']}")
    
    print("\n" + "=" * 70)
    print("\n💡 Probiere es mit deinem eigenen Geburtsdatum!")
    print("   Beispiel: finde_geburtsdatum_in_pi('19.12.1995', '15.56')")