"""
Main application entry point for VTK Project.
Demonstrates a 1+3 viewport layout with rendered cuboid.
Features:
  - 4 synchronized viewports (1 left isometric + 3 right stacked)
  - Interactive transform controls
  - Real-time synchronization across all viewports
  - Professional lighting and materials
  - 2D bounding box covering all objects
"""
from core.geometry import CuboidFactory
from core.renderer import RenderingEngine
from core.overlay import BoundingBoxOverlay
from ui.layout import ViewportLayout


class VTKApplication:
    """Main VTK Application wrapper."""
    
    def __init__(self):
        """Initialize the application."""
        self.engine = None
        self.layout = None
        self.actor = None
        self.actor2 = None
        self.bbox_actors = []  # Store bbox for each viewport
    
    def setup(self):
        """Setup the entire application."""
        # Create rendering engine
        self.engine = RenderingEngine(
            width=1000,
            height=800,
            title="VTK Visualization - 1+3 Multi-View"
        )
        
        # Create viewport layout
        self.layout = ViewportLayout()
        
        # Create a beautiful cuboid with glossy material
        mapper = CuboidFactory.create_cuboid(width=2.0, height=2.0, depth=2.0)
        self.actor = CuboidFactory.create_actor(
            mapper,
            color=(0.2, 0.6, 0.95),  # Beautiful blue
            material_type="glossy"
        )
        
        # Create a smaller cuboid on the left
        mapper2 = CuboidFactory.create_cuboid(width=0.8, height=0.8, depth=0.8)
        self.actor2 = CuboidFactory.create_actor(
            mapper2,
            color=(0.95, 0.6, 0.2),  # Orange
            material_type="glossy"
        )
        self.actor2.SetPosition(-2.5, 0, 0)  # Position on the left
        
        # Add actors to all viewports
        self.layout.add_actor_to_all(self.actor)
        self.layout.add_actor_to_all(self.actor2)
        
        # Create and add bounding box for each viewport
        for viewport in self.layout.viewports_list:
            bbox = BoundingBoxOverlay.create_responsive_bounding_box(
                [self.actor, self.actor2],
                viewport.get_renderer(),
                color=(0.2, 0.9, 0.2),  # Green
                line_width=2
            )
            viewport.add_actor_2d(bbox)
            self.bbox_actors.append(bbox)
            self.engine.register_bbox_2d(bbox)
        
        # Register all viewports with rendering engine
        for viewport, rect in self.layout.get_viewport_configs():
            self.engine.add_viewport(viewport, rect)
        
        # Set actor for transform controls
        self.engine.set_actor(self.actor)
    
    def run(self):
        """Run the application."""
        self.setup()
        self.engine.setup_interactor_style()
        print("\n" + "="*60)
        print("VTK Visualization - Interactive Controls")
        print("="*60)
        print("\nKeyboard Controls:")
        print("  Arrow Keys  - Move cuboid (X/Y)")
        print("  W/S         - Rotate around X axis")
        print("  A/D         - Rotate around Z axis")
        print("  Q/E         - Rotate around Y axis")
        print("  R           - Reset position & rotation")
        print("  Mouse       - Rotate camera view")
        print("="*60 + "\n")
        self.engine.render()


def main():
    """Entry point for the application."""
    app = VTKApplication()
    app.run()


if __name__ == "__main__":
    main()
