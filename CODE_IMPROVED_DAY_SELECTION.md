# 📅 VERBETERDE DAGKEUZE - ZONDER BLANCO, MET CHECKBOXES

## 🎯 VERANDERINGEN

**Voor:**
- Dropdown met: "Blanco", "ma", "di", "wo", etc.
- Werkt niet echt (Blanco is onduidelijk)

**Na:**
- Checkbox list met alle 7 dagen
- Prompts alleen voor AANGEVINKTE dagen
- Veel duidelijker en flexibeler

---

## 📍 STAP 1: Vervang deze constanten

**ZOEK (ongeveer line 70):**
```python
DAG_VERKORT_OPTIES = ["Blanco", "ma", "di", "wo", "do", "vr", "za", "zo"]
```

**VERVANG DOOR:**
```python
DAGEN_VAN_WEEK = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
DAGEN_AFKORT = ["ma", "di", "wo", "do", "vr", "za", "zo"]
```

---

## 📍 STAP 2: Voeg deze code toe in `__init__` (rond line 300)

**ZOEK:**
```python
self.show_filters = {show: tk.BooleanVar(value=False) for show in SHOWS_CONFIG.keys()}
self.show_buttons = {}
```

**VOEG ERBIJ TOE:**
```python
# Dag filters - checkboxes
self.dag_filters = {dag: tk.BooleanVar(value=False) for dag in DAGEN_VAN_WEEK}
self.dag_buttons = {}
```

---

## 📍 STAP 3: UI Verandering - Vervang de Dag Combobox

**ZOEK (in `setup_ui` methode, ongeveer line 2550):**
```python
ctk.CTkLabel(self.frame_inputs, text=t("broadcast_day", self.language)).grid(row=3, column=0, padx=10, pady=4,
                                                                             sticky="e")
self.cmb_day = ctk.CTkComboBox(self.frame_inputs, values=DAG_VERKORT_OPTIES)
self.cmb_day.grid(row=3, column=1, padx=10, pady=4, sticky="ew")
```

**VERVANG DOOR:**
```python
ctk.CTkLabel(self.frame_inputs, text=t("broadcast_day", self.language), font=("Helvetica", 10, "bold")).grid(
    row=3, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

# Dag checkbox frame
self.frame_days = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
self.frame_days.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
self.frame_days.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

for col_idx, (dag_full, dag_kort) in enumerate(zip(DAGEN_VAN_WEEK, DAGEN_AFKORT)):
    var = self.dag_filters[dag_full]
    btn = ctk.CTkCheckBox(
        self.frame_days,
        text=dag_kort.upper(),
        variable=var,
        onvalue=True,
        offvalue=False,
        font=("Helvetica", 9, "bold"),
        command=self.on_dag_filter_changed
    )
    btn.grid(row=0, column=col_idx, padx=2, pady=2, sticky="ew")
    self.dag_buttons[dag_full] = btn
```

**UPDATE row numbers:** Verschuif alle volgende rijen met 1 omhoog!

---

## 📍 STAP 4: Update alle ROW NUMBERS na de dag checkboxes

**Alles wat na de dag-checkbox state eronder zit, moet 1 rij omhoog:**

```python
# VOOR (oude nummering):
# row 4 = Select Voice
# row 5 = Prompt Status
# row 6 = AI Prompt

# NA (nieuwe nummering):
# row 5 = Select Voice
# row 6 = Prompt Status  
# row 7 = AI Prompt
```

**SNEL: Voeg +1 toe aan alle rijen na row 4:**

```python
ctk.CTkLabel(self.frame_inputs, text=t("select_voice", self.language)).grid(row=5, column=0, padx=10, pady=4,
                                                                            sticky="e")  # WAS row=4
self.cmb_voice = ctk.CTkComboBox(self.frame_inputs, values=STEM_OPTIES)
self.cmb_voice.grid(row=5, column=1, padx=10, pady=4, sticky="ew")  # WAS row=4

ctk.CTkLabel(self.frame_inputs, text=t("prompt_status", self.language)).grid(row=6, column=0, padx=10, pady=4,
                                                                             sticky="e")  # WAS row=5
self.sw_prompt_active = ctk.CTkSwitch(self.frame_inputs, text=t("active_on", self.language),
                                      variable=self.prompt_active_var,
                                      onvalue=True, offvalue=False)
self.sw_prompt_active.grid(row=6, column=1, padx=10, pady=4, sticky="w")  # WAS row=5

ctk.CTkLabel(self.frame_inputs, text=t("ai_prompt", self.language)).grid(row=7, column=0, padx=10, pady=4,
                                                                         sticky="ne")  # WAS row=6
self.txt_script = ctk.CTkTextbox(self.frame_inputs, height=200)
self.txt_script.grid(row=7, column=1, padx=10, pady=4, sticky="nsew")  # WAS row=6

# EN ALLES DAARNA OOK +1!
```

