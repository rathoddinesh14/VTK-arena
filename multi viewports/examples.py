"""
Example showcase demonstrating the VTK Visualization Studio capabilities.
This file shows various ways to customize and extend the visualization.
"""
from core.geometry import CuboidFactory, MaterialFactory, GeometryHelper
from core.renderer import RenderingEngine
from core.overlay import TextOverlay
from ui.layout import ViewportLayout


def example_basic():
    """Basic example: Simple cuboid visualization."""
    engine = RenderingEngine(title="VTK Studio - Basic Example")
    layout = ViewportLayout()
    layout.configure_cameras()
    layout.add_lights()
    
    mapper = CuboidFactory.create_cuboid(width=2.0, height=2.0, depth=2.0)
    actor = CuboidFactory.create_actor(mapper, color=(0.2, 0.6, 0.95), material_type="glossy")
    
    layout.add_actor_to_all(actor)
    layout.enable_all_overlays(actor)
    
    for viewport, rect in layout.get_viewport_configs():
        engine.add_viewport(viewport, rect)
    
    engine.setup_interactor_style()
    engine.render()


def example_materials():
    """Example: Different materials showcase."""
    engine = RenderingEngine(title="VTK Studio - Material Showcase")
    layout = ViewportLayout()
    layout.configure_cameras()
    layout.add_lights()
    
    # Glossy material (blue)
    mapper = CuboidFactory.create_cuboid(width=1.5, height=1.5, depth=1.5)
    actor = CuboidFactory.create_actor(
        mapper,
        color=(0.2, 0.6, 0.95),
        material_type="glossy"
    )
    
    layout.add_actor_to_all(actor)
    layout.enable_all_overlays(actor)
    
    for viewport, rect in layout.get_viewport_configs():
        engine.add_viewport(viewport, rect)
    
    engine.setup_interactor_style()
    engine.render()


def example_custom_colors():
    """Example: Custom color cuboid."""
    engine = RenderingEngine(
        width=1600,
        height=1000,
        title="VTK Studio - Custom Colors"
    )
    layout = ViewportLayout()
    layout.configure_cameras()
    layout.add_lights()
    
    # Create a golden/metallic cuboid
    mapper = CuboidFactory.create_cuboid(width=2.5, height=1.5, depth=1.0)
    actor = CuboidFactory.create_actor(
        mapper,
        color=(0.85, 0.65, 0.15),  # Gold
        material_type="metallic"
    )
    
    layout.add_actor_to_all(actor)
    layout.enable_all_overlays(actor)
    
    for viewport, rect in layout.get_viewport_configs():
        engine.add_viewport(viewport, rect)
    
    engine.setup_interactor_style()
    engine.render()


def example_large_cuboid():
    """Example: Large rectangular cuboid."""
    engine = RenderingEngine(
        width=1600,
        height=1000,
        title="VTK Studio - Large Cuboid"
    )
    layout = ViewportLayout()
    layout.configure_cameras()
    layout.add_lights()
    
    # Create a large rectangular box
    mapper = CuboidFactory.create_cuboid(width=4.0, height=2.0, depth=1.0)
    actor = CuboidFactory.create_actor(
        mapper,
        color=(0.95, 0.4, 0.2),  # Orange-red
        material_type="matte"
    )
    
    layout.add_actor_to_all(actor)
    layout.enable_all_overlays(actor)
    
    for viewport, rect in layout.get_viewport_configs():
        engine.add_viewport(viewport, rect)
    
    engine.setup_interactor_style()
    engine.render()


if __name__ == "__main__":
    # Uncomment the example you want to run:
    example_basic()
    # example_materials()
    # example_custom_colors()
    # example_large_cuboid()
