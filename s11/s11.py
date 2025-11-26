#REALIZADO POR: 
# JUAN CARLOS SANMIGUEL
# GONZALO FERNÁNDEZ
# ANA PADILLA
# ANAÍS GONZÁLEZ
# DANIEL RAMOS JIMÉNEZ

# Cosas a mejorar en este S11:
# Guardar y cargar claves desde archivo "Gonzalo" ---HECHO---
# Agregar más emojis a la lista para generar claves más seguras "Ana" ---HECHO---
# Mejorar la interfaz gráfica con más estilos y organización "Juan Carlos"  ---HECHO---
# Mejorar minijuegos (pistas y no repetir misma frase dos veces seguidas) "Daniel Ramos" ---Hecho---
# Validar entrada antes de codificar/decodificar (si está vacío o no) "ANAIS" ---Hecho---
# Indicar en la interfaz si hay clave cargada/generada "Ana" ---HECHO---

# EmojiCiper
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import random
import emoji
import json
import unicodedata

# ---------------------- Configuración global ----------------------
clave_actual = None
estado_clave_label = None

# Paleta de colores
BG_PRIMARY = "#0F172A"
BG_SECONDARY = "#1E293B"
TXT_PRIMARY = "#EAEAEA"
BTN_MAIN = "#6366F1"
BTN_ALT = "#22C55E"
BTN_GAME = "#F59E0B"
INPUT_BG = "#0B1220"

# ---------------------- Funciones utilitarias ----------------------
def actualizar_estado_clave(texto):
    global estado_clave_label
    if estado_clave_label is not None:
        estado_clave_label.config(text=f"🔐 {texto}")

def normalize_text(s: str) -> str:
    s = s.strip().lower()
    nfkd = unicodedata.normalize('NFD', s)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))

# ---------------------- Emoji y codificación ----------------------
def emoji_translate(text: str) -> str:
    text = text.strip()
    for lang in ["es", "alias"]:
        em = emoji.emojize(f":{text}:", language=lang)
        if em != f":{text}:":
            return em
    dem_es = emoji.demojize(text, language='es')
    dem_en = emoji.demojize(text, language='alias')
    if dem_es != text: return dem_es.strip(":")
    if dem_en != text: return dem_en.strip(":")
    return "❓"

def generar_clave():
    lista_emojis = list(emoji.EMOJI_DATA.keys())
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.!?-"
    random.shuffle(lista_emojis)
    lista_emojis = lista_emojis[:len(caracteres)]
    random.shuffle(lista_emojis)
    return {caracteres[i]: lista_emojis[i] for i in range(len(caracteres))}

def codificar(texto, clave):
    return "".join(clave.get(c, c) for c in texto)

def decodificar(texto, clave):
    inversa = {v: k for k, v in clave.items()}
    claves_ordenadas = sorted(inversa.keys(), key=len, reverse=True)
    res = ""
    i = 0
    while i < len(texto):
        match = None
        for em in claves_ordenadas:
            if texto.startswith(em, i):
                match = em
                break
        if match:
            res += inversa[match]
            i += len(match)
        else:
            res += texto[i]
            i += 1
    return res

# ---------------------- Juegos ----------------------
frases_emoji = {
    "te quiero": "❤️👉👤",
    "buenos días": "☀️👋",
    "vamos a comer": "👉🍽️",
    "hace calor": "🔥🌞",
    "estoy cansado": "😩🛌"
}

peliculas_emoji = {
    "titanic": "🚢🌊💔",
    "el rey leon": "🦁👑🌅",
    "avatar": "🌌👽💙",
    "it": "🤡🎈",
    "jurassic park": "🦖🚙🌴"
}

ultima_frase = None
ultima_peli = None

def elegir_item_sin_repetir(diccionario: dict, ultima):
    keys = list(diccionario.keys())
    if len(keys) == 0: return None, None
    if len(keys) == 1: return keys[0], diccionario[keys[0]]
    intento = random.choice(keys)
    while intento == ultima:
        intento = random.choice(keys)
    return intento, diccionario[intento]

def generar_pista_simple(respuesta_original: str, tipo: str = "frase") -> str:
    partes = respuesta_original.split()
    if tipo=="frase":
        primera = partes[0] if partes else ""
        return f"Pista: empieza por '{primera}' y tiene {len(partes)} palabra(s)."
    else:
        iniciales = " ".join(p[0] for p in partes if p)
        return f"Pista: iniciales {iniciales} — {len(partes)} palabra(s)."