---

## 📍 STAP 5: Voeg deze methodes toe

**Voeg onderstaande methodes toe in je App klasse:**

```python
def on_dag_filter_changed(self):
    """Wordt aangroepen wanneer een dag-checkbox verandert"""
    self.update_listbox()

def get_selected_days(self):
    """Geeft lijst van aangevinkte dagen terug"""
    selected = [dag for dag, var in self.dag_filters.items() if var.get()]
    return selected

def prompt_matches_selected_days(self, prompt):
    """Check of prompt aan geselecteerde dagen voldoet"""
    prompt_days = prompt.get("days", [])  # BELANGRIJK: zie stap 6!
    
    # Als geen dagen ingesteld → altijd tonen
    if not prompt_days:
        return True
    
    # Anders: check of tenminste 1 dag aangevinkt is
    selected_days = self.get_selected_days()
    if not selected_days:  # Geen dagen aangevinkt = alles tonen
        return True
    
    # Check overlap tussen prompt dagen en selected dagen
    return any(day in prompt_days for day in selected_days)
```

---

## 📍 STAP 6: Update de `on_listbox_select` methode

**ZOEK:**
```python
def on_listbox_select(self, e):
    sel = self.lst_prompts.curselection()
    if sel:
        # ... code ...
        self.cmb_day.set(p.get("day", "Blanco"))
```

**VERVANG DOOR:**
```python
def on_listbox_select(self, e):
    sel = self.lst_prompts.curselection()
    if sel:
        # ... bestaande code ...
        
        # VERVANG DEZE REGEL:
        # self.cmb_day.set(p.get("day", "Blanco"))
        
        # MET DEZE CODE:
        # Reset alle dag checkboxes
        for var in self.dag_filters.values():
            var.set(False)
        
        # Zet aangevinkte dagen van prompt
        prompt_days = p.get("days", [])
        for dag in prompt_days:
            if dag in self.dag_filters:
                self.dag_filters[dag].set(True)
```

---

## 📍 STAP 7: Update `on_new_prompt` methode

**ZOEK:**
```python
def on_new_prompt(self):
    p = {
        "start": self.ent_start.get().strip(),
        "end": self.ent_end.get().strip(),
        "show": self.cmb_show.get().strip(),
        "day": self.cmb_day.get(),
        "voice": self.cmb_voice.get(),
        "active": self.prompt_active_var.get(),
        "script": self.txt_script.get("1.0", "end").strip()
    }
```

**VERVANG DOOR:**
```python
def on_new_prompt(self):
    selected_days = self.get_selected_days()
    
    p = {
        "start": self.ent_start.get().strip(),
        "end": self.ent_end.get().strip(),
        "show": self.cmb_show.get().strip(),
        "days": selected_days,  # NIEUW: List van dagen ipv single "day"
        "voice": self.cmb_voice.get(),
        "active": self.prompt_active_var.get(),
        "script": self.txt_script.get("1.0", "end").strip()
    }
```

---

## 📍 STAP 8: Update `on_update_prompt` methode

**ZOEK:**
```python
def on_update_prompt(self):
    if self.edit_index is not None and self.edit_index < len(self.prompts):
        self.prompts[self.edit_index] = {
            "start": self.ent_start.get().strip(),
            "end": self.ent_end.get().strip(),
            "show": self.cmb_show.get().strip(),
            "day": self.cmb_day.get(),
            "voice": self.cmb_voice.get(),
            "active": self.prompt_active_var.get(),
            "script": self.txt_script.get("1.0", "end").strip()
        }
```

**VERVANG DOOR:**
```python
def on_update_prompt(self):
    if self.edit_index is not None and self.edit_index < len(self.prompts):
        selected_days = self.get_selected_days()
        
        self.prompts[self.edit_index] = {
            "start": self.ent_start.get().strip(),
            "end": self.ent_end.get().strip(),
            "show": self.cmb_show.get().strip(),
            "days": selected_days,  # NIEUW
            "voice": self.cmb_voice.get(),
            "active": self.prompt_active_var.get(),
            "script": self.txt_script.get("1.0", "end").strip()
        }
```

---

## 📍 STAP 9: Update `update_listbox` methode

