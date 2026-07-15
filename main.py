import sys
import os
import threading
import time

def _animate_splash():
    try:
        import pyi_splash
        dots = 1
        while pyi_splash.is_alive():
            pyi_splash.update_text("Cargando" + "." * dots)
            dots = (dots % 3) + 1
            time.sleep(0.4)
    except Exception:
        pass

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    threading.Thread(target=_animate_splash, daemon=True).start()

import customtkinter as ctk
import yt_dlp
import threading
import os
import requests
import subprocess
import shutil
import urllib.request
import urllib.error
import urllib.parse
import json
import sys
from tkinter import filedialog
from io import BytesIO
from PIL import Image
import imageio_ffmpeg
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
try:
    from plyer import notification
except ImportError:
    pass

APP_VERSION = "1.3.6"
GITHUB_REPO = "otkpetare100-ux/aerodownloaderpro"

def cleanup_old_exe():
    import time
    old_exe = sys.executable + ".old"
    for _ in range(5):
        if os.path.exists(old_exe):
            try:
                os.remove(old_exe)
                break
            except Exception:
                time.sleep(1)

import threading
threading.Thread(target=cleanup_old_exe, daemon=True).start()

# Configuración Premium
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aero Downloader - Premium")
        import os
        import sys
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
            
        icon_path = os.path.join(base_path, "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
            
        # Centrar la ventana en la pantalla
        window_width = 900
        window_height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.resizable(False, False)
        
        # Colores personalizados para un look premium
        self.bg_color = "#0f0f13"
        self.card_color = "#1a1a24"
        self.card_border = "#2b2b36"
        self.accent_color = "#00B4DB" 
        self.accent_hover = "#0083B0"
        
        self.configure(fg_color=self.bg_color)
        
        # Configurar grid principal (3 filas ahora: titlebar, header, main content)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Titlebar
        self.grid_rowconfigure(1, weight=0) # Header
        self.grid_rowconfigure(2, weight=1) # Main content

        self.bind_all("<Button-1>", self.check_click_outside)

        # Variables Globales de Estado
        self.url_var = ctk.StringVar()
        self.format_var = ctk.StringVar(value="")
        self.enable_sound = ctk.BooleanVar(value=True)
        self.enable_notif = ctk.BooleanVar(value=True)
        self.video_info = None
        self.available_formats = {}
        self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        
        # Manejo robusto de carpeta de descargas
        self.download_folder = os.environ.get('USERPROFILE')
        if self.download_folder:
            self.download_folder = os.path.join(self.download_folder, 'Downloads')
        else:
            self.download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
            
        if not os.path.exists(self.download_folder):
            try:
                os.makedirs(self.download_folder)
            except:
                pass

        # Construcción de Interfaz Modular
        self.overrideredirect(True)
        self.setup_titlebar()
        self.setup_header()
        self.setup_help_popup()
        self.setup_settings_popup()
        self.setup_main_tabs()
        self.setup_web_tab()
        self.setup_local_extractor_ui()
        self.setup_bridge_tab()

        # Iniciar Aero Bridge (Integración de Navegador)
        self.start_bridge_server()
        
        # Variables de estado para tooltips
        self._tooltip_after_id = None
        self._tooltip_win = None
        
        # Cerrar el Splash Screen de PyInstaller (la ventanita de carga) y hacer fade-in
        try:
            import pyi_splash
            pyi_splash.close()
        except ImportError:
            pass
            
        self.attributes("-alpha", 0.0)
        self.after(100, self.fade_in)

    def fade_in(self):
        current_alpha = self.attributes("-alpha")
        if current_alpha < 1.0:
            self.attributes("-alpha", min(1.0, current_alpha + 0.08))
            self.after(25, self.fade_in)
        else:
            self.attributes("-topmost", False)

    # ==========================================
    # UI SETUP
    # ==========================================

    def setup_titlebar(self):
        self.title_bar = ctk.CTkFrame(self, fg_color="#101014", corner_radius=0, height=35)
        self.title_bar.grid(row=0, column=0, sticky="ew")
        self.title_bar.grid_columnconfigure(0, weight=1)
        
        # Logo y Titulo
        self.title_label = ctk.CTkLabel(self.title_bar, text=f"   Aero Downloader PRO v{APP_VERSION}", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray70")
        self.title_label.grid(row=0, column=0, sticky="w", padx=10)
        
        # Botones de Control
        self.btn_min = ctk.CTkButton(self.title_bar, text="—", width=40, height=35, fg_color="transparent", hover_color=self.card_border, text_color="white", corner_radius=0, command=lambda: self.wm_state('iconic'))
        self.btn_min.grid(row=0, column=1)
        
        self.btn_close = ctk.CTkButton(self.title_bar, text="✕", width=40, height=35, fg_color="transparent", hover_color="#e81123", text_color="white", corner_radius=0, command=lambda: os._exit(0))
        self.btn_close.grid(row=0, column=2)

        # Lógica de arrastre (Drag)
        self._drag_data = {"x": 0, "y": 0}

        def start_drag(event):
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

        def stop_drag(event):
            self._drag_data["x"] = None
            self._drag_data["y"] = None

        def do_drag(event):
            if self._drag_data["x"] is not None and self._drag_data["y"] is not None:
                x = self.winfo_x() - self._drag_data["x"] + event.x
                y = self.winfo_y() - self._drag_data["y"] + event.y
                self.geometry(f"+{x}+{y}")

        self.title_bar.bind("<ButtonPress-1>", start_drag)
        self.title_bar.bind("<ButtonRelease-1>", stop_drag)
        self.title_bar.bind("<B1-Motion>", do_drag)
        self.title_label.bind("<ButtonPress-1>", start_drag)
        self.title_label.bind("<ButtonRelease-1>", stop_drag)
        self.title_label.bind("<B1-Motion>", do_drag)
        
        # Recuperar el comportamiento en la barra de tareas en Windows usando ctypes (Fix para overrideredirect)
        try:
            import ctypes
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except Exception:
            pass

    def setup_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=1, column=0, pady=(30, 20), padx=40, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        logo_path = r"C:\Users\Nanami\Downloads\Logo_Aero_Transparent.png"
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            aspect = img.width / img.height
            new_height = 55
            new_width = int(new_height * aspect)
            self.logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(new_width, new_height))
            self.logo_label = ctk.CTkLabel(self.header_frame, text="", image=self.logo_img)
            self.logo_label.grid(row=0, column=0, sticky="w")
        else:
            self.title_label = ctk.CTkLabel(self.header_frame, text="Aero Downloader", font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color="white")
            self.title_label.grid(row=0, column=0, sticky="w")
            
            self.subtitle_label = ctk.CTkLabel(self.header_frame, text="PRO", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=self.accent_color)
            self.subtitle_label.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="sw")

        # Botones de Acción (?, 📁, ⚙) ordenados por relevancia
        self.btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.btn_frame.grid(row=0, column=2, sticky="e")
        
        self.folder_btn = ctk.CTkButton(self.btn_frame, text="📁", width=34, height=34, font=ctk.CTkFont(family="Segoe UI Emoji", size=20), fg_color="transparent", text_color="gray50", hover_color=self.bg_color, command=lambda: os.startfile(self.download_folder) if os.path.exists(self.download_folder) else None)
        self.folder_btn.pack(side="left", padx=4)
        self.folder_btn.bind("<Enter>", lambda e: self.show_tooltip(self.folder_btn, "Abrir Descargas"))
        self.folder_btn.bind("<Leave>", lambda e: self.hide_tooltip())
        
        self.settings_btn = ctk.CTkButton(self.btn_frame, text="⚙", width=34, height=34, font=ctk.CTkFont(size=22), fg_color="transparent", text_color="gray50", hover_color=self.bg_color, command=self.toggle_settings)
        self.settings_btn.pack(side="left", padx=4)
        self.settings_btn.bind("<Enter>", lambda e: self.show_tooltip(self.settings_btn, "Configuración"))
        self.settings_btn.bind("<Leave>", lambda e: self.hide_tooltip())

    def setup_help_popup(self):
        self.help_popup = ctk.CTkFrame(self, fg_color=self.card_color, corner_radius=10, border_width=1, border_color=self.card_border)
        self.help_visible = False
        
        self.help_label = ctk.CTkLabel(self.help_popup, text="", font=ctk.CTkFont(size=13), justify="left", wraplength=300, text_color="gray80")
        self.help_label.pack(padx=20, pady=20)
        
        # Cerrar automáticamente al quitar el ratón
        self.help_popup.bind("<Leave>", self.check_help_leave)
        self.help_label.bind("<Leave>", self.check_help_leave)

    def check_help_leave(self, event=None):
        if not self.help_visible:
            return
        # Esperar un instante para obtener las coordenadas correctas
        self.after(50, self._do_check_help_leave)
        
    def _do_check_help_leave(self):
        if not self.help_visible:
            return
        x, y = self.winfo_pointerxy()
        x0 = self.help_popup.winfo_rootx()
        y0 = self.help_popup.winfo_rooty()
        x1 = x0 + self.help_popup.winfo_width()
        y1 = y0 + self.help_popup.winfo_height()
        
        # Si el ratón está fuera del recuadro, cerramos
        if not (x0 <= x <= x1 and y0 <= y <= y1):
            self.toggle_help()

    def setup_main_tabs(self):
        self.main_tabs = ctk.CTkTabview(
            self, 
            segmented_button_fg_color="#121218",
            segmented_button_selected_color=self.accent_color, 
            segmented_button_selected_hover_color=self.accent_hover,
            segmented_button_unselected_color="#121218",
            segmented_button_unselected_hover_color="#1e1e24",
            text_color="white", # Increased contrast
            corner_radius=12,
            command=self.on_tab_change
        )
        self.main_tabs.grid(row=2, column=0, padx=40, pady=(0, 20), sticky="nsew")
        self.main_tabs._segmented_button.configure(font=ctk.CTkFont(size=15, weight="bold"))
        
        self.main_tabs.add("Descarga Web")
        self.main_tabs.add("Extraer Audio")
        self.main_tabs.add("Aero Bridge")
        
        self.main_tabs.tab("Descarga Web").grid_columnconfigure(0, weight=1)
        self.main_tabs.tab("Descarga Web").grid_rowconfigure(1, weight=1)
        self.main_tabs.tab("Extraer Audio").grid_columnconfigure(0, weight=1)
        self.main_tabs.tab("Aero Bridge").grid_columnconfigure(0, weight=1)
        
        # Vincular click para la ayuda
        for tab_name, btn in self.main_tabs._segmented_button._buttons_dict.items():
            btn.bind("<Button-1>", lambda e, name=tab_name: self.on_tab_clicked(e, name))
            
        # Poner el texto [?] en la pestaña inicial
        self.main_tabs._segmented_button._buttons_dict["Descarga Web"].configure(text="Descarga Web [?]")

    def on_tab_clicked(self, event, tab_name):
        if self.main_tabs.get() == tab_name:
            # Calcular posición X relativa a la ventana
            click_x = event.x_root - self.winfo_rootx()
            self.toggle_help(x_pos=click_x)

    def on_tab_change(self):
        tab = self.main_tabs.get()
        # Actualizar textos
        for name, btn in self.main_tabs._segmented_button._buttons_dict.items():
            if name == tab:
                btn.configure(text=f"{name} [?]")
            else:
                btn.configure(text=name)
        
        # Cerrar popup si cambian de tab
        if self.help_visible:
            self.toggle_help()

    def setup_web_tab(self):
        web_tab = self.main_tabs.tab("Descarga Web")
        
        # Tarjeta de Búsqueda
        self.search_card = ctk.CTkFrame(web_tab, fg_color=self.card_color, corner_radius=15, border_width=1, border_color=self.card_border)
        self.search_card.grid(row=0, column=0, pady=(10, 20), sticky="ew")
        self.search_card.grid_columnconfigure(0, weight=1)
        
        self.url_entry = ctk.CTkEntry(self.search_card, textvariable=self.url_var, placeholder_text="Pega la URL del video aquí...", font=ctk.CTkFont(size=14), height=45, corner_radius=8, border_color="#333344", fg_color="#1e1e24")
        self.url_entry.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="ew")
        
        self.search_btn = ctk.CTkButton(self.search_card, text="Buscar Video", font=ctk.CTkFont(size=14, weight="bold"), height=45, width=120, corner_radius=8, fg_color=self.accent_color, hover_color=self.accent_hover, text_color="white", text_color_disabled="#f3f4f6", command=self.search_media)
        self.search_btn.grid(row=0, column=1, padx=(0, 20), pady=20)

        self.search_progress = ctk.CTkProgressBar(self.search_card, mode="indeterminate", width=300, height=6, fg_color="#2b2b36", progress_color=self.accent_color)
        self.search_progress.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        self.search_progress.grid_remove()

        # Tarjeta de Resultados
        self.result_card = ctk.CTkFrame(web_tab, fg_color=self.card_color, corner_radius=15, height=450, border_width=1, border_color=self.card_border)
        self.result_card.grid(row=1, column=0, pady=(0, 10), sticky="nsew")
        self.result_card.grid_propagate(False)
        self.result_card.grid_columnconfigure(1, weight=1)
        self.result_card.grid_rowconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(self.result_card, text="Esperando enlace...", font=ctk.CTkFont(size=16), text_color="gray50")
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")

        self.left_col = ctk.CTkFrame(self.result_card, fg_color="transparent")
        self.right_col = ctk.CTkFrame(self.result_card, fg_color="transparent")

        self.thumb_label = ctk.CTkLabel(self.left_col, text="", width=384, height=216, fg_color="#121218", corner_radius=12)
        self.thumb_label.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        self.download_thumb_btn = ctk.CTkButton(self.left_col, text="Descargar Miniatura", height=35, font=ctk.CTkFont(size=12, weight="bold"), fg_color="#2b2b36", hover_color="#3a3a48", command=self.download_thumbnail)
        self.download_thumb_btn.grid(row=1, column=0, pady=(0, 20))
        self.download_thumb_btn.grid_remove()

        self.right_col.grid_columnconfigure(0, weight=1)
        self.right_col.grid_rowconfigure(1, weight=1)
        
        self.video_title_label = ctk.CTkLabel(self.right_col, text="", font=ctk.CTkFont(size=18, weight="bold"), wraplength=350, justify="left", text_color="white")
        self.video_title_label.grid(row=0, column=0, pady=(20, 10), padx=(0, 20), sticky="nw")

        self.tabview = ctk.CTkTabview(
            self.right_col, height=350, 
            segmented_button_fg_color="#1e1e24",
            segmented_button_selected_color=self.accent_color, 
            segmented_button_selected_hover_color=self.accent_hover,
            segmented_button_unselected_color="#1e1e24",
            segmented_button_unselected_hover_color="#2b2b36",
            text_color="gray80",
            corner_radius=10
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=(0, 20), pady=(0, 10))
        self.tabview._segmented_button.configure(font=ctk.CTkFont(size=13, weight="bold"))
        self.tabview.add("Video")
        self.tabview.add("Audio")

        self.video_scroll = ctk.CTkScrollableFrame(self.tabview.tab("Video"), fg_color="transparent", scrollbar_button_color=self.accent_color, scrollbar_button_hover_color=self.accent_hover)
        self.video_scroll.pack(fill="both", expand=True)

        self.audio_scroll = ctk.CTkScrollableFrame(self.tabview.tab("Audio"), fg_color="transparent", scrollbar_button_color=self.accent_color, scrollbar_button_hover_color=self.accent_hover)
        self.audio_scroll.pack(fill="both", expand=True)
        
        try:
            shadow_top_img = ctk.CTkImage(light_image=Image.open("shadow_top.png"), dark_image=Image.open("shadow_top.png"), size=(400, 30))
            shadow_bot_img = ctk.CTkImage(light_image=Image.open("shadow_bottom.png"), dark_image=Image.open("shadow_bottom.png"), size=(400, 30))
            
            # Sombras para la pestaña Video
            self.shadow_v_top = ctk.CTkLabel(self.tabview.tab("Video"), text="", image=shadow_top_img, fg_color="transparent")
            self.shadow_v_top.place(relx=0, rely=0, relwidth=0.95, height=30)
            self.shadow_v_bot = ctk.CTkLabel(self.tabview.tab("Video"), text="", image=shadow_bot_img, fg_color="transparent")
            self.shadow_v_bot.place(relx=0, rely=1.0, anchor="sw", relwidth=0.95, height=30)
            
            # Sombras para la pestaña Audio
            self.shadow_a_top = ctk.CTkLabel(self.tabview.tab("Audio"), text="", image=shadow_top_img, fg_color="transparent")
            self.shadow_a_top.place(relx=0, rely=0, relwidth=0.95, height=30)
            self.shadow_a_bot = ctk.CTkLabel(self.tabview.tab("Audio"), text="", image=shadow_bot_img, fg_color="transparent")
            self.shadow_a_bot.place(relx=0, rely=1.0, anchor="sw", relwidth=0.95, height=30)
        except Exception:
            pass

        self.format_radios = []

        self.progress_bar = ctk.CTkProgressBar(self.right_col, height=8, fg_color="#2b2b36", progress_color=self.accent_color)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=(0, 20), pady=(0, 20))
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()
        
        self.status_label = ctk.CTkLabel(self.right_col, text="", font=ctk.CTkFont(size=11), text_color="gray50")
        self.status_label.grid(row=3, column=0, sticky="ew", padx=(0, 20), pady=(0, 10))
        self.status_label.grid_remove()

    def setup_local_extractor_ui(self):
        local_tab = self.main_tabs.tab("Extraer Audio")
        
        card = ctk.CTkFrame(local_tab, fg_color=self.card_color, corner_radius=15, border_width=1, border_color=self.card_border)
        card.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(card, text="Extractor de Audio Local", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        title.pack(pady=(30, 10))
        
        desc = ctk.CTkLabel(card, text="Selecciona un archivo de video de tu computadora para extraerle el audio en su calidad original.", text_color="gray70")
        desc.pack(pady=(0, 30))
        
        self.local_file_path = None
        self.local_file_btn = ctk.CTkButton(card, text="Seleccionar Video...", height=40, fg_color="#2b2b36", hover_color="#3a3a48", command=self.select_local_video)
        self.local_file_btn.pack(pady=10)
        
        self.local_file_label = ctk.CTkLabel(card, text="Ningún archivo seleccionado", text_color="gray50")
        self.local_file_label.pack(pady=(0, 20))
        
        self.local_format_var = ctk.StringVar(value="MP3")
        self.local_format_seg = ctk.CTkSegmentedButton(card, values=["MP3", "M4A"], variable=self.local_format_var, selected_color=self.accent_color, selected_hover_color=self.accent_hover)
        self.local_format_seg.pack(pady=10)
        
        self.local_extract_btn = ctk.CTkButton(card, text="Extraer Audio", height=45, width=200, font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.accent_color, hover_color=self.accent_hover, text_color="white", text_color_disabled="#f3f4f6", state="disabled", command=self.start_local_extraction)
        self.local_extract_btn.pack(pady=(20, 10))
        
        self.local_progress = ctk.CTkProgressBar(card, mode="indeterminate", width=300, height=6, fg_color="#2b2b36", progress_color=self.accent_color)
        self.local_progress.pack(pady=10)
        self.local_progress.pack_forget()
        
        self.local_status = ctk.CTkLabel(card, text="", text_color="gray50")
        self.local_status.pack(pady=(0, 20))

    def setup_bridge_tab(self):
        bridge_tab = self.main_tabs.tab("Aero Bridge")
        
        card = ctk.CTkFrame(bridge_tab, fg_color=self.card_color, corner_radius=15, border_width=1, border_color=self.card_border)
        card.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(card, text="Extensión Oficial Aero Bridge", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        title.grid(row=0, column=0, pady=(30, 10))
        
        desc = ctk.CTkLabel(card, text="Añade nuestra extensión a tu navegador para enviar videos con 1 clic.\n(Soporta Auto-Arranque de la aplicación).", text_color="gray70", wraplength=500)
        desc.grid(row=1, column=0, pady=(0, 20))

        # Paso 1
        step1_title = ctk.CTkLabel(card, text="Paso 1: Activar Modo Desarrollador", font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
        step1_title.grid(row=2, column=0, pady=(0, 5))
        
        step1_desc = ctk.CTkLabel(card, text="Abre tu navegador (Chrome/Edge/Brave), ve a la ventana de\nExtensiones y activa el interruptor 'Modo de desarrollador'.", text_color="gray70")
        step1_desc.grid(row=3, column=0, pady=(0, 20))

        # Paso 2
        step2_title = ctk.CTkLabel(card, text="Paso 2: Cargar la Extensión", font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
        step2_title.grid(row=4, column=0, pady=(0, 5))
        
        step2_desc = ctk.CTkLabel(card, text="Haz clic abajo para abrir la carpeta. Luego, en tu navegador haz clic en\n'Cargar extensión sin empaquetar' y selecciona la carpeta 'extension'.", text_color="gray70")
        step2_desc.grid(row=5, column=0, pady=(0, 10))
        
        ext_path = self.get_extension_path()
        step2_btn = ctk.CTkButton(card, text="Abrir Carpeta de la Extensión", height=45, width=240, font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.accent_color, hover_color=self.accent_hover, text_color="white", command=lambda: os.startfile(ext_path) if os.path.exists(ext_path) else None)
        step2_btn.grid(row=6, column=0, pady=(0, 20))
        
        # Indicador de estado con pulso animado
        status_frame = ctk.CTkFrame(card, fg_color="transparent")
        status_frame.grid(row=7, column=0, pady=(0, 20))
        self.bridge_pulse_label = ctk.CTkLabel(status_frame, text="●", font=ctk.CTkFont(size=10), text_color="#10B981")
        self.bridge_pulse_label.pack(side="left", padx=(0, 6))
        ctk.CTkLabel(status_frame, text="Protocolo aerodl:// y Servidor Bridge ACTIVOS", font=ctk.CTkFont(size=12, weight="bold"), text_color="#10B981").pack(side="left")
        self.animate_bridge_pulse()

    # ==========================================
    # LOGIC: POPUPS
    # ==========================================

    def check_click_outside(self, event):
        # Cerramos los popups si el click no fue en ellos ni en sus respectivos botones
        if self.settings_visible:
            widget_path = str(event.widget)
            if widget_path != str(self.settings_btn) and str(self.settings_popup) not in widget_path:
                self.toggle_settings()
                
        if self.help_visible:
            widget_path = str(event.widget)
            if widget_path != str(self.help_btn) and str(self.help_popup) not in widget_path:
                self.toggle_help()

    def setup_settings_popup(self):
        self.settings_popup = ctk.CTkFrame(self, fg_color=self.card_color, corner_radius=12, border_width=1, border_color="#374151")
        self.settings_visible = False
        
        # Header
        header_frame = ctk.CTkFrame(self.settings_popup, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        icon_lbl = ctk.CTkLabel(header_frame, text="⚙️", font=ctk.CTkFont(size=18))
        icon_lbl.pack(side="left", padx=(0, 10))
        
        lbl = ctk.CTkLabel(header_frame, text="Configuración Avanzada", font=ctk.CTkFont(size=15, weight="bold"), text_color="white")
        lbl.pack(side="left")
        
        # Opciones
        options_frame = ctk.CTkFrame(self.settings_popup, fg_color="#1F2937", corner_radius=8)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        # Switch de Sonido
        self.sound_switch = ctk.CTkSwitch(options_frame, text="Sonidos de interfaz", variable=self.enable_sound, onvalue=True, offvalue=False, progress_color=self.accent_color, font=ctk.CTkFont(size=13))
        self.sound_switch.pack(padx=15, pady=(15, 10), fill="x")
        
        # Switch de Notificaciones
        self.notif_switch = ctk.CTkSwitch(options_frame, text="Notificaciones push", variable=self.enable_notif, onvalue=True, offvalue=False, progress_color=self.accent_color, font=ctk.CTkFont(size=13))
        self.notif_switch.pack(padx=15, pady=(5, 15), fill="x")
        
        # Separator
        separator = ctk.CTkFrame(self.settings_popup, height=1, fg_color="#374151")
        separator.pack(fill="x", padx=20, pady=10)
        
        # Update App Button
        self.update_engine_btn = ctk.CTkButton(self.settings_popup, text="🔄 Buscar Actualizaciones", font=ctk.CTkFont(size=13, weight="bold"), height=36, fg_color="#374151", hover_color="#4B5563", text_color="white", text_color_disabled="white", command=self.check_app_updates)
        self.update_engine_btn.pack(padx=20, pady=(5, 10), fill="x")
        
        # Barra de progreso de actualización (oculta por defecto)
        self.update_progress_bar = ctk.CTkProgressBar(self.settings_popup, height=5, fg_color="#1F2937", progress_color=self.accent_color)
        self.update_progress_bar.pack(padx=20, pady=(0, 15), fill="x")
        self.update_progress_bar.set(0)
        self.update_progress_bar.pack_forget()

    def toggle_settings(self):
        if self.settings_visible:
            self.settings_popup.place_forget()
            self.settings_visible = False
            self.settings_btn.configure(text_color="gray50")
        else:
            if self.help_visible:
                self.toggle_help() # Close help if open
            self.settings_popup.place(relx=0.95, rely=0.15, anchor="ne")
            self.settings_popup.lift()
            self.settings_visible = True
            self.settings_btn.configure(text_color="white")

    def check_app_updates(self):
        self.update_engine_btn.configure(state="disabled", text="Buscando actualizaciones...")
        import threading
        thread = threading.Thread(target=self.check_app_updates_thread, daemon=True)
        thread.start()

    def check_app_updates_thread(self):
        try:
            import json
            import urllib.request
            import os
            import sys
            import subprocess
            
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = urllib.request.Request(url, headers={'User-Agent': 'AeroDownloader-Updater'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            latest_version = data.get("tag_name", "").lstrip("v")
            
            # Comparación numérica de versiones para evitar downgrades
            def parse_version(v):
                return tuple(int(x) for x in v.split('.'))
            
            if latest_version and parse_version(latest_version) > parse_version(APP_VERSION):
                self.after(0, lambda: self.update_engine_btn.configure(text=f"Descargando v{latest_version}..."))
                
                # Buscar el asset .exe
                exe_url = None
                for asset in data.get("assets", []):
                    if asset.get("name", "").endswith(".exe"):
                        exe_url = asset.get("browser_download_url")
                        break
                        
                if exe_url:
                    # Mostrar barra de progreso real de la descarga
                    self.after(0, lambda: self.update_progress_bar.pack(padx=20, pady=(0, 15), fill="x"))
                    self.after(0, lambda: self.update_progress_bar.set(0))
                    
                    import tempfile
                    new_exe_path = os.path.join(tempfile.gettempdir(), "AeroDownloader_Setup.exe")
                    
                    self._last_update_pct = -1
                    def progress_callback(block_num, block_size, total_size):
                        if total_size > 0:
                            pct = min(block_num * block_size / total_size, 1.0)
                            pct_int = int(pct * 100)
                            if pct_int > self._last_update_pct:
                                self._last_update_pct = pct_int
                                self.after(0, lambda p=pct, pi=pct_int: (
                                    self.update_progress_bar.set(p),
                                    self.update_engine_btn.configure(text=f"Descargando... {pi}%")
                                ))
                    
                    urllib.request.urlretrieve(exe_url, new_exe_path, reporthook=progress_callback)
                    
                    self.after(0, lambda: self.update_engine_btn.configure(text="¡Instalando actualización...", fg_color=self.accent_color))
                    self.after(0, lambda: self.update_progress_bar.set(1.0))
                    
                    # Lanzar el instalador en modo silencioso y cerrar la app
                    subprocess.Popen([new_exe_path, "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/CLOSEAPPLICATIONS", "/FORCECLOSEAPPLICATIONS"])
                    self.after(500, self.fade_out_and_exit)
                else:
                    self.after(0, lambda: self.update_engine_btn.configure(text="No se encontró instalador", fg_color="#EF4444"))
                    self.after(4000, lambda: self.reset_update_btn())
            else:
                self.after(0, lambda: self.update_engine_btn.configure(text="Ya tienes la última versión", fg_color=self.accent_color, text_color="white", state="normal"))
                self.after(4000, lambda: self.reset_update_btn())
                
        except Exception as e:
            self.after(0, lambda: self.update_engine_btn.configure(text="Error al buscar updates", fg_color="#EF4444"))
            self.after(4000, lambda: self.reset_update_btn())
        
    def reset_update_btn(self):
        if self.update_engine_btn.winfo_exists():
            self.update_engine_btn.configure(text="🔄 Buscar Actualizaciones", state="normal", fg_color="#374151", text_color="white")

    def toggle_help(self, x_pos=None):
        if self.help_visible:
            self.help_popup.place_forget()
            self.help_visible = False
        else:
            if x_pos is None:
                x_pos = self.winfo_width() / 2
                
            # Restringir x_pos para que la ventana no se salga de los bordes
            # Ancho del popup ~340px (mitad = 170)
            popup_half_width = 170
            max_x = self.winfo_width() - popup_half_width - 20
            min_x = popup_half_width + 20
            x_pos = max(min_x, min(max_x, x_pos))
            
            if self.settings_visible:
                self.toggle_settings() # Close settings if open
            current_tab = self.main_tabs.get()
            if current_tab == "Descarga Web":
                info_text = (
                    "Aero Downloader PRO es una herramienta universal.\n\n"
                    "Plataformas compatibles:\n"
                    "• YouTube (Videos, Shorts, Listas)\n"
                    "• Twitter / X\n"
                    "• TikTok\n"
                    "• Instagram (Reels y Posts)\n"
                    "• Facebook, Twitch, Reddit, Vimeo\n"
                    "• ... ¡Y cientos de sitios más!\n\n"
                    "Pega el enlace y la aplicación extraerá todas las calidades automáticamente."
                )
            elif current_tab == "Extraer Audio":
                info_text = (
                    "Extractor de Audio Local PRO.\n\n"
                    "Extrae el audio de videos que ya tienes en tu computadora.\n\n"
                    "Formatos de video soportados:\n"
                    "• MP4, MKV, AVI, MOV, FLV, WEBM\n\n"
                    "Formatos de salida:\n"
                    "• MP3: Compresión a formato universal en alta calidad.\n"
                    "• M4A: Extracción de la pista original sin pérdida y muy rápido."
                )
            else:
                info_text = (
                    "Aero Bridge - Conexión con Navegadores\n\n"
                    "Instala la extensión para enviar descargas al instante.\n\n"
                    "¿Cómo funciona?\n"
                    "1. Carga la extensión en tu navegador basado en Chromium.\n"
                    "2. Abre cualquier video en la web.\n"
                    "3. Toca el ícono de la extensión.\n\n"
                    "El enlace se mandará de forma automática y silenciosa a la aplicación."
                )
            self.help_label.configure(text=info_text)

            # Posicionar el popup debajo de las pestañas centrada en el clic
            self.help_popup.place(x=x_pos, rely=0.15, anchor="n")
            self.help_popup.lift()
            self.help_visible = True
            
            # Si el ratón ya estaba lejos cuando se abrió (ej: por clic rápido),
            # no lo cerramos inmediatamente, dejamos que el usuario interactúe.

    # ==========================================
    # LOGIC: AERO BRIDGE SERVER
    # ==========================================
    
    def start_bridge_server(self):
        class BridgeHandler(BaseHTTPRequestHandler):
            app_instance = self
            
            def do_OPTIONS(self):
                self.send_response(200, "ok")
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
                self.end_headers()

            def do_GET(self):
                parsed_path = urllib.parse.urlparse(self.path)
                
                # Servir el script de Tampermonkey
                if parsed_path.path == '/script.user.js':
                    try:
                        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aero_youtube.user.js")
                        with open(script_path, "r", encoding="utf-8") as f:
                            script_content = f.read()
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/javascript; charset=utf-8')
                        self.end_headers()
                        self.wfile.write(script_content.encode('utf-8'))
                    except Exception as e:
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(b'Error reading script')
                    return

                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                query = urllib.parse.parse_qs(parsed_path.query)
                
                if 'url' in query:
                    video_url = query['url'][0]
                    self.app_instance.after(0, self.app_instance.receive_bridge_url, video_url)
                    self.wfile.write(b'{"status": "success"}')
                else:
                    self.wfile.write(b'{"status": "no url provided"}')
                    
            def log_message(self, format, *args):
                pass
                
        def run_server():
            try:
                server = HTTPServer(('127.0.0.1', 65432), BridgeHandler)
                server.serve_forever()
            except Exception as e:
                print("Bridge server error:", e)
                
        threading.Thread(target=run_server, daemon=True).start()

    def receive_bridge_url(self, url):
        self.main_tabs.set("Descarga Web")
        self.url_var.set(url)
        self.search_media()
        # Bring window to front
        self.deiconify()
        self.attributes('-topmost', 1)
        self.attributes('-topmost', 0)

    # ==========================================
    # LOGIC: LOCAL AUDIO EXTRACTION
    # ==========================================

    def select_local_video(self):
        filetypes = [("Archivos de video", "*.mp4 *.mkv *.avi *.mov *.webm *.flv"), ("Todos los archivos", "*.*")]
        filepath = filedialog.askopenfilename(title="Selecciona un video", filetypes=filetypes)
        if filepath:
            self.local_file_path = filepath
            filename = os.path.basename(filepath)
            self.local_file_label.configure(text=filename, text_color="white")
            self.local_extract_btn.configure(state="normal")
            self.local_status.configure(text="")
            
    def start_local_extraction(self):
        if not self.local_file_path:
            return
        
        self.local_extract_btn.configure(state="disabled", text="Extrayendo...")
        self.local_progress.pack(pady=10)
        self.local_progress.start()
        self.local_status.configure(text="Procesando archivo local...", text_color="white")
        
        thread = threading.Thread(target=self.extract_local_audio_thread, daemon=True)
        thread.start()

    def extract_local_audio_thread(self):
        try:
            filename = os.path.basename(self.local_file_path)
            name_only, _ = os.path.splitext(filename)
            fmt = self.local_format_var.get().lower()
            output_path = os.path.join(self.download_folder, f"{name_only}.{fmt}")
            
            while os.path.exists(output_path):
                import random
                output_path = os.path.join(self.download_folder, f"{name_only}_{random.randint(1000,9999)}.{fmt}")

            if fmt == "mp3":
                cmd = [self.ffmpeg_path, "-y", "-i", self.local_file_path, "-vn", "-c:a", "libmp3lame", "-q:a", "2", output_path]
            else:
                cmd = [self.ffmpeg_path, "-y", "-i", self.local_file_path, "-vn", "-c:a", "aac", "-b:a", "192k", output_path]
                
            flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, creationflags=flags)
            
            self.after(0, self.update_local_success)
        except Exception as e:
            self.after(0, self.update_local_error, str(e))
            
    def update_local_success(self):
        self.local_progress.stop()
        self.local_progress.pack_forget()
        self.local_extract_btn.configure(state="disabled", text="¡Completado!", fg_color=self.accent_color)
        self.local_status.configure(text="¡Extracción completada! (En Descargas)", text_color=self.accent_color)
        
        if self.enable_sound.get():
            try:
                import winsound
                winsound.PlaySound(r"C:\Windows\Media\Windows Navigation Start.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                pass
        
        if self.enable_notif.get():
            try:
                notification.notify(title="Aero Downloader", message="¡Audio extraído con éxito!", app_name="Aero Downloader", timeout=5)
            except:
                pass
            
        # Restablecer botón tras 4 segundos
        self.after(4000, self.reset_local_btn)
        
    def reset_local_btn(self):
        self.local_extract_btn.configure(state="normal", text="Extraer Audio")
        self.local_status.configure(text="")

    def update_local_error(self, err):
        self.local_progress.stop()
        self.local_progress.pack_forget()
        self.local_extract_btn.configure(state="normal", text="Extraer Audio")
        self.local_status.configure(text="Error al extraer audio.", text_color="#EF4444")

    def get_extension_path(self):
        import os, sys, shutil
        if getattr(sys, 'frozen', False):
            appdata = os.getenv('APPDATA')
            target_ext_dir = os.path.join(appdata, 'AeroDownloader', 'extension')
            meipass_ext_dir = os.path.join(sys._MEIPASS, 'extension')
            if os.path.exists(meipass_ext_dir):
                try:
                    if os.path.exists(target_ext_dir):
                        shutil.rmtree(target_ext_dir)
                    shutil.copytree(meipass_ext_dir, target_ext_dir)
                except Exception:
                    pass
            return target_ext_dir
        else:
            return os.path.abspath("extension")

    # ==========================================
    # LOGIC: EVENT HANDLERS
    # ==========================================

    # ==========================================
    # LOGIC: ANIMATIONS & TOOLTIPS
    # ==========================================

    def show_tooltip(self, widget, text):
        """Muestra un tooltip elegante con fade-in sobre el widget."""
        self.hide_tooltip()
        
        if not hasattr(self, '_tooltip_window') or self._tooltip_window is None:
            import tkinter as tk
            self._tooltip_window = tk.Toplevel(self)
            self._tooltip_window.wm_overrideredirect(True)
            self._tooltip_window.configure(bg="#374151")
            
            self._tooltip_label = tk.Label(self._tooltip_window, text="", font=("Segoe UI", 9), bg="#374151", fg="white", padx=8, pady=4)
            self._tooltip_label.pack()
            
        x = widget.winfo_rootx() + widget.winfo_width() // 2
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        
        self._tooltip_label.configure(text=text)
        self._tooltip_window.wm_geometry(f"+{x}+{y}")
        self._tooltip_window.attributes("-alpha", 0.0)
        self._tooltip_window.attributes("-topmost", True)
        self._tooltip_window.deiconify()
        
        # Guardar ID actual para asegurar que el fade in coincida
        self._current_tooltip_id = id(widget)
        self._fade_in_tooltip(0.0, self._current_tooltip_id)

    def _fade_in_tooltip(self, alpha, tooltip_id):
        if not hasattr(self, '_current_tooltip_id') or self._current_tooltip_id != tooltip_id:
            return
            
        alpha = min(alpha + 0.15, 1.0)
        try:
            self._tooltip_window.attributes("-alpha", alpha)
        except Exception:
            return
            
        if alpha < 1.0:
            self._tooltip_after_id = self.after(20, lambda: self._fade_in_tooltip(alpha, tooltip_id))

    def hide_tooltip(self):
        self._current_tooltip_id = None
        if getattr(self, '_tooltip_after_id', None):
            self.after_cancel(self._tooltip_after_id)
            self._tooltip_after_id = None
        if hasattr(self, '_tooltip_window') and self._tooltip_window:
            self._tooltip_window.withdraw()

    def animate_bridge_pulse(self):
        """Hace que el punto de estado Bridge parpadee suavemente."""
        if not hasattr(self, 'bridge_pulse_label') or not self.bridge_pulse_label.winfo_exists():
            return
        current = self.bridge_pulse_label.cget("text_color")
        next_color = "#6EE7B7" if current == "#10B981" else "#10B981"
        self.bridge_pulse_label.configure(text_color=next_color)
        self.after(900, self.animate_bridge_pulse)

    def fade_out_and_exit(self, alpha=1.0):
        """Desvanece la ventana antes de cerrarla para un cierre elegante."""
        alpha = max(alpha - 0.1, 0.0)
        try:
            self.attributes("-alpha", alpha)
        except Exception:
            pass
        if alpha > 0.0:
            self.after(30, lambda: self.fade_out_and_exit(alpha))
        else:
            os._exit(0)

    def animate_result_in(self):
        """Anima la aparición del panel de resultados con fade-in."""
        self.attributes("-alpha", 1.0)  # Asegurar visibilidad total de la ventana
        self._result_alpha = 0.0
        self.left_col.configure(fg_color="transparent")
        self.right_col.configure(fg_color="transparent")
        self._step_result_fade()

    def _step_result_fade(self):
        self._result_alpha = min(self._result_alpha + 0.12, 1.0)
        # Actualizamos el color de texto del título como proxy del fade
        gray_val = int(self._result_alpha * 255)
        hex_color = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"
        try:
            self.video_title_label.configure(text_color=hex_color)
        except Exception:
            pass
        if self._result_alpha < 1.0:
            self.after(30, self._step_result_fade)
        else:
            self.video_title_label.configure(text_color="white")

    # ==========================================
    # LOGIC: EVENT HANDLERS
    # ==========================================

    def show_result_ui(self):
        self.status_label.place_forget()
        self.left_col.grid(row=0, column=0, sticky="ns")
        self.right_col.grid(row=0, column=1, sticky="nsew")

    def search_media(self):
        url = self.url_var.get()
        if not url:
            return
        
        self.search_btn.configure(state="disabled")
        self.status_label.configure(text="Buscando información...", text_color="white")
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")
        self.left_col.grid_forget()
        self.right_col.grid_forget()
        
        self.search_progress.grid()
        self.search_progress.start()

        thread = threading.Thread(target=self.fetch_video_info_thread, args=(url,), daemon=True)
        thread.start()

    def fetch_video_info_thread(self, url):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': self.ffmpeg_path,
            'extract_flat': False,
            'noplaylist': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            pil_img = None
            if 'thumbnail' in info:
                try:
                    response = requests.get(info['thumbnail'], timeout=10)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        img.thumbnail((384, 216))
                        pil_img = img
                except:
                    pass
            
            title = info.get('title', 'Video sin título')

            formats = info.get('formats', [])
            video_resolutions = set()
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('resolution') and f.get('resolution') != 'audio only':
                    res = f.get('height')
                    if res and res >= 144:  
                        video_resolutions.add(res)
            
            options = []
            new_available_formats = {}
            
            for res in sorted(list(video_resolutions), reverse=True):
                label = f"Video - {res}p HD" if res >= 720 else f"Video - {res}p"
                options.append(label)
                new_available_formats[label] = f"bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/best[height<={res}][ext=mp4]/best"
            
            options.append("Audio - MP3 (Comprimido)")
            new_available_formats["Audio - MP3 (Comprimido)"] = "audio_mp3"

            options.append("Audio - M4A (Original)")
            new_available_formats["Audio - M4A (Original)"] = "audio_m4a"

            self.after(0, self.update_search_success, info, pil_img, title, options, new_available_formats)

        except Exception as e:
            self.after(0, self.update_search_error, str(e))

    def update_search_success(self, info, pil_img, title, options, new_available_formats):
        self.search_progress.stop()
        self.search_progress.grid_remove()
        
        self.video_info = info
        self.available_formats = new_available_formats
        self.show_result_ui()
        self.animate_result_in()

        if pil_img:
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
            self.thumb_label.configure(image=ctk_img, text="")
            self.download_thumb_btn.grid()
        else:
            self.thumb_label.configure(text="Sin miniatura", image="")
            self.download_thumb_btn.grid_remove()
            
        self.video_title_label.configure(text=title)

        if not options:
            options = ["Video (Mejor calidad)"]
            self.available_formats["Video (Mejor calidad)"] = "bestvideo+bestaudio/best"

        for radio in self.format_radios:
            radio.master.destroy()
        self.format_radios.clear()

        for option in options:
            parent_scroll = self.video_scroll if option.startswith("Video") else self.audio_scroll
            
            row_frame = ctk.CTkFrame(parent_scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=8, padx=15)
            
            btn = ctk.CTkButton(row_frame, text=option, font=ctk.CTkFont(size=14, weight="bold"), height=40, fg_color="#2b2b36", hover_color=self.accent_hover, text_color_disabled="white", command=lambda f=option: self.start_download(f))
            btn.pack(side="left", fill="x", expand=True)
            
            x_btn = ctk.CTkButton(row_frame, text="✖", font=ctk.CTkFont(size=16, weight="bold"), width=40, height=40, fg_color="#EF4444", hover_color="#DC2626", text_color="white", command=self.cancel_download)
            btn.x_btn = x_btn
            
            self.format_radios.append(btn)

        self.search_btn.configure(state="normal")

    def update_search_error(self, error_msg):
        self.search_progress.stop()
        self.search_progress.grid_remove()
        
        self.status_label.configure(text="Error: No se pudo encontrar el video. Revisa la URL.", text_color="#EF4444")
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")
        self.left_col.grid_forget()
        self.right_col.grid_forget()
        self.search_btn.configure(state="normal")
        self.progress_bar.grid_remove()

    def download_thumbnail(self):
        if not self.video_info or 'thumbnail' not in self.video_info:
            return
            
        url = self.video_info['thumbnail']
        # Buscar la mayor resolución posible en el array de thumbnails
        if 'thumbnails' in self.video_info and self.video_info['thumbnails']:
            # Ordenar por ancho (width) o preferencia, tomando el último (el mayor)
            best_thumb = max(self.video_info['thumbnails'], key=lambda t: t.get('width', 0) or t.get('preference', -1))
            if 'url' in best_thumb:
                url = best_thumb['url']
        title = self.video_info.get('title', 'thumbnail')
        import re
        clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
        
        output_path = os.path.join(self.download_folder, f"{clean_title}_thumb.jpg")
        if os.path.exists(output_path):
            import random
            output_path = os.path.join(self.download_folder, f"{clean_title}_thumb_{random.randint(1000,9999)}.jpg")
            
        def _dl():
            try:
                self.download_thumb_btn.configure(state="disabled", text="Descargando...")
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    self.after(0, lambda: self.download_thumb_btn.configure(text="¡Completado!"))
                    if self.enable_sound.get():
                        try:
                            import winsound
                            winsound.PlaySound(r"C:\Windows\Media\Windows Navigation Start.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                        except Exception:
                            pass
                    
                    if self.enable_notif.get():
                        try:
                            notification.notify(title="Aero Downloader", message="¡Miniatura descargada con éxito!", app_name="Aero Downloader", timeout=5)
                        except:
                            pass
                    self.after(3000, lambda: self.download_thumb_btn.configure(state="normal", text="Descargar Miniatura"))
                else:
                    self.after(0, lambda: self.download_thumb_btn.configure(state="normal", text="Descargar Miniatura"))
            except:
                self.after(0, lambda: self.download_thumb_btn.configure(state="normal", text="Descargar Miniatura"))

        threading.Thread(target=_dl, daemon=True).start()

    def update_progress(self, percent, status_text=""):
        self.progress_bar.set(percent)
        if status_text:
            self.status_label.configure(text=status_text)

    def progress_hook(self, d):
        if 'filename' in d:
            if not hasattr(self, 'current_downloading_files'):
                self.current_downloading_files = set()
            self.current_downloading_files.add(d['filename'])
            
        if getattr(self, 'cancel_download_flag', False):
            raise Exception("Descarga Cancelada por el Usuario")
            
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            
            if total > 0:
                percent = downloaded / total
                status_text = f"Descargando... {speed} - Faltan {eta}"
                self.after(0, self.update_progress, percent, status_text)
        elif d['status'] == 'finished':
            # File finished downloading, might be merging now
            self.after(0, self.update_progress, 1.0, "Mezclando Audio y Video (Por favor espera)...")

    def cancel_download(self):
        self.cancel_download_flag = True
        if self.current_download_btn:
            self.current_download_btn.x_btn.configure(state="disabled")
            self.current_download_btn.configure(text="Cancelando   ", fg_color="#EF4444")

    def start_download(self, format_name):
        url = self.url_var.get()
        self.cancel_download_flag = False
        self.current_downloading_files = set()
        self.current_download_btn = None
        self.current_format_name = format_name
        for btn in self.format_radios:
            btn.configure(state="disabled")
            if btn.cget("text") == format_name:
                self.current_download_btn = btn
                btn.configure(text="Descargando   ", fg_color=self.accent_color)
                btn.x_btn.pack(side="right", padx=(5, 0))
                
        self.download_anim_step = 0
        self.animate_downloading(self.current_download_btn)
                
        self.search_btn.configure(state="disabled")
        
        self.progress_bar.grid()
        self.status_label.grid()
        self.update_progress(0, "Iniciando descarga...")

        thread = threading.Thread(target=self.download_media_thread, args=(url, format_name), daemon=True)
        thread.start()

    def download_media_thread(self, url, format_name):
        formato_str = self.available_formats.get(format_name, 'best')
        
        ydl_opts = {
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': self.ffmpeg_path,
            'noplaylist': True,
            'progress_hooks': [self.progress_hook]
        }

        if format_name == "Audio - MP3 (Comprimido)":
            ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]})
        elif format_name == "Audio - M4A (Original)":
            ydl_opts.update({'format': 'bestaudio[ext=m4a]/bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a'}]})
        else:
            ydl_opts.update({'format': formato_str, 'merge_output_format': 'mp4'})

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.after(0, self.update_download_success, format_name)
        except Exception as e:
            self.after(0, self.update_download_error, str(e))

    def update_download_success(self, original_format_name):
        self.progress_bar.set(1.0)
        if self.current_download_btn:
            self.current_download_btn.configure(text="¡Completado!")
            # Resetear a los 4 segundos
            self.after(4000, lambda: self.reset_download_btn(self.current_download_btn, original_format_name))
            
        for btn in self.format_radios:
            if btn != self.current_download_btn:
                btn.configure(state="normal")
        self.search_btn.configure(state="normal")
        
        if self.enable_sound.get():
            try:
                import winsound
                winsound.PlaySound(r"C:\Windows\Media\Windows Navigation Start.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                pass
        
        if self.enable_notif.get():
            try:
                notification.notify(title="Aero Downloader", message="¡Tu descarga ha finalizado con éxito!", app_name="Aero Downloader", timeout=5)
            except:
                pass
            
    def reset_download_btn(self, btn, original_text):
        if btn.winfo_exists():
            btn.configure(text=original_text, fg_color="#2b2b36", state="normal")
            if hasattr(btn, 'x_btn') and btn.x_btn.winfo_exists():
                btn.x_btn.pack_forget()
                btn.x_btn.configure(state="normal")
        self.progress_bar.grid_remove()
        self.status_label.grid_remove()
        
    def animate_downloading(self, btn):
        if not btn.winfo_exists() or btn != getattr(self, 'current_download_btn', None) or getattr(self, 'cancel_download_flag', False):
            return
            
        current_text = btn.cget("text")
        if current_text.startswith("¡Completado") or current_text.startswith("Error"):
            return
            
        dots = "." * (self.download_anim_step % 4)
        btn.configure(text=f"Descargando{dots:<3}")
        self.download_anim_step += 1
        
        self.after(500, lambda: self.animate_downloading(btn))

    def animate_canceling(self, btn, step, original_text):
        if not btn.winfo_exists():
            return
            
        dots = "." * (step % 4)
        btn.configure(text=f"Cancelando{dots:<3}")
        
        if step < 8:  # 8 steps * 500ms = 4 seconds
            self.after(500, lambda: self.animate_canceling(btn, step + 1, original_text))
        else:
            self.reset_download_btn(btn, original_text)
            
    def update_download_error(self, error_msg):
        self.progress_bar.grid_remove()
        self.status_label.grid_remove()
        if self.current_download_btn:
            restored_text = getattr(self, 'current_format_name', "Descargar")
            if getattr(self, 'cancel_download_flag', False):
                self.current_download_btn.configure(fg_color="gray50")
                self.animate_canceling(self.current_download_btn, 0, restored_text)
                
                # Cleanup leftover files
                if hasattr(self, 'current_downloading_files'):
                    for f in self.current_downloading_files:
                        try:
                            import os
                            if os.path.exists(f): os.remove(f)
                            if os.path.exists(f + '.part'): os.remove(f + '.part')
                            if os.path.exists(f + '.ytdl'): os.remove(f + '.ytdl')
                        except Exception:
                            pass
                    self.current_downloading_files.clear()
            else:
                self.current_download_btn.configure(text="Error", fg_color="#EF4444")
                self.after(4000, lambda: self.reset_download_btn(self.current_download_btn, restored_text))
        
        for btn in self.format_radios:
            if btn != self.current_download_btn:
                btn.configure(state="normal")
        self.search_btn.configure(state="normal")

if __name__ == "__main__":
    app = App()
    
    import sys
    import urllib.parse
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("aerodl://"):
            video_url = arg.replace("aerodl://", "", 1)
            if video_url.endswith('/'): video_url = video_url[:-1]
            video_url = urllib.parse.unquote(video_url)
            app.after(500, lambda: app.receive_bridge_url(video_url))
            
    app.mainloop()