def pedir_respuesta_con_toplevel(titulo, mensaje):
    ventana_resp = tk.Toplevel(ventana)
    ventana_resp.title(titulo)
    ventana_resp.geometry("420x230")
    lbl = tk.Label(ventana_resp, text=mensaje, font=("Consolas", 13))
    lbl.pack(padx=20, pady=20)
    entrada_resp = tk.Entry(ventana_resp, font=("Consolas", 12))
    entrada_resp.pack(padx=20, pady=10, fill="x")
    resultado = {"respuesta": None}
    def enviar():
        resultado["respuesta"] = entrada_resp.get()
        ventana_resp.destroy()
    btn = tk.Button(ventana_resp, text="Enviar", command=enviar, font=("Consolas", 12))
    btn.pack(pady=10)
    entrada_resp.bind("<Return>", lambda e: enviar())
    ventana_resp.transient(ventana)
    ventana_resp.grab_set()
    ventana.wait_window(ventana_resp)
    return resultado["respuesta"]

def jugar_frase_emoji():
    global ultima_frase
    frase, em = elegir_item_sin_repetir(frases_emoji, ultima_frase)
    if frase is None: return
    ultima_frase = frase
    intentos = 2
    while intentos > 0:
        mensaje = f"Traduce esta frase:\n\n{em}\n\nIntentos restantes: {intentos}"
        respuesta = pedir_respuesta_con_toplevel("Adivina la frase", mensaje)
        if respuesta is None: return
        if normalize_text(respuesta) == normalize_text(frase):
            messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
            return
        intentos -= 1
        if intentos==1:
            pista = generar_pista_simple(frase, "frase")
            messagebox.showinfo("Pista", pista)
        else:
            messagebox.showerror("Fin del juego", f"Has perdido 😢\nLa frase era:\n\n{frase}")
            return

def jugar_pelicula_emoji():
    global ultima_peli
    peli, em = elegir_item_sin_repetir(peliculas_emoji, ultima_peli)
    if peli is None: return
    ultima_peli = peli
    intentos = 2
    while intentos > 0:
        mensaje = f"Adivina la película:\n\n{em}\n\nIntentos restantes: {intentos}"
        respuesta = pedir_respuesta_con_toplevel("Adivina la película", mensaje)
        if respuesta is None: return
        if normalize_text(respuesta) == normalize_text(peli):
            messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
            return
        intentos -=1
        if intentos==1:
            pista = generar_pista_simple(peli, "pelicula")
            messagebox.showinfo("Pista", pista)
        else:
            messagebox.showerror("Fin del juego", f"Has perdido 😢\nLa película era:\n\n{peli}")
            return

# ---------------------- Guardar/Cargar clave ----------------------
def guardar_clave():
    global clave_actual
    if clave_actual is None:
        messagebox.showwarning("Aviso", "No hay ninguna clave para guardar.")
        return
    archivo = filedialog.asksaveasfilename(defaultextension=".json",
                                           filetypes=[("Archivos JSON", "*.json")],
                                           title="Guardar clave")
    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(clave_actual, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Éxito", "Clave guardada correctamente.")

def cargar_clave():
    global clave_actual
    archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")],
                                         title="Cargar clave")
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            clave_actual = json.load(f)
        actualizar_estado_clave("Clave cargada ✔")
        messagebox.showinfo("Éxito", "Clave cargada correctamente.")
        mostrar_main_ui()

# ---------------------- UI ----------------------
ventana = tk.Tk()
ventana.title("EmojiCiper")
ventana.geometry("1200x800")
ventana.configure(bg=BG_PRIMARY)
ventana.resizable(False, False)

# --- Pantalla inicial de acceso ---
pantalla_inicio = tk.Frame(ventana, bg=BG_PRIMARY)
pantalla_inicio.pack(expand=True, fill="both")

lbl_titulo = tk.Label(pantalla_inicio, text="EmojiCiper", font=("Arial", 36, "bold"), bg=BG_PRIMARY, fg=BTN_MAIN)
lbl_titulo.pack(pady=40)

lbl_info = tk.Label(pantalla_inicio, text="Genera o carga tu clave para acceder a la aplicación",
                    font=("Arial", 16), bg=BG_PRIMARY, fg=TXT_PRIMARY)
lbl_info.pack(pady=20)

def generar_y_cargar_clave():
    global clave_actual
    clave_actual = generar_clave()
    actualizar_estado_clave("Clave generada ✔")
    messagebox.showinfo("Clave", "Clave generada correctamente.")
    mostrar_main_ui()

btn_generar = tk.Button(pantalla_inicio, text="Generar clave", font=("Arial", 14, "bold"),
                        bg=BTN_MAIN, fg="white", width=25, height=2, command=generar_y_cargar_clave)
btn_generar.pack(pady=10)

btn_cargar = tk.Button(pantalla_inicio, text="Cargar clave", font=("Arial", 14, "bold"),
                        bg=BTN_ALT, fg="white", width=25, height=2, command=cargar_clave)
btn_cargar.pack(pady=10)

