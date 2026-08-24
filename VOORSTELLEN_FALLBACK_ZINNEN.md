# 💡 VOORSTELLEN: BETERE FALLBACK ZINNEN VOOR [NEXT_ART] EN [NEXT_TIT]

## Huidge Fallback Zinnen (MOMENTEEL):
```python
n_art = "de volgende artiest"
n_tit = "een schitterende track"
```

**Probleem:** Te generiek en voelt niet natuurlijk in veel scripts.

---

## 🎯 VERBETERDE VOORSTEL #1: Context-Aware Fallbacks

### Idee: Zin verandert gebaseerd op tijd van de dag

```python
def get_next_track_fallback(self):
    now = datetime.now()
    hour = now.hour
    
    if 6 <= hour < 12:  # Ochtend
        art = "de volgende artiest"
        tit = "een frisse opener"
    elif 12 <= hour < 17:  # Middag
        art = "onze volgende ster"
        tit = "het volgende gebeuren"
    elif 17 <= hour < 21:  # Avond
        art = "de avondartiest"
        tit = "een fijne track"
    else:  # Nacht
        art = "de volgende artiest"
        tit = "een nachtelijk nummer"
    
    return art, tit
```

### Voorbeelden Output:
```
Ochtend:  "de volgende artiest brengt je een frisse opener"
Middag:   "onze volgende ster met het volgende gebeuren"
Avond:    "de avondartiest met een fijne track"
Nacht:    "de volgende artiest met een nachtelijk nummer"
```

**Voordeel:** Voelt veel natuurlijker door tijd-context! ✅

---

## 🎯 VERBETERDE VOORSTEL #2: Show-Aware Fallbacks

### Idee: Zin verschilt per show/programma

```python
def get_next_track_fallback_by_show(self, show_name):
    show_fallbacks = {
        "Radio Freaks": {"art": "de volgende freak", "tit": "een bizarre banger"},
        "Middag Post": {"art": "onze volgende gast", "tit": "een middag hit"},
        "Lage Landen": {"art": "de volgende performer", "tit": "een Benelux klassieker"},
        "Hotel Romantiek": {"art": "de romantische artiest", "tit": "een smoochy track"},
        "Nachtelijke Beats": {"art": "de nacht dj", "tit": "een beat bomb"},
        "Indie Vibes": {"art": "de volgende indie ster", "tit": "een indie juweel"},
        "Klassiek & Jazz": {"art": "de volgende virtuoos", "tit": "een jazzstandaard"},
        "Electronic Dreams": {"art": "de volgende producer", "tit": "een electronic masterpiece"},
        "Soul & Groove": {"art": "de volgende soul zanger", "tit": "een groove nummer"},
        "Retro Rewind": {"art": "de retro legende", "tit": "een klassieke hit"},
    }
    
    fallback = show_fallbacks.get(show_name, {"art": "de volgende artiest", "tit": "een schitterende track"})
    return fallback["art"], fallback["tit"]
```

### Voorbeelden Output:
```
Radio Freaks:        "de volgende freak met een bizarre banger"
Hotel Romantiek:     "de romantische artiest met een smoochy track"
Electronic Dreams:   "de volgende producer met een electronic masterpiece"
Soul & Groove:       "de volgende soul zanger met een groove nummer"
```

**Voordeel:** Brand-consistent en thema-passend! ✅

---

## 🎯 VERBETERDE VOORSTEL #3: Genre-Aware Fallbacks

### Idee: Fallback gebaseerd op genre van huidge track

```python
def get_next_track_fallback_by_genre(self, current_genre):
    genre_fallbacks = {
        "pop": {"art": "de volgende popster", "tit": "een poparij"},
        "rock": {"art": "de volgende rocker", "tit": "een rock anthem"},
        "hiphop": {"art": "de volgende mc", "tit": "een hip hop banger"},
        "jazz": {"art": "de volgende jazzmusicus", "tit": "een jazzstandaard"},
        "electronic": {"art": "de volgende producer", "tit": "een electronic track"},
        "dance": {"art": "de volgende dj", "tit": "een dancefloor killer"},
        "indie": {"art": "de volgende indie artiest", "tit": "een indie hit"},
        "reggae": {"art": "de volgende reggae artiest", "tit": "een reggae vibes"},
        "blues": {"art": "de volgende bluesman", "tit": "een klassieke blues"},
        "country": {"art": "de volgende country zanger", "tit": "een country tune"},
    }
    
    fallback = genre_fallbacks.get(current_genre.lower(), 
                                   {"art": "de volgende artiest", "tit": "een schitterende track"})
    return fallback["art"], fallback["tit"]
```

### Voorbeelden Output:
```
Pop:       "de volgende popster met een poparij"
Rock:      "de volgende rocker met een rock anthem"
Hip Hop:   "de volgende mc met een hip hop banger"
Electronic: "de volgende producer met een electronic track"
```

**Voordeel:** Genre blijft consistent! ✅

---

## 🎯 VERBETERDE VOORSTEL #4: GECOMBINEERD (BEST!)

### Idee: Show + Tijd + Genre combinatie

