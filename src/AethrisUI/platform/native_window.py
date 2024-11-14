import sys
import win32gui
import win32con
import win32api
import logging
from typing import Tuple, Optional, Dict, Any
from ..core import VirtualNode
from .graphics import Canvas
from .events import Event
from ctypes import Structure, c_ulong, POINTER, byref, WINFUNCTYPE, sizeof, windll

logger = logging.getLogger(__name__)

class PAINTSTRUCT(Structure):
    _fields_ = [
        ('hdc', c_ulong),
        ('fErase', c_ulong),
        ('rcPaint', c_ulong * 4),
        ('fRestore', c_ulong),
        ('fIncUpdate', c_ulong),
        ('rgbReserved', c_ulong * 32),
    ]

class TRACKMOUSEEVENT(Structure):
    _fields_ = [
        ('cbSize', c_ulong),
        ('dwFlags', c_ulong),
        ('hwndTrack', c_ulong),
        ('dwHoverTime', c_ulong),
    ]

class NativeWindow:
    _window_class_registered = False
    _window_class_name = "ModernGUIClass"
    _windows = {}
    
    def __init__(self, title: str = "Modern GUI Window", size: Tuple[int, int] = (800, 600)):
        logger.debug("Initializing NativeWindow")
        if not sys.platform == "win32":
            raise OSError("Platform not supported")
            
        self.title = title
        self.size = size
        self.handle = None
        self.canvas = Canvas(size)
        self._instance = win32gui.GetModuleHandle(None)
        self._needs_render = False
        self._is_painting = False
        self._current_node = None
        self._renderer = None
        NativeWindow._windows[id(self)] = self
        self._setup_native_window()
        
        # Aggiungi tracking del mouse
        self._tracking_mouse = False
    
    def _setup_native_window(self):
        logger.debug("Setting up native window")
        try:
            if not NativeWindow._window_class_registered:
                self._register_class()
            self._create_window()
            self._init_renderer()
        except Exception as e:
            logger.error(f"Error setting up native window: {e}", exc_info=True)
            raise
    
    def _init_renderer(self):
        """Inizializza il renderer dopo che la finestra è stata creata"""
        from ..core.renderer import Renderer
        self._renderer = Renderer(self.canvas)
        self._renderer.set_window(self)
    
    def _window_proc(self, hwnd: int, msg: int, wparam: int, lparam: int) -> Optional[int]:
        try:
            if msg == win32con.WM_CLOSE:
                logger.debug("WM_CLOSE received")
                win32gui.DestroyWindow(hwnd)
                return 0
                
            elif msg == win32con.WM_DESTROY:
                logger.debug("WM_DESTROY received")
                win32gui.PostQuitMessage(0)
                return 0
                
            elif msg == win32con.WM_PAINT:
                logger.debug("WM_PAINT received")
                self._paint()
                return 0
                
            elif msg == win32con.WM_MOUSEMOVE:
                if not self._tracking_mouse:
                    # Inizia il tracking del mouse
                    track = TRACKMOUSEEVENT()
                    track.cbSize = sizeof(TRACKMOUSEEVENT)
                    track.dwFlags = win32con.TME_LEAVE
                    track.hwndTrack = hwnd
                    track.dwHoverTime = 0
                    windll.user32.TrackMouseEvent(byref(track))
                    self._tracking_mouse = True
                
                # Gestisci il movimento del mouse
                x = win32api.LOWORD(lparam)
                y = win32api.HIWORD(lparam)
                if self._renderer:
                    self._renderer.handle_mouse_move(x, y)
            
            elif msg == win32con.WM_MOUSELEAVE:
                self._tracking_mouse = False
                if self._renderer:
                    self._renderer.handle_mouse_move(-1, -1)
            
            elif msg == win32con.WM_LBUTTONDOWN:
                # Gestisci il click del mouse
                x = win32api.LOWORD(lparam)
                y = win32api.HIWORD(lparam)
                if self._renderer:
                    self._renderer._active_node = self._renderer._hovered_node
                    self._renderer.render(self._current_node)
            
            elif msg == win32con.WM_LBUTTONUP:
                if self._renderer:
                    self._renderer._active_node = None
                    self._renderer.render(self._current_node)
                    # Gestisci il click
                    x = win32api.LOWORD(lparam)
                    y = win32api.HIWORD(lparam)
                    if self._renderer.handle_click(x, y):
                        return 0
            
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
            
        except Exception as e:
            logger.error(f"Error in window proc: {str(e)}", exc_info=True)
        
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    
    def _register_class(self):
        logger.debug("Registering window class")
        try:
            wc = win32gui.WNDCLASS()
            wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
            wc.lpfnWndProc = self._window_proc
            wc.hInstance = self._instance
            wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
            wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
            wc.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
            wc.lpszClassName = self._window_class_name
            
            win32gui.RegisterClass(wc)
            NativeWindow._window_class_registered = True
            logger.debug("Window class registered successfully")
            
        except Exception as e:
            logger.error(f"Error registering window class: {e}", exc_info=True)
            raise
    
    def _create_window(self):
        logger.debug("Creating window")
        try:
            style = win32con.WS_OVERLAPPEDWINDOW | win32con.WS_VISIBLE
            
            # Calcola le dimensioni della finestra
            rect = win32gui.GetClientRect(win32gui.GetDesktopWindow())
            x = (rect[2] - self.size[0]) // 2
            y = (rect[3] - self.size[1]) // 2
            
            logger.debug(f"Creating window with dimensions: {self.size[0]}x{self.size[1]} at {x},{y}")
            
            self.handle = win32gui.CreateWindow(
                self._window_class_name,
                self.title,
                style,
                x, y,
                self.size[0], self.size[1],
                0, 0,
                self._instance,
                None
            )
            
            if not self.handle:
                error = win32api.GetLastError()
                raise WindowsError(f"Could not create window: {error}")
            
            logger.debug(f"Window created successfully with handle: {self.handle}")
            
            win32gui.ShowWindow(self.handle, win32con.SW_SHOWNORMAL)
            win32gui.UpdateWindow(self.handle)
            
        except Exception as e:
            logger.error(f"Error creating window: {e}", exc_info=True)
            raise
    
    def _paint(self):
        if self._is_painting or not self._renderer:
            return 0
            
        logger.debug("Painting window")
        try:
            self._is_painting = True
            hdc = win32gui.GetDC(self.handle)
            if hdc:
                try:
                    self.canvas.set_device_context(hdc)
                    self.canvas.clear()
                    if self._current_node:
                        self._renderer.render(self._current_node)
                finally:
                    win32gui.ReleaseDC(self.handle, hdc)
                    rect = win32gui.GetClientRect(self.handle)
                    win32gui.ValidateRect(self.handle, rect)
        except Exception as e:
            logger.error(f"Error during painting: {e}", exc_info=True)
            raise
        finally:
            self._is_painting = False
            
        return 0
    
    def render(self, node: VirtualNode):
        logger.debug("Rendering node")
        if self._is_painting:
            return
            
        self._current_node = node
        if self.handle:
            rect = win32gui.GetClientRect(self.handle)
            win32gui.InvalidateRect(self.handle, rect, True)
    
    def run(self):
        logger.debug("Starting message loop")
        try:
            while True:
                try:
                    msg = win32gui.GetMessage(None, 0, 0)
                    if msg[0] <= 0:
                        break
                    win32gui.TranslateMessage(msg[1])
                    win32gui.DispatchMessage(msg[1])
                except Exception as e:
                    logger.error(f"Error in message loop: {e}", exc_info=True)
                    break
            logger.debug("Message loop ended")
        except Exception as e:
            logger.error(f"Error in run: {e}", exc_info=True)
            raise 