# ---------------------- Función para mostrar menú principal ----------------------
def mostrar_main_ui():
    pantalla_inicio.pack_forget()

    main_frame = tk.Frame(ventana, bg=BG_PRIMARY)
    main_frame.pack(expand=True, fill="both")

    global estado_clave_label
    estado_clave_label = tk.Label(main_frame, text="Clave actual: ✔", font=("Consolas", 12, "bold"),
                                  bg=BG_PRIMARY, fg=TXT_PRIMARY)
    estado_clave_label.pack(pady=5)

    notebook = ttk.Notebook(main_frame)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # --- Pestaña Codificación ---
    tab_cod = tk.Frame(notebook, bg=BG_SECONDARY)
    notebook.add(tab_cod, text="Codificación")
    entrada_cod = scrolledtext.ScrolledText(tab_cod, width=85, height=10, font=("Consolas", 12),
                                            bg=INPUT_BG, fg=TXT_PRIMARY, insertbackground=TXT_PRIMARY)
    entrada_cod.pack(padx=10, pady=10)
    salida_cod = scrolledtext.ScrolledText(tab_cod, width=85, height=10, font=("Consolas", 12),
                                           bg=INPUT_BG, fg=TXT_PRIMARY, insertbackground=TXT_PRIMARY)
    salida_cod.pack(padx=10, pady=10)
    frame_cod_btn = tk.Frame(tab_cod, bg=BG_SECONDARY)
    frame_cod_btn.pack(pady=10)
    def add_button(parent, text, cmd, color):
        b = tk.Button(parent, text=text, command=cmd, font=("Arial", 12, "bold"),
                      bg=color, fg="white", width=28, height=3)
        return b
    # Botones codificación
    btn1 = add_button(frame_cod_btn, "Codificar", lambda: codificar_wrapper(entrada_cod, salida_cod), BTN_MAIN)
    btn2 = add_button(frame_cod_btn, "Decodificar", lambda: decodificar_wrapper(salida_cod), BTN_ALT)
    btn3 = add_button(frame_cod_btn, "Traducir emoji/palabra", lambda: traducir_wrapper(entrada_cod, salida_cod), BTN_GAME)
    btn4 = add_button(frame_cod_btn, "Ver clave", lambda: messagebox.showinfo("Clave actual", str(clave_actual)), BTN_MAIN)
    btn1.grid(row=0, column=0, padx=10, pady=5)
    btn2.grid(row=0, column=1, padx=10, pady=5)
    btn3.grid(row=1, column=0, padx=10, pady=5)
    btn4.grid(row=1, column=1, padx=10, pady=5)

    # --- Pestaña Minijuegos ---
    tab_juegos = tk.Frame(notebook, bg=BG_SECONDARY)
    notebook.add(tab_juegos, text="Minijuegos")
    frame_juegos = tk.Frame(tab_juegos, bg=BG_SECONDARY)
    frame_juegos.pack(pady=40)
    btn_j1 = add_button(frame_juegos, "Adivina la frase con emojis", jugar_frase_emoji, BTN_GAME)
    btn_j2 = add_button(frame_juegos, "Adivina la película", jugar_pelicula_emoji, BTN_GAME)
    btn_j1.grid(row=0, column=0, padx=10, pady=5)
    btn_j2.grid(row=0, column=1, padx=10, pady=5)

    # --- Pestaña Gestión de Clave ---
    tab_clave = tk.Frame(notebook, bg=BG_SECONDARY)
    notebook.add(tab_clave, text="Gestionar Clave")
    frame_clave = tk.Frame(tab_clave, bg=BG_SECONDARY)
    frame_clave.pack(pady=40)
    btn_guardar = add_button(frame_clave, "Guardar clave", guardar_clave, BTN_MAIN)
    btn_cargar_tab = add_button(frame_clave, "Cargar clave", cargar_clave, BTN_ALT)
    btn_guardar.grid(row=0, column=0, padx=10, pady=5)
    btn_cargar_tab.grid(row=0, column=1, padx=10, pady=5)

# ---------------------- Wrappers ----------------------
def codificar_wrapper(entrada_widget, salida_widget):
    global clave_actual
    texto = entrada_widget.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "Escribe algo para codificar")
        return
    salida_widget.delete("1.0", tk.END)
    salida_widget.insert(tk.END, codificar(texto, clave_actual))

def decodificar_wrapper(salida_widget):
    global clave_actual
    texto = salida_widget.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "No hay texto para decodificar")
        return
    salida_widget.delete("1.0", tk.END)
    salida_widget.insert(tk.END, decodificar(texto, clave_actual))

def traducir_wrapper(entrada_widget, salida_widget):
    texto = entrada_widget.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "Escribe algo para traducir")
        return
    salida_widget.delete("1.0", tk.END)
    salida_widget.insert(tk.END, emoji_translate(texto))

ventana.mainloop()
