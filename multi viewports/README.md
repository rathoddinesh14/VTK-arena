# VTK Python Visualization Studio

A beautiful, modular VTK Python application featuring professional 1+3 multi-viewport visualization with advanced rendering capabilities.

## Features

### Visual Enhancements ✨
- **Multi-Viewport Layout**: 1 isometric main view + 3 orthographic views (top, front, right)
- **Professional Lighting**: 3-point lighting setup (key, fill, back lights) for realistic rendering
- **Material Properties**: Glossy, metallic, and matte material options with specular highlights
- **Gradient Backgrounds**: Beautiful dark theme with subtle gradient backgrounds per viewport
- **Viewport Titles**: Color-coded overlays identifying each viewport
- **Coordinate Axes**: 3D axes indicators in each viewport
- **Bounds Information**: Real-time display of object dimensions and bounds
- **Edge Highlighting**: Visible edges with subtle coloring for better depth perception

### Project Structure 🏗️
```
vtk/
├── core/                    # Core visualization modules
│   ├── __init__.py
│   ├── geometry.py         # Geometry creation and materials
│   ├── viewport.py         # Individual viewport management
│   ├── renderer.py         # Rendering engine and window
│   ├── axes.py             # Coordinate axes and indicators
│   └── overlay.py          # Text overlays and HUD elements
├── ui/                      # User interface modules
│   ├── __init__.py
│   └── layout.py           # Viewport layout configuration
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── venv/                   # Python virtual environment
```

### Modular Design 🔧
- **GeometryFactory**: Create various 3D objects with different materials
- **MaterialFactory**: Define and apply materials (metallic, glossy, matte)
- **Viewport**: Individual viewport management with overlays and axes
- **RenderingEngine**: Centralized rendering window and interactor management
- **ViewportLayout**: Configurable viewport arrangement and synchronization
- **TextOverlay**: Rich 2D text rendering for HUD elements
- **AxisIndicator**: Coordinate system visualization

## Installation

### Prerequisites
- Python 3.8+
- macOS/Linux/Windows

### Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the Application
```bash
cd /Users/rathod_ias/vtk
source venv/bin/activate
python main.py
```

### Interact with the Visualization
- **Rotate**: Click and drag with left mouse button
- **Zoom**: Scroll wheel or middle mouse button drag
- **Pan**: Right-click and drag
- **Orthographic Switch**: Not implemented (use isometric/orthographic views)

### Customize the Application

#### Change Cuboid Dimensions
Edit `main.py`:
```python
mapper = CuboidFactory.create_cuboid(width=3.0, height=2.0, depth=1.5)
```

#### Change Material Type
Edit `main.py`:
```python
# Options: "glossy", "metallic", "matte"
actor = CuboidFactory.create_actor(
    mapper,
    color=(0.2, 0.6, 0.95),
    material_type="metallic"
)
```

#### Modify Colors
Edit `ui/layout.py` to change viewport-specific colors:
```python
VIEWPORT_COLORS = {
    "main": (0.9, 0.9, 0.95),      # Light blue-white
    "top": (0.95, 0.92, 0.85),      # Warm beige
    "front": (0.88, 0.95, 0.88),    # Light green
    "right": (0.95, 0.88, 0.88),    # Light red
}
```

#### Adjust Lighting
Edit `core/viewport.py` `_setup_lighting()` method to customize light positions and intensities.

## Architecture

### Rendering Pipeline
1. **Geometry Creation** → Create 3D objects with materials
2. **Viewport Setup** → Configure viewports with cameras and lighting
3. **Layout Configuration** → Arrange viewports in specific regions
4. **Rendering** → Render to VTK window with interactor

### Data Flow
```
CuboidFactory → create_actor → Viewport.add_actor
                                    ↓
                            Viewport overlay setup
                                    ↓
                            RenderingEngine.add_viewport
                                    ↓
                            Render Window
```

## Dependencies

- **vtk** (≥9.0.0): Visualization Toolkit for 3D graphics
- **numpy** (≥1.23): Numerical computing
- **matplotlib** (≥2.0.0): Plotting library (required by VTK)

## Performance Notes

- The application is optimized for real-time interaction
- 4 synchronized viewports render simultaneously
- Professional lighting with 3 lights per viewport provides high visual quality
- Edge visualization adds minimal overhead while improving depth perception

## Future Enhancements

- [ ] Add more primitive shapes (spheres, cylinders, cones)
- [ ] Implement viewport picking and selection
- [ ] Add animation capabilities
- [ ] Create scene graph for complex assemblies
- [ ] Implement measurement tools
- [ ] Add clipping planes
- [ ] Support for loading external geometry files

## License

This project is provided as-is for educational and professional visualization purposes.

## Author

Created with VTK 9.5.2 and Python 3.13

---

**Happy Visualizing!** 🎨
