import json
from pathlib import Path
try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:
    tk = None
    ttk = None

from .prompt_logic import DAY_ORDER, migrate_prompt_record, prompt_days, prompt_is_valid_for_moment, prompt_sort_key

DEFAULT_PROMPTS_PATH = Path(__file__).resolve().parents[1] / "prompts.json"

class RadioAIPro(tk.Tk if tk else object):
    def __init__(self, prompts_path=DEFAULT_PROMPTS_PATH):
        if tk is None or ttk is None:
            raise RuntimeError("tkinter is required to run RadioAIPro")
        super().__init__()
        self.title("Radio AI PRO")
        self.prompts_path = Path(prompts_path)
        self.prompts = []
        self.edit_index = None
        self._sorted_prompt_indices = []

        self._build_ui()
        self.load_prompts()

    def _build_ui(self):
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.pack(fill="x", padx=12, pady=12)

        ttk.Label(self.frame_inputs, text="Start").grid(row=0, column=0, sticky="e", padx=4, pady=2)
        self.ent_start = ttk.Entry(self.frame_inputs)
        self.ent_start.grid(row=0, column=1, sticky="ew", padx=4, pady=2)

        ttk.Label(self.frame_inputs, text="Eind").grid(row=1, column=0, sticky="e", padx=4, pady=2)
        self.ent_end = ttk.Entry(self.frame_inputs)
        self.ent_end.grid(row=1, column=1, sticky="ew", padx=4, pady=2)

        ttk.Label(self.frame_inputs, text="Show").grid(row=2, column=0, sticky="e", padx=4, pady=2)
        self.cmb_show = ttk.Combobox(self.frame_inputs, values=[])
        self.cmb_show.grid(row=2, column=1, sticky="ew", padx=4, pady=2)

        ttk.Label(self.frame_inputs, text="Dagen").grid(row=3, column=0, sticky="ne", padx=4, pady=2)
        self.frame_days = ttk.Frame(self.frame_inputs)
        self.frame_days.grid(row=3, column=1, sticky="w", padx=4, pady=2)
        self.day_vars = {}
        for col, day in enumerate(DAY_ORDER):
            var = tk.BooleanVar(value=False)
            self.day_vars[day] = var
            ttk.Checkbutton(self.frame_days, text=day.upper(), variable=var).grid(
                row=0, column=col, padx=2, pady=2, sticky="w"
            )

        ttk.Label(self.frame_inputs, text="Voice").grid(row=4, column=0, sticky="e", padx=4, pady=2)
        self.cmb_voice = ttk.Combobox(self.frame_inputs, values=[])
        self.cmb_voice.grid(row=4, column=1, sticky="ew", padx=4, pady=2)

        self.prompt_active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.frame_inputs, text="Actief", variable=self.prompt_active_var).grid(
            row=5, column=1, sticky="w", padx=4, pady=2
        )

        ttk.Label(self.frame_inputs, text="Script").grid(row=6, column=0, sticky="ne", padx=4, pady=2)
        self.txt_script = tk.Text(self.frame_inputs, height=6, width=50)
        self.txt_script.grid(row=6, column=1, sticky="ew", padx=4, pady=2)

        self.frame_inputs.grid_columnconfigure(1, weight=1)

        self.lst_prompts = tk.Listbox(self)
        self.lst_prompts.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.lst_prompts.bind("<<ListboxSelect>>", self.on_listbox_select)

    def update_clock(self):
        self.after(1000, self.update_clock)

    def _selected_days(self):
        return [day for day, var in self.day_vars.items() if var.get()]

    def _set_day_checkboxes(self, prompt):
        selected = set(prompt_days(prompt))
        for day, var in self.day_vars.items():
            var.set(day in selected)

    def _build_prompt_payload(self):
        selected_days = self._selected_days()
        return {
            "start": self.ent_start.get().strip(),
            "end": self.ent_end.get().strip(),
            "show": self.cmb_show.get().strip(),
            "days": selected_days,
            "voice": self.cmb_voice.get().strip(),
            "active": self.prompt_active_var.get(),
            "script": self.txt_script.get("1.0", "end").strip(),
        }

    def on_new_prompt(self):
        prompt = self._build_prompt_payload()
        if not prompt["start"] or not prompt["end"] or not prompt["script"] or not prompt["days"]:
            return False
        self.prompts.append(prompt)
        self.save_prompts()
        self.update_listbox()
        return True

    def on_update_prompt(self):
        if self.edit_index is None or self.edit_index >= len(self.prompts):
            return False
        prompt = self._build_prompt_payload()
        if not prompt["start"] or not prompt["end"] or not prompt["script"] or not prompt["days"]:
            return False
        self.prompts[self.edit_index] = prompt
        self.save_prompts()
        self.update_listbox()
        return True

    def on_listbox_select(self, _event=None):
        selected = self.lst_prompts.curselection()
        if not selected:
            return
        sorted_idx = selected[0]
        if sorted_idx >= len(self._sorted_prompt_indices):
            return
        self.edit_index = self._sorted_prompt_indices[sorted_idx]
        prompt = self.prompts[self.edit_index]

        self.ent_start.delete(0, "end")
        self.ent_start.insert(0, prompt.get("start", ""))
        self.ent_end.delete(0, "end")
        self.ent_end.insert(0, prompt.get("end", ""))
        self.cmb_show.set(prompt.get("show", ""))
        self.cmb_voice.set(prompt.get("voice", ""))
        self.prompt_active_var.set(prompt.get("active", True))

        self.txt_script.delete("1.0", "end")
        self.txt_script.insert("1.0", prompt.get("script", ""))
        self._set_day_checkboxes(prompt)

    def get_valid_prompts(self, now=None):
        return sorted((p for p in self.prompts if prompt_is_valid_for_moment(p, now)), key=prompt_sort_key)

    def update_listbox(self):
        self.lst_prompts.delete(0, "end")
        sorted_pairs = sorted(enumerate(self.prompts), key=lambda pair: prompt_sort_key(pair[1]))
        self._sorted_prompt_indices = [idx for idx, _prompt in sorted_pairs]

        for _idx, prompt in sorted_pairs:
            days = prompt_days(prompt)
            day_text = ",".join(days) if days else "-"
            display = f"{prompt.get('start', '')}-{prompt.get('end', '')} | {day_text} | {prompt.get('show', '')}"
            self.lst_prompts.insert("end", display)

    def load_prompts(self):
        if self.prompts_path.exists():
            with self.prompts_path.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
                prompt_list = loaded.get("prompts", loaded) if isinstance(loaded, dict) else loaded
                if not isinstance(prompt_list, list):
                    prompt_list = []
                self.prompts = [migrate_prompt_record(prompt) for prompt in prompt_list if isinstance(prompt, dict)]
        else:
            self.prompts = []
        self.save_prompts()
        self.update_listbox()

    def save_prompts(self):
        payload = [migrate_prompt_record(prompt) for prompt in self.prompts]
        self.prompts_path.parent.mkdir(parents=True, exist_ok=True)
        with self.prompts_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