**ZOEK:**
```python
def update_listbox(self):
    selected_shows = [show for show, var in self.show_filters.items() if var.get()]

    if selected_shows:
        filtered_prompts = [p for p in self.prompts if p.get("show") in selected_shows]
    else:
        filtered_prompts = self.prompts

    filtered_prompts = self.filter_by_tags(filtered_prompts)
```

**VERVANG DOOR:**
```python
def update_listbox(self):
    # Show filters
    selected_shows = [show for show, var in self.show_filters.items() if var.get()]
    if selected_shows:
        filtered_prompts = [p for p in self.prompts if p.get("show") in selected_shows]
    else:
        filtered_prompts = self.prompts

    # Tag filters
    filtered_prompts = self.filter_by_tags(filtered_prompts)
    
    # DAG FILTERS (NIEUW)
    filtered_prompts = [p for p in filtered_prompts if self.prompt_matches_selected_days(p)]
```

---

## 📍 STAP 10: Update listbox display text

**ZOEK (in `update_listbox`):**
```python
for idx, p in enumerate(sorted_prompts):
    start = p.get("start", "00:00")
    end = p.get("end", "00:00")
    day = p.get("day", "Blanco")
    show = p.get("show", "Onbekende Show")
    # ... rest ...
    display_text = f" {start}-{end} | {day} | {show} | {voice}{status_str}"
```

**VERVANG DOOR:**
```python
for idx, p in enumerate(sorted_prompts):
    start = p.get("start", "00:00")
    end = p.get("end", "00:00")
    
    # Dagen weergeven (NIEUW)
    prompt_days = p.get("days", [])
    if prompt_days:
        days_text = ", ".join([DAGEN_AFKORT[DAGEN_VAN_WEEK.index(dag)] for dag in prompt_days])
    else:
        days_text = "alle"
    
    show = p.get("show", "Onbekende Show")
    voice = p.get("voice", "alloy")
    is_active = p.get("active", True)

    status_str = "" if is_active else " [UIT]"
    display_text = f" {start}-{end} | {days_text} | {show} | {voice}{status_str}"
```

---

## 📍 STAP 11: Migratie van oude data

**Voeg dit toe in `load_prompts` methode:**

```python
def load_prompts(self):
    if os.path.exists(PATH_PROMPTS):
        try:
            with open(PATH_PROMPTS, "r") as f:
                data = json.load(f)
                if isinstance(data, dict) and "prompts" in data:
                    self.prompts = data["prompts"]
                elif isinstance(data, list):
                    self.prompts = data
                else:
                    self.prompts = []
            
            # MIGRATIE: Converteer oude "day" naar "days" (NIEUW)
            for prompt in self.prompts:
                if "day" in prompt and "days" not in prompt:
                    old_day = prompt.get("day", "Blanco")
                    if old_day and old_day != "Blanco":
                        prompt["days"] = [old_day]
                    else:
                        prompt["days"] = []  # Blanco → alle dagen
                    del prompt["day"]
            
            self.save_prompts()  # Sla meteen op met nieuw format
            
        except Exception as e:
            self.log(f"Fout bij laden van bestaande prompts: {e}")

    if not self.prompts:
        self.prompts = DEFAULT_PROMPTS.copy()
        self.save_prompts()
    else:
        self.update_listbox()
```

---

## 📍 STAP 12: Update DEFAULT_PROMPTS

**ZOEK:**
```python
DEFAULT_PROMPTS = [
    {
        "start": "09:00", "end": "11:00", "show": "Radio Freaks", "day": "Blanco", "voice": "alloy", "active": True,
        "script": "Welkom bij Radio Freaks! [art] brengt je [tit]. Dit is de plek voor bizarre en coole muziek!"
    },
]
```

**VERVANG DOOR:**
```python
DEFAULT_PROMPTS = [
    {
        "start": "09:00", 
        "end": "11:00", 
        "show": "Radio Freaks", 
        "days": [],  # Leeg = alle dagen
        "voice": "alloy", 
        "active": True,
        "script": "Welkom bij Radio Freaks! [art] brengt je [tit]. Dit is de plek voor bizarre en coole muziek!"
    },
]
```

---

## ✅ KLAAR!

### Wat veranderd is:

| Voor | Na |
|------|-----|
| Dropdown "Blanco, ma, di..." | Checkbox buttons Ma-Zo |
| `"day": "ma"` | `"days": ["Maandag", "Dinsdag"]` |
| Prompt werkt op 1 dag | Prompt werkt op meerdere aangevinkte dagen |
| Onduidelijk | Duidelijk visueel |

### In de listbox zie je nu:
```
09:00-11:00 | ma, wo, vr | Radio Freaks | alloy
09:00-11:00 | alle | Middag Post | nova
```

Klaar? 🚀

