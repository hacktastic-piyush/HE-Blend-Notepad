import tkinter as tk
from tkinter import filedialog, messagebox
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# ---------------- LANGUAGE ----------------
LANG = {
    "en": {
        "title": "HE-Blend Notepad",
        "file": "File",
        "view": "View",
        "convert": "Convert to Hindi",
        "new": "New",
        "open": "Open",
        "save": "Save",
        "sas": "Save As",
        "exit": "Exit",
        "theme": "ChangeTheme",
        "language": "Switch to Hindi",
        "exit_msg": "Do you want to exit?"
    },
    "hi": {
        "title": "HE-Blend Notepad",
        "file": "फ़ाइल",
        "view": "दृश्य",
        "convert": "हिंदी में बदलें",
        "new": "नया",
        "open": "खोलें",
        "save": "सहेजें",
        "sas": "इस रूप में सहेजें",
        "exit": "बाहर निकलें",
        "theme": "थीम बदलें",
        "language": "अंग्रेज़ी में बदलें",
        "exit_msg": "क्या आप बाहर निकलना चाहते हैं?"
    }
}

# ---------------- THEME ----------------
LIGHT = {"bg": "#ffffff", "fg": "#000000"}
DARK  = {"bg": "#1e1e1e", "fg": "#ffffff"}

# ---------------- STATE ----------------
current_lang = "en"
drkmode = False
cf = None

# ---------------- WINDOW ----------------
rot = tk.Tk()
rot.geometry("700x400")

# ---------------- FUNCTIONS ----------------
def apply_theme():
    t = DARK if drkmode else LIGHT
    rot.configure(bg=t["bg"])
    txta.configure(bg=t["bg"], fg=t["fg"], insertbackground=t["fg"])

def change_theme():
    global drkmode
    drkmode = not drkmode
    apply_theme()

def contohi():
    """
    Converts full English phonetic text to correct Hindi
    using the indic-transliteration library.
    """
    try:
        text = txta.get("1.0", "end-1c")
        hindi = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
        txta.delete("1.0", tk.END)
        txta.insert("1.0", hindi)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def nf():
    global cf
    txta.delete("1.0", tk.END)
    cf = None

def opf():
    global cf
    path = filedialog.askopenfilename()
    if path:
        with open(path, "r", encoding="utf-8") as f:
            txta.delete("1.0", tk.END)
            txta.insert("1.0", f.read())
        cf = path

def sf():
    global cf
    if not cf:
        sas()
        return
    with open(cf, "w", encoding="utf-8") as f:
        f.write(txta.get("1.0", "end-1c"))

def sas():
    global cf
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    if path:
        cf = path
        sf()

def ea():
    if messagebox.askyesno(
        LANG[current_lang]["exit"],
        LANG[current_lang]["exit_msg"]
    ):
        rot.destroy()

def bm():
    global mbr
    l = LANG[current_lang]

    mbr = tk.Menu(rot)

    fm = tk.Menu(mbr, tearoff=0)
    vm = tk.Menu(mbr, tearoff=0)

    fm.add_command(label=l["new"], command=nf)
    fm.add_command(label=l["open"], command=opf)
    fm.add_command(label=l["save"], command=sf)
    fm.add_command(label=l["sas"], command=sas)
    fm.add_separator()
    fm.add_command(label=l["exit"], command=ea)

    vm.add_command(label=l["convert"], command=contohi)
    vm.add_command(label=l["theme"], command=change_theme)
    vm.add_command(label=l["language"], command=sl)

    mbr.add_cascade(label=l["file"], menu=fm)
    mbr.add_cascade(label=l["view"], menu=vm)

    rot.config(menu=mbr)
    rot.title(l["title"])

def sl(event=None):
    global current_lang
    current_lang = "hi" if current_lang == "en" else "en"
    bm()

# ---------------- TEXT AREA ----------------
txta = tk.Text(
    rot,
    wrap="word",
    font=("Nirmala UI", 14)
)
txta.pack(fill="both", expand=True)

# ---------------- SHORTCUTS ----------------
rot.bind("<Control-l>", sl)
rot.bind("<Control-h>", lambda e: contohi())

# ---------------- START ----------------
apply_theme()
bm()
rot.mainloop()
