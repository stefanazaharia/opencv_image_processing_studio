import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import script
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesare Imagini")
        self.root.geometry("1200x650")
        self.root.configure(bg="#edf1fc")
        
        self.original_cv = None
        self.processed_cv = None
        
        # bara de meniu
        self.menu_bar = tk.Menu(self.root)
        self.menu_bar.add_command(label="Ajutor", command=self.open_help_window)
        
        self.root.config(menu=self.menu_bar)

        # fereastra
        
        # coloana stanga cu filtre poze
        self.filter_frame = tk.LabelFrame(root, text="Filtre si Efecte", bg="#cfdeff", font=("Arial", 10, "bold"),  padx=10, pady=10)
        self.filter_frame.place(x=20, y=20, width=180, height=620)
        
        effects = [
            ("BLUR GAUSSIAN", script.apply_blur),
            ("BLUR STACK", script.apply_stack_blur),
            ("ALB-NEGRU", script.apply_grayscale),
            ("NEGATIV", script.apply_negative),
            ("ALB-NEGRU(Threshold)", script.apply_threshold),
            ("CONTUR (CANNY)", script.apply_edges),
            ("ROTIRE 90", script.apply_rotate),
            ("ROTIRE 45", script.apply_rotate_45),
            ("VARTEJ", script.apply_vortex),   
            ("VALURI", script.apply_waves),
            ("OGLINDIRE", script.apply_flip),
            ("PIXELI", script.apply_pixelate),
            ("CLARITATE", script.apply_sharpen),
            ("RAMA", script.apply_frame),
            ("DRAW", script.apply_shapes),
            ("WATERMARK", script.apply_watermark),
            ("ZOOM", script.apply_zoom)
        ]
        
        for name, func in effects:
            btn = tk.Button(self.filter_frame, text=name, bg="#2279fa", fg="white", activebackground="#095efd", font=("Arial", 10, "bold"), command=lambda f=func: self.process(f), width=15)
            btn.pack(pady=3, fill="x")
            btn.bind("<Enter>", lambda e, b =btn: b.config(bg="#5696fd"))
            btn.bind("<Leave>", lambda e, b =btn: b.config(bg="#2279fa"))

        # centru
        self.display_frame = tk.Frame(root, bg="#edf1fc")
        self.display_frame.place(x=210, y=20)

        # imagine initiala
        self.box_orig = tk.Frame(self.display_frame, bg="#cfdeff", width=450, height=450, highlightbackground="#61a0ff", highlightthickness=2)
        self.box_orig.grid(row=1, column=0, padx=20)
        self.box_orig.pack_propagate(False)
        tk.Label(self.display_frame, text="Imagine Originala", bg="#edf1fc", font=("Arial", 12, "bold")).grid(row=0, column=0)
        self.lbl_orig = tk.Label(self.box_orig, text="Nicio imagine incarcata", bg="#cfdeff", font=("Arial", 10, "bold"))
        self.lbl_orig.pack(expand=True)

        # imagine modificata
        self.box_proc = tk.Frame(self.display_frame, bg="#cfdeff", width=450, height=450, highlightbackground="#61a0ff", highlightthickness=2)
        self.box_proc.grid(row=1, column=1, padx=20)
        self.box_proc.pack_propagate(False)
        tk.Label(self.display_frame, text="Imagine Modificata",  bg="#edf1fc", font=("Arial", 12, "bold")).grid(row=0, column=1)
        self.lbl_proc = tk.Label(self.box_proc, text="Asteptare procesare...", bg="#cfdeff", font=("Arial", 10, "bold"))
        self.lbl_proc.pack(expand=True)

        # butoane jos
        self.ctrl_frame = tk.Frame(root, bg="#edf1fc")
        self.ctrl_frame.place(relx=0.5, rely=0.9, anchor="center")
        
        self.btn_incarca = tk.Button(self.ctrl_frame, text="INCARCA IMAGINE", bg="#61a0ff", fg="white", activebackground="#3c6fcf",  font=("Arial", 10, "bold"), 
                  padx=20, command=self.upload_action)
        self.btn_incarca.grid(row=0, column=0, padx=10)
        self.btn_incarca.bind("<Enter>", lambda e: self.btn_incarca.config(bg="#88b5fd"))
        self.btn_incarca.bind("<Leave>", lambda e: self.btn_incarca.config(bg="#61a0ff"))
        
        self.btn_random = tk.Button(self.ctrl_frame, text="RANDOM FOTO", bg="#61a0ff", fg="white", activebackground="#3c6fcf", font=("Arial", 10, "bold"), 
                  padx=20, command=self.random_action)
        self.btn_random.grid(row=0, column=1, padx=10)
        self.btn_random.bind("<Enter>", lambda e: self.btn_random.config(bg="#88b5fd"))
        self.btn_random.bind("<Leave>", lambda e: self.btn_random.config(bg="#61a0ff"))

        self.btn_save = tk.Button(self.ctrl_frame, text="SALVEAZA IMAGINE", bg="#61a0ff", fg="white", activebackground="#3c6fcf", font=("Arial", 10, "bold"), 
                  padx=20, command=self.save_action)
        self.btn_save.grid(row=0, column=2, padx=10)
        self.btn_save.bind("<Enter>", lambda e: self.btn_save.config(bg="#88b5fd"))
        self.btn_save.bind("<Leave>", lambda e: self.btn_save.config(bg="#61a0ff"))

    def process(self, func):
        if self.original_cv is not None:
            # salvez rezultatul in variabila clasei pentru ca sa pot salva ulterior
            self.processed_cv = func(self.original_cv)
            display_res = cv2.resize(self.processed_cv, (450, 450))
            self.show(display_res, self.lbl_proc)
        else:
            messagebox.showwarning("Atentie", "Incarca o imagine mai intai!")

    def save_action(self):
        if self.processed_cv is not None:
            folder_salvare = "imagini_salvate"
            if not os.path.exists(folder_salvare):
                os.makedirs(folder_salvare)
            
            cale_fisier = filedialog.asksaveasfilename(
                initialdir=folder_salvare,
                title="Salveaza imaginea",
                defaultextension=".jpg",
                initialfile="imagine_modificata.jpg",
                filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
            )
            
            if cale_fisier:
                nume_fisier = os.path.basename(cale_fisier)
                if "modificata" not in nume_fisier.lower():
                    nume, ext = os.path.splitext(cale_fisier)
                    cale_fisier = f"{nume}_modificata{ext}"
                
                cv2.imwrite(cale_fisier, self.processed_cv)
                messagebox.showinfo("Succes", f"Imaginea a fost salvata in:\n{cale_fisier}")
        else:
            messagebox.showwarning("Eroare", "Nu exista nicio imagine procesata pentru a fi salvata!")

        # fereastra ajutor

    def open_help_window(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Instructiuni de folosire a aplicatiei")
        help_window.geometry("600x500")
        help_window.configure(bg="#edf1fc", padx=0, pady=10)

        title_label = tk.Label(help_window, text="Manual de Utilizare", bg="#edf1fc",  font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))

        text_ajutor = """
            Aplicatia este conceputa pentru a procesa diferite imagini alese de utilizator. Acesta
        alege efectul sau filtrul dorit.
        1. BLUR GAUSSIAN => Blurul imaginii este mai scazut, reduce zgomotul
        2. BLUR STACK => Blurul imagiini este mai ridicat, reduce zgomotul
        3. ALB-NEGRU => Transforma intr-o imagine alb-negru
        4. ALB-NEGRU (Threshold) => Efect de alb negru pur pentru ca se separa pixelii in 
        functie de o valoare prag
        5. CONTUR (Canny) => Vor aparea doar mariginile obiectelor
        6. ROTIRE 90 => Rotirea imaginii 90 de grade la stanga
        7. ROTIRE 45 => Rotirea imagini 45 de grade la dreapta, cu ajutorul matricei de rotatie
        8. VARTEJ => Da imaginii efectul de Twirl
        9. VALURI => Da imaginii efectul de valuri
        10. OGLINDIRE => Imaginea este vazuta in oglinda
        11. PIXELI => Imaginea este pixelata
        12. CLARITATE => Clarifica imaginea
        13. RAMA => Ii pune imaginii un frame albastru
        14. DRAW => Deseneaza pe imagine doua linii in X
        15. WATERMARK => Adauga un watermark pe imagine
        16. ZOOM => Mareste imaginea in centru
        
                                                Optiuni noi, in curand...
        """
        
        msg = tk.Label(help_window, text=text_ajutor, bg="#edf1fc", justify="left", font=("Arial", 10))
        msg.pack(expand=True, fill="both")

        # buton inchidere fereastra
        self.btn_fereastra = tk.Button(help_window, text="AM INTELES", bg="#61a0ff", fg="white", activebackground="#3c6fcf", font=("Arial", 10, "bold"), command=help_window.destroy)
        self.btn_fereastra.pack(pady=10)
        self.btn_fereastra.bind("<Enter>", lambda e: self.btn_fereastra.config(bg="#88b5fd"))
        self.btn_fereastra.bind("<Leave>", lambda e: self.btn_fereastra.config(bg="#61a0ff"))

    def show(self, img, target):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        target.config(image=img_tk, text="")
        target.image = img_tk

    def upload_action(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_cv = script.load_image(path)
            self.show(self.original_cv, self.lbl_orig)

    def random_action(self):
        path = script.get_random_image("imagini_test")
        if path:
            self.original_cv = script.load_image(path)
            self.show(self.original_cv, self.lbl_orig)
        else:
            messagebox.showinfo("Folder gol", "Adauga poze in folderul 'imagini_test'")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
