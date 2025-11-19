# Versión con interfaz gráfica usando Tkinter
# Incluye codificación/decodificación, traducción,
# + juegos con ventanas emergentes redimensionables

import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import emoji

# ------------------ Funciones originales ------------------
def emoji_translate(text: str) -> str:
    text = text.strip()

    shortcode_es = f":{text}:"
    em_es = emoji.emojize(shortcode_es, language='es')
    if em_es != shortcode_es:
        return em_es

    shortcode_en = f":{text}:"
    em_en = emoji.emojize(shortcode_en, language='alias')
    if em_en != shortcode_en:
        return em_en

    dem_es = emoji.demojize(text, language='es')
    if dem_es != text:
        return dem_es.strip(":")

    dem_en = emoji.demojize(text, language='alias')
    if dem_en != text:
        return dem_en.strip(":")

    return "❓"


def generar_clave():
    emoji_shortnames = [
        "grinning_face","smiley","sweat_smile","laughing","sunglasses",
        "rocket","snake","fire","star","heart","brain","computer",
        "coffee","book","robot","taco","pizza","cry","clap","wave"
    ]

    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.!?-"

    while len(emoji_shortnames) < len(caracteres):
        emoji_shortnames *= 2
    
    emoji_shortnames = emoji_shortnames[:len(caracteres)]
    random.shuffle(emoji_shortnames)

    clave = {c: emoji.emojize(f":{name}:", language='alias')
             for c, name in zip(caracteres, emoji_shortnames)}
    return clave


def codificar(texto, clave):
    return "".join(clave.get(c, c) for c in texto)


def decodificar(texto, clave):
    inversa = {v: k for k, v in clave.items()}
    res = ""
    i = 0

    while i < len(texto):
        match = None
        for em in inversa:
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


# ------------------ NUEVOS JUEGOS ------------------
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


def pedir_respuesta_con_toplevel(titulo, mensaje):
    """
    Ventana emergente redimensionable para pedir una respuesta.
    """
    ventana_resp = tk.Toplevel(ventana)
    ventana_resp.title(titulo)
    ventana_resp.geometry("420x230")
    ventana_resp.minsize(300, 150)
    ventana_resp.resizable(True, True)

    lbl = tk.Label(ventana_resp, text=mensaje, font=("Consolas", 13))
    lbl.pack(padx=20, pady=20, expand=True, fill="both")

    entrada_resp = tk.Entry(ventana_resp, font=("Consolas", 12))
    entrada_resp.pack(padx=20, pady=10, fill="x")

    resultado = {"respuesta": None}

    def enviar():
        resultado["respuesta"] = entrada_resp.get()
        ventana_resp.destroy()

    btn = tk.Button(ventana_resp, text="Enviar", command=enviar, font=("Consolas", 12))
    btn.pack(pady=10)

    entrada_resp.bind("<Return>", lambda event: enviar())

    ventana_resp.transient(ventana)
    ventana_resp.grab_set()
    ventana.wait_window(ventana_resp)

    return resultado["respuesta"]


def jugar_frase_emoji():
    frase, em = random.choice(list(frases_emoji.items()))
    intentos = 3

    while intentos > 0:
        mensaje = f"Traduce esta frase:\n\n{em}\n\nIntentos restantes: {intentos}"
        respuesta = pedir_respuesta_con_toplevel("Adivina la frase", mensaje)

        if respuesta is None:
            return

        if respuesta.lower().strip() == frase:
            messagebox.showinfo("Correcto", "¡Has acertado! 🎉")
            return

        intentos -= 1

    messagebox.showerror("Fin del juego", f"Has perdido 😢\nLa frase correcta era:\n\n{frase}")


def jugar_pelicula_emoji():
    peli, em = random.choice(list(peliculas_emoji.items()))
    intentos = 3

    while intentos > 0:
        mensaje = f"Adivina la película:\n\n{em}\n\nIntentos restantes: {intentos}"
        respuesta = pedir_respuesta_con_toplevel("Adivina la película", mensaje)

        if respuesta is None:
            return

        if respuesta.lower().strip() == peli:
            messagebox.showinfo("Correcto", "¡Acertaste la película! 🎬✨")
            return

        intentos -= 1

    messagebox.showerror("Fin del juego", f"No acertaste 😢\nLa película era:\n\n{peli}")


# ------------------ Interfaz gráfica ------------------
clave_actual = None

ventana = tk.Tk()
ventana.title("Emoji Encoder GUI")
ventana.geometry("600x650")
ventana.configure(bg="#2e2e2e")

fuente_texto = ("Consolas", 12)
color_fondo_texto = "#1e1e1e"
color_texto = "#ffffff"
color_boton = "#444444"
color_boton_fg = "#ffffff"

entrada = scrolledtext.ScrolledText(
    ventana, width=60, height=8, bg=color_fondo_texto, fg=color_texto,
    font=fuente_texto, insertbackground=color_texto
)
entrada.pack(pady=10, padx=10)

salida = scrolledtext.ScrolledText(
    ventana, width=60, height=8, bg=color_fondo_texto, fg=color_texto,
    font=fuente_texto, insertbackground=color_texto
)
salida.pack(pady=10, padx=10)

# ------------------ Acciones Botones ------------------
def accion_generar_clave():
    global clave_actual
    clave_actual = generar_clave()
    messagebox.showinfo("Clave", "Clave generada correctamente.")

def accion_codificar():
    if clave_actual is None:
        messagebox.showwarning("Aviso", "Genera una clave primero.")
        return
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, codificar(entrada.get("1.0", tk.END), clave_actual))

def accion_decodificar():
    if clave_actual is None:
        messagebox.showwarning("Aviso", "Genera una clave primero.")
        return
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, decodificar(entrada.get("1.0", tk.END), clave_actual))

def accion_traducir():
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, emoji_translate(entrada.get("1.0", tk.END).strip()))

# ------------------ Botones ------------------
frame_botones = tk.Frame(ventana, bg="#2e2e2e")
frame_botones.pack(pady=10)

def add_btn(text, cmd):
    b = tk.Button(
        frame_botones, text=text, width=25, height=2, command=cmd,
        bg=color_boton, fg=color_boton_fg, activebackground="#555555",
        font=("Consolas", 11, "bold")
    )
    b.pack(pady=5)

add_btn("Generar clave", accion_generar_clave)
add_btn("Codificar", accion_codificar)
add_btn("Decodificar", accion_decodificar)
add_btn("Traducir emoji/palabra", accion_traducir)
add_btn("🎮 Adivina la frase con emojis", jugar_frase_emoji)
add_btn("🎬 Adivina la película", jugar_pelicula_emoji)

ventana.mainloop()
