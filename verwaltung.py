import tkinter as tk
from tkinter import messagebox
import os
import json
import re
from PIL import Image
import datetime

DARK_BG = "#1e1e1e"
DARK_FG = "#ffffff"
BUTTON_BG = "#333333"
HIGHLIGHT = "#4a90e2"

# === HTML Generator ===
def open_html_gui():
    def extract_username(instagram_url):
        match = re.search(r"instagram\.com/([^/?#]+)", instagram_url)
        return match.group(1) if match else "unknown"

    def generate_html():
        titel = entry_titel.get()
        instagram = entry_instagram.get()
        beschreibung = text_beschreibung.get("1.0", tk.END).strip()
        ordner = entry_ordner.get()

        if not all([titel, instagram, beschreibung, ordner]):
            messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")
            return

        username = extract_username(instagram)

        html_output = HTML_TEMPLATE.format(
            titel=titel,
            instagram=instagram,
            username=username,
            beschreibung=beschreibung,
            ordner=ordner
        )

        filename = f"{ordner}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_output)

        log_event(f"HTML generiert: {filename}")
        messagebox.showinfo("Erfolg", f"HTML wurde erstellt: {filename}")

    html_window = tk.Toplevel()
    html_window.title("HTML Generator")
    html_window.configure(bg=DARK_BG)
    html_window.resizable(False, False)

    tk.Label(html_window, text="🖋 Titel / Überschrift:", bg=DARK_BG, fg=DARK_FG).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    entry_titel = tk.Entry(html_window, width=50, bg=BUTTON_BG, fg=DARK_FG, insertbackground=DARK_FG)
    entry_titel.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(html_window, text="🔗 Instagram-Link:", bg=DARK_BG, fg=DARK_FG).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    entry_instagram = tk.Entry(html_window, width=50, bg=BUTTON_BG, fg=DARK_FG, insertbackground=DARK_FG)
    entry_instagram.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(html_window, text="📝 Beschreibung:", bg=DARK_BG, fg=DARK_FG).grid(row=2, column=0, sticky="ne", pady=5, padx=5)
    text_beschreibung = tk.Text(html_window, width=38, height=5, bg=BUTTON_BG, fg=DARK_FG, insertbackground=DARK_FG)
    text_beschreibung.grid(row=2, column=1, pady=5, padx=5)

    tk.Label(html_window, text="📁 Ordnername (z. B. C400):", bg=DARK_BG, fg=DARK_FG).grid(row=3, column=0, sticky="e", pady=5, padx=5)
    entry_ordner = tk.Entry(html_window, width=50, bg=BUTTON_BG, fg=DARK_FG, insertbackground=DARK_FG)
    entry_ordner.grid(row=3, column=1, pady=5, padx=5)

    tk.Button(html_window, text="✨ HTML generieren", bg=HIGHLIGHT, fg=DARK_FG, command=generate_html).grid(row=4, column=1, pady=10)

    HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>LUMARO - GALLERY</title>
  <link rel="icon" href="dist/assets/favicon.ico" />
  <link rel="stylesheet" href="dist/output.css" />
  <link rel="stylesheet" href="styles.css" />
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Signika:wght@400;700&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.css" />
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    #loader {{
      position: fixed;
      inset: 0;
      background: rgb(25, 25, 25);
      z-index: 50;
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    .loader {{ display: flex; gap: 12px; }}
    .dot {{
      width: 22px; height: 22px; border-radius: 50%;
      animation: bounce 1s infinite ease-in-out;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }}
    .dot:nth-child(1) {{ background-color: #FFA500; animation-delay: 0s; }}
    .dot:nth-child(2) {{ background-color: #FF6A00; animation-delay: 0.1s; }}
    .dot:nth-child(3) {{ background-color: #FF3C38; animation-delay: 0.2s; }}
    .dot:nth-child(4) {{ background-color: #FF0080; animation-delay: 0.3s; }}
    .dot:nth-child(5) {{ background-color: #FF00BF; animation-delay: 0.4s; }}
    @keyframes bounce {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-12px); }}
    }}
  </style>
</head>
<body class="dark:bg-black bg-white min-h-screen flex flex-col text-black dark:text-white px-5 md:px-20">
  <div id="loader"><div class="loader">
    <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
  </div></div>
  <header class="pt-4 pb-4">
    <nav class="w-full">
      <div class="container mx-auto flex items-center">
        <a href="gallery.html" class="text-2xl font-signika font-bold">LUMARO</a>
      </div>
    </nav>
  </header>
  <main class="container mx-auto">
    <h1 class="text-4xl pt-10 pb-8 font-bold">{titel} - GALLERY</h1>
    <div class="bg-neutral-200 dark:bg-neutral-800 p-4 rounded-lg mb-6 shadow-md">
      <p class="text-lg font-signika mb-2">
        <a href="{instagram}" target="_blank" class="hover:underline">@{username}</a>
      </p>
      <p class="text-base text-neutral-800 dark:text-neutral-300">{beschreibung}</p>
    </div>
    <section class="text-neutral-700">
      <div class="flex flex-wrap w-full">
        <div class="flex w-full md:w-1/2 flex-wrap" id="leftCol"></div>
        <div class="flex w-full md:w-1/2 flex-wrap" id="rightCol"></div>
      </div>
    </section>
  </main>
  <footer class="text-center mt-auto py-4">
    <p class="text-xs text-gray-600 dark:text-gray-300">
      © 2025 <a href="https://lumaro.pics" class="hover:underline">lumaro.pics</a> – by
      <a href="https://www.instagram.com/visualsby.ben/" class="underline">Ben</a>
    </p>
  </footer>
  <script>
    Fancybox.bind("[data-fancybox]", {{}});
    const galleryFolder = "{ordner}";
    const leftCol = document.getElementById("leftCol");
    const rightCol = document.getElementById("rightCol");
    const loader = document.getElementById("loader");
    let left = true;
    fetch(`json/${{galleryFolder}}.json`)
      .then(res => res.json())
      .then(images => {{
        let loaded = 0;
        const total = images.length;
        const updateProgress = () => {{
          loaded++;
          if (loaded === total) {{
            setTimeout(() => loader.style.display = "none", 300);
          }}
        }};
        images.forEach(image => {{
          const target = left ? leftCol : rightCol;
          left = !left;
          const img = new Image();
          img.src = image;
          img.alt = "";
          img.className = "block h-full w-full object-cover object-center opacity-0 transition duration-500 hover:scale-105";
          img.onload = () => {{
            img.classList.add("opacity-100");
            updateProgress();
          }};
          img.onerror = updateProgress;
          const wrapper = document.createElement("div");
          wrapper.className = "w-full p-1";
          wrapper.innerHTML = `<div class="overflow-hidden h-full w-full"><a href="${{image}}" data-fancybox="gallery"></a></div>`;
          wrapper.querySelector("a").appendChild(img);
          target.appendChild(wrapper);
        }});
      }});
  </script>
</body>
</html>"""

# === JSON Generator ===
def generate_jsons():
    base_dir = "upload/jpg"
    output_dir = "json"
    os.makedirs(output_dir, exist_ok=True)
    count = 0

    for ordnername in os.listdir(base_dir):
        ordnerpfad = os.path.join(base_dir, ordnername)
        if os.path.isdir(ordnerpfad):
            bilder = [
                os.path.join("upload/jpg", ordnername, f)
                for f in sorted(os.listdir(ordnerpfad))
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            ]
            if bilder:
                json_path = os.path.join(output_dir, f"{ordnername}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(bilder, f, indent=2)
                count += 1

    log_event(f"{count} JSON-Datei(en) erstellt.")
    messagebox.showinfo("Erledigt", f"{count} JSON-Datei(en) wurden erstellt.")

# === Bildverkleinerung ===
def resize_images():
    def resize_image_to_target_size(input_path, output_path):
        from PIL import Image
        import io

        TARGET_SIZE = 1_000_000  # 1 MB
        TOLERANCE = 0.03  # 3 %
        with Image.open(input_path) as img:
            img = img.convert("RGB")
            width, height = img.size
            scale = 1.0
            step = 0.05
            quality = 95

            for _ in range(30):
                new_size = (int(width * scale), int(height * scale))
                resized_img = img.resize(new_size, Image.LANCZOS)
                buffer = io.BytesIO()
                resized_img.save(buffer, format="JPEG", quality=quality)
                size = buffer.tell()
                diff = (size - TARGET_SIZE) / TARGET_SIZE

                if abs(diff) <= TOLERANCE:
                    resized_img.save(output_path, format="JPEG", quality=quality)
                    return True

                if size > TARGET_SIZE:
                    scale -= step
                    quality = max(20, quality - 5)
                else:
                    scale += step
                    quality = min(95, quality + 5)

            resized_img.save(output_path, format="JPEG", quality=quality)
            return False

    def start_resizing():
        ordner_input = entry_ordner.get()
        ordnerliste = [o.strip() for o in ordner_input.split(",") if o.strip()]
        base_dir = "upload/jpg"
        resized_count = 0

        for ordner in ordnerliste:
            full_path = os.path.join(base_dir, ordner)
            if not os.path.isdir(full_path):
                continue
            original_path = os.path.join(full_path, "original")
            os.makedirs(original_path, exist_ok=True)

            for file in os.listdir(full_path):
                if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    original_file = os.path.join(full_path, file)
                    backup_file = os.path.join(original_path, file)
                    os.replace(original_file, backup_file)

                    try:
                        resize_image_to_target_size(backup_file, original_file)
                        resized_count += 1
                    except Exception as e:
                        print(f"Fehler bei {file}: {e}")

        log_event(f"{resized_count} Bilder wurden angepasst (≈1 MB).")
        messagebox.showinfo("Fertig", f"{resized_count} Bilder wurden auf ~1 MB angepasst.")

    resize_win = tk.Toplevel()
    resize_win.title("🖼 Bilder auf 1 MB skalieren")
    resize_win.configure(bg=DARK_BG)
    resize_win.resizable(False, False)

    tk.Label(resize_win, text="Ordnernamen (kommagetrennt):", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
    entry_ordner = tk.Entry(resize_win, width=60, bg=BUTTON_BG, fg=DARK_FG, insertbackground=DARK_FG)
    entry_ordner.pack(pady=5)
    tk.Button(resize_win, text="📏 Skalierung starten", bg=HIGHLIGHT, fg=DARK_FG, command=start_resizing).pack(pady=10)


# === Logging Function ===
def log_event(event):
    with open("history.log", "a", encoding="utf-8") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {event}\n")

# === History Viewer ===
def view_history():
    history_window = tk.Toplevel()
    history_window.title("History")
    history_window.configure(bg=DARK_BG)
    history_window.resizable(False, False)

    tk.Label(history_window, text="Letzte Aktionen:", bg=DARK_BG, fg=DARK_FG, font=("Segoe UI", 12, "bold")).pack(pady=5)

    try:
        with open("history.log", "r", encoding="utf-8") as log_file:
            history_content = log_file.read()
    except FileNotFoundError:
        history_content = "Keine Einträge vorhanden."

    text_widget = tk.Text(history_window, width=60, height=20, bg=BUTTON_BG, fg=DARK_FG, wrap="word")
    text_widget.insert("1.0", history_content)
    text_widget.config(state="disabled")
    text_widget.pack(pady=5, padx=5)

    tk.Button(history_window, text="Schließen", bg=HIGHLIGHT, fg=DARK_FG, command=history_window.destroy).pack(pady=10)

# === Main Menu Update ===
def open_main_menu():
    root = tk.Tk()
    root.title("Verwaltungs-Tool")
    root.configure(bg=DARK_BG)
    root.geometry("400x300")
    root.resizable(False, False)

    tk.Label(root, text="Was willst du machen?", font=("Segoe UI", 14, "bold"), bg=DARK_BG, fg=DARK_FG).pack(pady=10)
    button_style = {"width": 30, "height": 2, "font": ("Segoe UI", 10), "bd": 0, "bg": BUTTON_BG, "fg": DARK_FG, "activebackground": HIGHLIGHT}

    tk.Button(root, text="📝 HTML generieren", command=open_html_gui, **button_style).pack(pady=5)
    tk.Button(root, text="🧾 JSONs aus Bildern erstellen", command=generate_jsons, **button_style).pack(pady=5)
    tk.Button(root, text="📉 Bilder verkleinern", command=resize_images, **button_style).pack(pady=5)
    tk.Button(root, text="✅ Letzte Aktionen", command=view_history, **button_style).pack(pady=5)

    root.mainloop()

# === Start ===
if __name__ == "__main__":
    open_main_menu()
