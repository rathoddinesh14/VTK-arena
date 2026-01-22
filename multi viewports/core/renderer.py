"""
Renderer module for managing the rendering window and interactor.
"""
import vtk


class RenderingEngine:
    """Manages the main render window and interactor."""
    
    def __init__(self, width=1400, height=900, title="VTK Project"):
        """
        Initialize the rendering engine.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            title: Window title
        """
        self.render_window = vtk.vtkRenderWindow()
        self.render_window.SetSize(width, height)
        self.render_window.SetWindowName(title)
        
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.render_window)
        
        self.viewports = []
        self.current_actor = None
        self.bbox_2d_actors = []  # Track 2D bounding box actors
    
    def add_viewport(self, viewport, viewport_rect):
        """
        Add a viewport to the rendering window with clear border.
        
        Args:
            viewport: Viewport instance
            viewport_rect: Tuple (x0, y0, x1, y1) normalized coordinates (0-1)
        """
        renderer = viewport.get_renderer()
        renderer.SetViewport(*viewport_rect)
        renderer.DrawOn()
        self.render_window.AddRenderer(renderer)
        self.viewports.append(viewport)
    
    def setup_interactor_style(self):
        """Setup mouse interaction style with transform controls."""
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(style)
        
        # Add keyboard callbacks for transform controls
        self.interactor.AddObserver('KeyPressEvent', self.on_key_press)
        
        # Add render callback to update bounding boxes on every render
        self.render_window.AddObserver('StartEvent', self.on_render_start)
    
    def set_actor(self, actor):
        """Set the actor for transform operations."""
        self.current_actor = actor
    
    def register_bbox_2d(self, bbox_actor):
        """Register a 2D bounding box actor for updates."""
        self.bbox_2d_actors.append(bbox_actor)
    
    def on_key_press(self, obj, event):
        """Handle keyboard events for actor transformation."""
        key = self.interactor.GetKeySym()
        
        if self.current_actor is None:
            return
        
        step = 0.1
        rotation_step = 5.0
        
        if key == 'Right':
            self.current_actor.AddPosition(step, 0, 0)
        elif key == 'Left':
            self.current_actor.AddPosition(-step, 0, 0)
        elif key == 'Up':
            self.current_actor.AddPosition(0, step, 0)
        elif key == 'Down':
            self.current_actor.AddPosition(0, -step, 0)
        elif key == 'w':
            self.current_actor.RotateX(rotation_step)
        elif key == 's':
            self.current_actor.RotateX(-rotation_step)
        elif key == 'a':
            self.current_actor.RotateZ(rotation_step)
        elif key == 'd':
            self.current_actor.RotateZ(-rotation_step)
        elif key == 'q':
            self.current_actor.RotateY(rotation_step)
        elif key == 'e':
            self.current_actor.RotateY(-rotation_step)
        elif key == 'r':
            # Reset position and rotation
            self.current_actor.SetPosition(0, 0, 0)
            self.current_actor.SetOrientation(0, 0, 0)
        
        # Render all viewports
        self._update_and_render()
    
    def on_render_start(self, obj, event):
        """Callback before rendering - updates bounding boxes."""
        try:
            self._update_bbox_only()
        except Exception:
            # Silently ignore errors during render callbacks
            pass
    
    def render(self):
        """Render and display the window."""
        self._update_and_render()
        self.interactor.Initialize()
        self.interactor.Start()
    
    def _update_and_render(self):
        """Update bounding boxes and render all viewports."""
        from core.overlay import BoundingBoxOverlay
        
        # Update all 2D bounding boxes
        for bbox_actor in self.bbox_2d_actors:
            BoundingBoxOverlay.update_responsive_bounding_box(bbox_actor)
        
        # Render
        self.render_window.Render()
    
    def _update_bbox_only(self):
        """Update only bounding boxes without re-rendering."""
        from core.overlay import BoundingBoxOverlay
        
        # Update all 2D bounding boxes
        for bbox_actor in self.bbox_2d_actors:
            BoundingBoxOverlay.update_responsive_bounding_box(bbox_actor)
    
    def get_render_window(self):
        """Get the vtkRenderWindow instance."""
        return self.render_window
    
    def get_interactor(self):
        """Get the vtkRenderWindowInteractor instance."""
        return self.interactor