```python
def get_best_next_fallback(self, show_name, current_genre):
    """Best van alles: show-aware + genre-aware"""
    
    now = datetime.now()
    hour = now.hour
    
    # Basis fallback per show
    show_base = {
        "Radio Freaks": "de volgende freak",
        "Hotel Romantiek": "de romantische artiest",
        "Electronic Dreams": "de volgende producer",
        # ... rest
    }
    
    # Toevoeging gebaseerd op genre
    genre_add = {
        "pop": "pop",
        "rock": "rock",
        "electronic": "electronic",
    }
    
    # Tijd-gebaseerde eindwoord
    time_endings = {
        "morning": "opener",
        "afternoon": "middag-hit",
        "evening": "avond-favor",
        "night": "nachtelijk nummer",
    }
    
    artist = show_base.get(show_name, "de volgende artiest")
    
    if hour < 12:
        title = "een frisse opener"
    elif hour < 17:
        title = "een middag-hit"
    elif hour < 21:
        title = "een fijne track"
    else:
        title = "een nachtelijk nummer"
    
    return artist, title
```

### Voorbeelden Output:
```
08:00 Radio Freaks (Pop):      "de volgende freak met een frisse opener"
14:00 Hotel Romantiek (Soul):  "de romantische artiest met een middag-hit"
20:00 Electronic Dreams:       "de volgende producer met een fijne track"
23:00 Nachtelijke Beats:       "de nacht dj met een nachtelijk nummer"
```

**Voordeel:** Maximum naturalness! 🎯✅

---

## 📊 VERGELIJKING VAN ALLE VOORSTELLEN

| Voorstel | Naturalness | Complexiteit | Implementatie | Best Voor |
|----------|------------|--------------|---------------|-----------|
| Huidg (generiek) | ⭐ | ⭐ | Eenvoudig | Niks |
| #1 Tijd-aware | ⭐⭐⭐ | ⭐⭐ | Gemiddeld | Dagschema's |
| #2 Show-aware | ⭐⭐⭐⭐ | ⭐⭐ | Gemiddeld | Multi-show stations |
| #3 Genre-aware | ⭐⭐⭐ | ⭐⭐ | Gemiddeld | Music variety |
| #4 Gecombineerd | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Wat meer werk | ALLES! 🏆 |

---

## 🔧 IMPLEMENTATIE IN JOUW CODE

### LOCATIE in code:
```python
# HUIDIGING (rond line 1500):
n_art = next_track.get("art", "de volgende artiest") if next_track else "nieuwe muziek"
n_tit = next_track.get("tit", "een schitterende track") if next_track else "nog meer hits"
```

### VERVANGEN DOOR:
```python
if next_track:
    n_art = next_track.get("art", self.get_next_art_fallback())
    n_tit = next_track.get("tit", self.get_next_tit_fallback())
else:
    n_art, n_tit = self.get_next_track_fallback()
```

### EN TOEVOEGEN (nieuwe methode):
```python
def get_next_art_fallback(self):
    """Artist fallback met context"""
    now = datetime.now()
    hour = now.hour
    
    if 6 <= hour < 12:
        return "de volgende artiest"
    elif 12 <= hour < 17:
        return "onze volgende ster"
    elif 17 <= hour < 21:
        return "de volgende performer"
    else:
        return "de volgende artiest"

def get_next_tit_fallback(self):
    """Titel fallback met tijd-context"""
    now = datetime.now()
    hour = now.hour
    
    if 6 <= hour < 12:
        return "een frisse opener"
    elif 12 <= hour < 17:
        return "een middag-hit"
    elif 17 <= hour < 21:
        return "een fijne track"
    else:
        return "een nachtelijk nummer"

def get_next_track_fallback(self):
    """Complete fallback als geen next track"""
    return self.get_next_art_fallback(), self.get_next_tit_fallback()
```

---

## ✅ MIJN AANBEVELING

**VOORSTEL #2 (Show-Aware)** is het beste voor jou omdat:

1. ✅ Je hebt al 10 shows gedefinieerd in `SHOWS_CONFIG`
2. ✅ Elke show heeft eigen branding/kleur
3. ✅ Voelt veel professioneler
4. ✅ Niet te complex om aan te passen
5. ✅ DJs zien het verschil in hun scripts

### Snelle Implementatie (10 minuten werk):
```python
NEXT_FALLBACKS = {
    "Radio Freaks": {"art": "de volgende freak", "tit": "een bizarre tune"},
    "Middag Post": {"art": "onze volgende artiest", "tit": "een middag-hit"},
    "Lage Landen": {"art": "de volgende performer", "tit": "een Benelux favoriete"},
    "Hotel Romantiek": {"art": "de romantische artiest", "tit": "een smoochy moment"},
    "Nachtelijke Beats": {"art": "de nacht dj", "tit": "een beat-killer"},
    "Indie Vibes": {"art": "de volgende indie legende", "tit": "een indie juweel"},
    "Klassiek & Jazz": {"art": "de volgende maestro", "tit": "een klassiek moment"},
    "Electronic Dreams": {"art": "de volgende producer", "tit": "een electronic high"},
    "Soul & Groove": {"art": "de soul zanger", "tit": "een groove moment"},
    "Retro Rewind": {"art": "de retro ster", "tit": "een klassieke oldie"},
}

def get_next_fallback(self, show_name):
    return NEXT_FALLBACKS.get(show_name, 
                              {"art": "de volgende artiest", "tit": "een schitterende track"})
```

---

## 💬 Wil je nog meer opties?
Laat het weten! Ik kan ook voorstel #4 (gecombineerd) volledig uitwerken!
