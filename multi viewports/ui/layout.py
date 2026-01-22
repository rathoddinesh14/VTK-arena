"""
Layout module for viewport arrangement.
"""
from core.viewport import Viewport


class ViewportLayout:
    """Manages the 1+3 viewport layout with enhanced visualization."""
    
    # Color scheme for each viewport
    VIEWPORT_COLORS = {
        "main": (0.9, 0.9, 0.95),      # Light blue-white
        "top": (0.95, 0.92, 0.85),      # Warm beige
        "front": (0.88, 0.95, 0.88),    # Light green
        "right": (0.95, 0.88, 0.88),    # Light red
    }
    
    BG_COLORS = {
        "main": (0.9, 0.92, 0.95),      # Light blue-white
        "top": (0.95, 0.93, 0.88),      # Light beige
        "front": (0.90, 0.96, 0.90),    # Light green
        "right": (0.96, 0.90, 0.90),    # Light red
    }
    
    def __init__(self):
        """Initialize viewports for 1+3 layout."""
        self.main_viewport = Viewport(title="Main (Isometric)", bg_color=self.BG_COLORS["main"])
        self.viewport_top = Viewport(title="Top View (XY Plane)", bg_color=self.BG_COLORS["top"])
        self.viewport_front = Viewport(title="Front View (XZ Plane)", bg_color=self.BG_COLORS["front"])
        self.viewport_right = Viewport(title="Right View (YZ Plane)", bg_color=self.BG_COLORS["right"])
        
        self.viewports_list = [
            self.main_viewport,
            self.viewport_top,
            self.viewport_front,
            self.viewport_right
        ]
    
    
    def get_viewport_configs(self):
        """
        Get viewport configurations for rendering engine.
        
        Returns:
            List of tuples (viewport, rect) where rect is normalized (0-1) coords
            Layout: Main viewport left half (full height), 3 others right half stacked vertically
        """
        return [
            # Main viewport (left half, full height)
            (self.main_viewport, (0.0, 0.0, 0.5, 1.0)),
            # Right view (right half, bottom 1/3)
            (self.viewport_right, (0.5, 0.0, 1.0, 1.0/3.0)),
            # Front view (right half, middle 1/3)
            (self.viewport_front, (0.5, 1.0/3.0, 1.0, 2.0/3.0)),
            # Top view (right half, top 1/3)
            (self.viewport_top, (0.5, 2.0/3.0, 1.0, 1.0)),
        ]
    
    def add_actor_to_all(self, actor):
        """Add the same actor to all viewports."""
        for viewport in self.viewports_list:
            viewport.add_actor(actor)
    
    def add_actor_2d_to_all(self, actor2d):
        """Add the same 2D actor to all viewports."""
        for viewport in self.viewports_list:
            viewport.add_actor_2d(actor2d)
