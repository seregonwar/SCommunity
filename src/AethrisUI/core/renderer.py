from typing import Dict, Any, Optional, Tuple, List
from .virtual_node import VirtualNode
from ..platform.graphics import Canvas, Color
import logging
import win32gui

logger = logging.getLogger(__name__)

class Renderer:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self._current_tree: Optional[VirtualNode] = None
        self._node_positions = {}
        self._hovered_node = None
        self._active_node = None
        self._window = None
        logger.debug("Renderer initialized")
    
    def set_window(self, window):
        self._window = window
    
    def handle_mouse_move(self, x: int, y: int):
        """Gestisce il movimento del mouse"""
        old_hovered = self._hovered_node
        self._hovered_node = None
        
        # Trova il nodo sotto il cursore
        for node_id, (node, pos_x, pos_y, width, height) in self._node_positions.items():
            if (pos_x <= x <= pos_x + width and 
                pos_y <= y <= pos_y + height):
                self._hovered_node = node
                break
        
        # Se il nodo hovered è cambiato, aggiorna la visualizzazione
        if old_hovered != self._hovered_node and self._current_tree:
            self.render(self._current_tree)
    
    def handle_click(self, x: int, y: int) -> bool:
        """Gestisce il click del mouse"""
        for node_id, (node, pos_x, pos_y, width, height) in self._node_positions.items():
            if (pos_x <= x <= pos_x + width and 
                pos_y <= y <= pos_y + height):
                if "onClick" in node.props:
                    node.props["onClick"]()
                    return True
        return False
    
    def render(self, node: VirtualNode):
        try:
            logger.debug(f"Rendering node of type: {node.component_type}")
            self._current_tree = node
            self._node_positions.clear()
            self.canvas.clear()
            self._render_node(node)
            self.canvas.update()
        except Exception as e:
            logger.error(f"Error in render: {str(e)}", exc_info=True)
            raise
    
    def _get_color_from_style(self, style: Dict[str, Any], key: str, default: str = "#000000") -> Color:
        """Converte un valore di colore dallo stile in un oggetto Color"""
        color_value = style.get(key)
        
        if color_value is None:
            return Color(default)
            
        if isinstance(color_value, Color):
            return color_value
            
        if isinstance(color_value, str):
            return Color(color_value)
            
        if isinstance(color_value, dict) and "color" in color_value:
            return Color(color_value["color"])
            
        return Color(default)
    
    def _render_node(self, node: VirtualNode, parent_pos: Tuple[int, int] = (0, 0)):
        try:
            style = node.props.get("style", {})
            x = parent_pos[0] + self._get_style_value(style, "left", 0)
            y = parent_pos[1] + self._get_style_value(style, "top", 0)
            
            if node.component_type == "text":
                self._render_text(node, (x, y))
            elif node.component_type == "button":
                self._render_button(node, (x, y))
            elif node.component_type == "container":
                self._render_container(node, (x, y))
                
        except Exception as e:
            logger.error(f"Error rendering node {node.component_type}: {str(e)}", exc_info=True)
            raise
    
    def _render_button(self, node: VirtualNode, pos: Tuple[int, int]):
        style = node.props.get("style", {})
        text = str(node.props.get("text", ""))
        
        # Assicurati che width e height siano interi
        width = self._get_style_value(style, "width", 60)
        height = self._get_style_value(style, "height", 30)
        
        # Ottieni i colori dallo stile
        background_color = self._get_color_from_style(style, "background", "#CCCCCC")
        text_color = self._get_color_from_style(style, "color", "#000000")
        
        # Se il bottone è hovered, applica gli stili hover
        if node == self._hovered_node and "hover" in style:
            hover_style = style["hover"]
            if "background" in hover_style:
                background_color = self._get_color_from_style(hover_style, "background", background_color.to_hex())
        
        # Se c'è un gradiente, usa il primo colore come background
        if "background_gradient" in style:
            gradient = style["background_gradient"]
            if isinstance(gradient, dict) and "stops" in gradient and len(gradient["stops"]) > 0:
                first_stop = gradient["stops"][0]
                if isinstance(first_stop, dict) and "color" in first_stop:
                    background_color = Color(first_stop["color"])
        
        # Disegna il rettangolo del pulsante
        self.canvas.draw_rectangle(
            pos[0], pos[1], width, height,
            background_color
        )
        
        # Disegna il testo centrato
        text_x = pos[0] + (width - len(text) * 8) // 2
        text_y = pos[1] + (height - 16) // 2
        self.canvas.draw_text(text, text_x, text_y, text_color)
        
        # Memorizza la posizione per gli eventi
        if "onClick" in node.props:
            self._node_positions[id(node)] = (node, pos[0], pos[1], width, height)
    
    def _render_text(self, node: VirtualNode, pos: Tuple[int, int]):
        style = node.props.get("style", {})
        text = str(node.props.get("text", ""))
        color = self._get_color_from_style(style, "color", "#000000")
        font_size = self._get_style_value(style, "font_size", 14)
        self.canvas.draw_text(text, pos[0], pos[1], color, font_size)
    
    def _render_container(self, node: VirtualNode, pos: Tuple[int, int]):
        style = node.props.get("style", {})
        
        # Ottieni le dimensioni
        width = self._get_style_value(style, "width", self.canvas.width)
        height = self._get_style_value(style, "height", self.canvas.height)
        
        # Ottieni padding e margini
        padding_top = self._get_style_value(style, "padding_top", self._get_style_value(style, "padding", 0))
        padding_right = self._get_style_value(style, "padding_right", self._get_style_value(style, "padding", 0))
        padding_bottom = self._get_style_value(style, "padding_bottom", self._get_style_value(style, "padding", 0))
        padding_left = self._get_style_value(style, "padding_left", self._get_style_value(style, "padding", 0))
        
        margin_top = self._get_style_value(style, "margin_top", self._get_style_value(style, "margin", 0))
        margin_right = self._get_style_value(style, "margin_right", self._get_style_value(style, "margin", 0))
        margin_bottom = self._get_style_value(style, "margin_bottom", self._get_style_value(style, "margin", 0))
        margin_left = self._get_style_value(style, "margin_left", self._get_style_value(style, "margin", 0))
        
        # Calcola la posizione effettiva considerando il margine
        actual_x = pos[0] + margin_left
        actual_y = pos[1] + margin_top
        
        # Calcola l'area di contenuto
        content_x = actual_x + padding_left
        content_y = actual_y + padding_top
        content_width = width - (padding_left + padding_right)
        content_height = height - (padding_top + padding_bottom)
        
        # Disegna lo sfondo se presente
        if "background" in style:
            background_color = self._get_color_from_style(style, "background")
            self.canvas.draw_rectangle(
                actual_x, actual_y, width, height,
                background_color
            )
        
        # Se c'è un gradiente, usa quello invece del colore solido
        if "background_gradient" in style:
            gradient = style["background_gradient"]
            if isinstance(gradient, dict) and "stops" in gradient and len(gradient["stops"]) > 0:
                first_stop = gradient["stops"][0]
                if isinstance(first_stop, dict) and "color" in first_stop:
                    background_color = Color(first_stop["color"])
                    self.canvas.draw_rectangle(
                        actual_x, actual_y, width, height,
                        background_color
                    )
        
        # Gestisci il layout dei figli
        if node.children:
            display = style.get("display", "block")
            flex_direction = style.get("flex_direction", "row")
            justify_content = style.get("justify_content", "flex-start")
            align_items = style.get("align_items", "flex-start")
            gap = self._get_style_value(style, "gap", 0)
            
            if display == "flex":
                # Layout flex
                children = node.children
                total_children = len(children)
                
                # Calcola le dimensioni totali dei figli
                total_flex_size = 0
                child_sizes = []
                
                for child in children:
                    child_style = child.props.get("style", {})
                    if flex_direction == "row":
                        size = self._get_style_value(child_style, "width", 0)
                    else:
                        size = self._get_style_value(child_style, "height", 0)
                    child_sizes.append(size)
                    total_flex_size += size
                
                # Calcola lo spazio disponibile
                available_space = content_width if flex_direction == "row" else content_height
                remaining_space = available_space - total_flex_size - (gap * (total_children - 1))
                
                # Distribuisci lo spazio in base a justify_content
                if justify_content == "space-between" and total_children > 1:
                    gap = remaining_space / (total_children - 1)
                elif justify_content == "space-around" and total_children > 0:
                    gap = remaining_space / total_children
                elif justify_content == "space-evenly" and total_children > 0:
                    gap = remaining_space / (total_children + 1)
                
                # Posiziona i figli
                current_pos = content_x if flex_direction == "row" else content_y
                
                for i, child in enumerate(children):
                    child_style = child.props.get("style", {})
                    child_width = self._get_style_value(child_style, "width", 0)
                    child_height = self._get_style_value(child_style, "height", 0)
                    
                    if flex_direction == "row":
                        child_x = current_pos
                        child_y = content_y
                        if align_items == "center":
                            child_y += (content_height - child_height) // 2
                        elif align_items == "flex-end":
                            child_y += content_height - child_height
                        
                        self._render_node(child, (child_x, child_y))
                        current_pos += child_width + gap
                    else:
                        child_x = content_x
                        child_y = current_pos
                        if align_items == "center":
                            child_x += (content_width - child_width) // 2
                        elif align_items == "flex-end":
                            child_x += content_width - child_width
                        
                        self._render_node(child, (child_x, child_y))
                        current_pos += child_height + gap
            
            else:
                # Layout block standard
                current_y = content_y
                for child in node.children:
                    child_style = child.props.get("style", {})
                    child_margin_top = self._get_style_value(child_style, "margin_top", 0)
                    child_margin_bottom = self._get_style_value(child_style, "margin_bottom", 0)
                    
                    current_y += child_margin_top
                    self._render_node(child, (content_x, current_y))
                    
                    child_height = self._get_style_value(child_style, "height", 0)
                    current_y += child_height + child_margin_bottom
    
    def _get_style_value(self, style: Dict[str, Any], key: str, default: Any = 0) -> int:
        """Converte un valore di stile in un intero"""
        if key not in style:
            return default if isinstance(default, int) else 0
            
        value = style[key]
        
        # Se è già un intero, ritornalo
        if isinstance(value, int):
            return value
            
        # Se è un float, convertilo a int
        if isinstance(value, float):
            return int(value)
            
        # Se è una stringa, prova a convertirla
        if isinstance(value, str):
            # Rimuovi 'px' se presente
            value = value.replace('px', '').strip()
            try:
                return int(float(value))
            except ValueError:
                return default if isinstance(default, int) else 0
                
        # Se è un dizionario (per padding/margin), prendi il valore più grande
        if isinstance(value, dict):
            try:
                return max(self._get_style_value(value, k, 0) for k in ['top', 'right', 'bottom', 'left'])
            except:
                return default if isinstance(default, int) else 0
                
        # Per qualsiasi altro tipo, usa il default
        return default if isinstance(default, int) else 0