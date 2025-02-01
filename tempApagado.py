import tkinter as tk
from tkinter import messagebox
import os
import threading
import time

class ShutdownTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienvenido Mitchel a tu temporizador de apagado B)")
        self.root.geometry("500x400")

        self.label = tk.Label(root, text="Selecciona el temporizador (minutos):")
        self.label.pack(pady=20)

        self.slider = tk.Scale(root, from_=1, to=120, orient=tk.HORIZONTAL, length=400)
        self.slider.pack(pady=20)

        self.done_button = tk.Button(root, text="Listo!", command=self.start_timer)
        self.done_button.pack(pady=20)

        self.cancel_button = tk.Button(root, text="Cancelar apagado", command=self.cancel_shutdown)
        self.cancel_button.pack(pady=20)

        self.status_label = tk.Label(root, text="", fg="red")
        self.status_label.pack(pady=10)

        self.shutdown_thread = None
        self.cancel_flag = threading.Event()

    def start_timer(self):
        minutes = self.slider.get()
        seconds = minutes * 60
        self.status_label.config(text=f"Quedan: {minutes} minuto(s) para el apagado.")
        self.cancel_flag.clear() 
        self.shutdown_thread = threading.Thread(target=self.shutdown_countdown, args=(seconds,))
        self.shutdown_thread.start()

    def shutdown_countdown(self, seconds):
        for remaining in range(seconds, 0, -1):
            if self.cancel_flag.is_set():
                self.root.after(0, lambda: self.status_label.config(text="Temporizador cancelado!"))
                return
            time.sleep(1)
            # Actualizar la GUI cada segundo
            self.root.after(0, lambda r=remaining: self.status_label.config(
                text=f"Quedan: {r // 60} min {r % 60} seg"))

        # Ejecutar el apagado después del conteo
        os.system("shutdown /s /t 1")

    def cancel_shutdown(self):
        self.cancel_flag.set()  # Señal para detener el hilo
        os.system("shutdown /a")
        self.status_label.config(text="Apagado cancelado!")
        messagebox.showinfo("Temporizador de apagado", "El temporizador fué cancelado!.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownTimerApp(root)
    root.mainloop()
