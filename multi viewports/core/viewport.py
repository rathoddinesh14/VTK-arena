"""
Viewport module for managing individual rendering viewports.
"""
import vtk


class Viewport:
    """Represents a single viewport with renderer and camera."""
    
    def __init__(self, title="Viewport", bg_color=(0.12, 0.14, 0.16)):
        """
        Initialize a viewport.
        
        Args:
            title: Name/identifier for the viewport
            bg_color: Background color RGB tuple
        """
        self.title = title
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(*bg_color)
        self.renderer.SetGradientBackground(True)
        # Gradient to slightly darker shade for visual depth
        bg2_darker = tuple(max(0.0, c - 0.1) for c in bg_color)
        self.renderer.SetBackground2(*bg2_darker)
        self.actors = []
    
    def add_actor(self, actor):
        """Add an actor to the viewport."""
        self.renderer.AddActor(actor)
        self.actors.append(actor)
    
    def add_actor_2d(self, actor2d):
        """Add a 2D actor to the viewport."""
        self.renderer.AddActor2D(actor2d)
        self.actors.append(actor2d)
    
    def set_camera_position(self, position, focal_point=(0, 0, 0)):
        """
        Set camera position and focal point.
        
        Args:
            position: Camera position (x, y, z)
            focal_point: Point where camera looks at
        """
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(*position)
        camera.SetFocalPoint(*focal_point)
        self.renderer.ResetCamera()
    
    def reset_camera(self):
        """Reset camera to default position."""
        self.renderer.ResetCamera()
    
    def get_renderer(self):
        """Get the vtkRenderer instance."""
        return self.renderer
    

