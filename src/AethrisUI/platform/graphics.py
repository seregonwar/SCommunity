from typing import Tuple, Union
import win32gui
import win32ui
import win32con
import win32api
from .color import Color
import math
from ctypes import byref, create_string_buffer, windll

class Canvas:
    def __init__(self, size: Tuple[int, int]):
        self.width = size[0]
        self.height = size[1]
        self.hdc = None
        
    def set_device_context(self, hdc):
        self.hdc = hdc
        
    def clear(self):
        if self.hdc:
            brush = win32gui.CreateSolidBrush(Color("#FFFFFF").to_windows_color())
            win32gui.FillRect(self.hdc, (0, 0, self.width, self.height), brush)
            win32gui.DeleteObject(brush)
            
    def draw_rounded_rectangle(self, x: int, y: int, width: int, height: int, radius: int, color: Color):
        """Disegna un rettangolo con angoli arrotondati"""
        if self.hdc:
            # Crea il pennello per il colore di riempimento
            brush = win32gui.CreateSolidBrush(color.to_windows_color())
            
            # Crea il percorso per il rettangolo arrotondato
            points = []
            
            # Angolo in alto a sinistra
            points.extend([
                (x + radius, y),
                (x + width - radius, y),
                (x + width - radius, y),
                (x + width, y),
                (x + width, y + radius)
            ])
            
            # Angolo in alto a destra
            points.extend([
                (x + width, y + radius),
                (x + width, y + height - radius),
                (x + width, y + height - radius),
                (x + width, y + height),
                (x + width - radius, y + height)
            ])
            
            # Angolo in basso a destra
            points.extend([
                (x + width - radius, y + height),
                (x + radius, y + height),
                (x + radius, y + height),
                (x, y + height),
                (x, y + height - radius)
            ])
            
            # Angolo in basso a sinistra
            points.extend([
                (x, y + height - radius),
                (x, y + radius),
                (x, y + radius),
                (x, y),
                (x + radius, y)
            ])
            
            # Disegna il percorso
            win32gui.BeginPath(self.hdc)
            win32gui.PolyBezier(self.hdc, points)
            win32gui.EndPath(self.hdc)
            win32gui.FillPath(self.hdc)
            
            # Pulisci le risorse
            win32gui.DeleteObject(brush)
            
    def draw_rectangle(self, x: int, y: int, width: int, height: int, color: Color, radius: int = 0):
        """Disegna un rettangolo, eventualmente con angoli arrotondati"""
        if radius > 0:
            self.draw_rounded_rectangle(x, y, width, height, radius, color)
        else:
            if self.hdc:
                brush = win32gui.CreateSolidBrush(color.to_windows_color())
                win32gui.FillRect(self.hdc, (x, y, x + width, y + height), brush)
                win32gui.DeleteObject(brush)
    
    def draw_text(self, text: str, x: int, y: int, color: Color, font_size: int = 14):
        if self.hdc:
            # Crea la struttura LOGFONT
            lf = win32gui.LOGFONT()
            lf.lfHeight = font_size
            lf.lfWidth = 0
            lf.lfWeight = win32con.FW_NORMAL
            lf.lfItalic = 0
            lf.lfUnderline = 0
            lf.lfStrikeOut = 0
            lf.lfCharSet = win32con.ANSI_CHARSET
            lf.lfOutPrecision = win32con.OUT_DEFAULT_PRECIS
            lf.lfClipPrecision = win32con.CLIP_DEFAULT_PRECIS
            lf.lfQuality = win32con.DEFAULT_QUALITY
            lf.lfPitchAndFamily = win32con.DEFAULT_PITCH | win32con.FF_DONTCARE
            lf.lfFaceName = "Segoe UI"
            
            # Crea il font
            font = win32gui.CreateFontIndirect(lf)
            
            # Imposta il colore del testo
            win32gui.SetTextColor(self.hdc, color.to_windows_color())
            win32gui.SetBkMode(self.hdc, win32con.TRANSPARENT)
            
            # Seleziona il font
            old_font = win32gui.SelectObject(self.hdc, font)
            
            # Disegna il testo
            win32gui.DrawText(
                self.hdc, text, -1,
                (x, y, x + 1000, y + 1000),  # rettangolo ampio per il testo
                win32con.DT_LEFT | win32con.DT_TOP | win32con.DT_SINGLELINE
            )
            
            # Ripristina il font originale e pulisci le risorse
            win32gui.SelectObject(self.hdc, old_font)
            win32gui.DeleteObject(font)
    
    def update(self):
        pass