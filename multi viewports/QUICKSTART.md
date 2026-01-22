# 🚀 Quick Start Guide

## Getting Started in 30 Seconds

### 1. Activate Virtual Environment
```bash
cd /Users/rathod_ias/vtk
source venv/bin/activate
```

### 2. Run the Application
```bash
python main.py
```

That's it! You'll see a beautiful 1+3 viewport visualization with:
- ✨ A glossy blue cuboid in the center
- 🎯 Professional 3-point lighting
- 📊 Four synchronized viewports (isometric + 3 orthographic views)
- 📌 Coordinate axes in each viewport
- 📝 Viewport titles and bounds information
- 🎨 Beautiful dark theme with gradient backgrounds

---

## Interactive Controls

| Action | Control |
|--------|---------|
| **Rotate** | Click + Drag (Left Mouse) |
| **Zoom** | Scroll Wheel / Middle Mouse Drag |
| **Pan** | Right-Click + Drag |
| **Reset View** | Press 'r' |

---

## Customization Examples

### Change Cuboid Dimensions
Edit `main.py` line 36:
```python
mapper = CuboidFactory.create_cuboid(width=3.0, height=2.0, depth=1.5)
```

### Change Material Type
Edit `main.py` line 40:
```python
# Options: "glossy", "metallic", "matte"
material_type="metallic"
```

### Change Color
Edit `main.py` line 37:
```python
color=(0.95, 0.4, 0.2)  # Orange-red
```

### Use Configuration File
Edit `config.py` to change:
- Window size
- Colors and lighting
- Material properties
- Camera positions
- Viewport titles

---

## Project Structure

```
vtk/
├── main.py              👈 Run this!
├── config.py            ⚙️  Configuration
├── examples.py          📚 More examples
├── requirements.txt     📦 Dependencies
├── README.md           📖 Full documentation
├── core/
│   ├── geometry.py     🟦 3D objects & materials
│   ├── viewport.py     🖼️  Viewport management
│   ├── renderer.py     🎨 Rendering engine
│   ├── axes.py         📐 Coordinate axes
│   └── overlay.py      📝 Text overlays
└── ui/
    └── layout.py       📐 Viewport layout
```

---

## Features at a Glance

### 🎨 Visual Features
- Multi-viewport synchronized rendering
- Professional 3-point lighting
- 3 material types (glossy, metallic, matte)
- Gradient backgrounds per viewport
- Edge highlighting for depth
- Coordinate axes indicators

### 🏗️ Architecture
- Modular design with clear separation of concerns
- Factory pattern for geometry and materials
- Configurable viewport layout
- Extensible overlay system
- Professional code organization

### 📊 Visualization Options
- Main isometric view (50% of screen)
- Top orthographic view (16.7% of screen)
- Front orthographic view (16.7% of screen)
- Right orthographic view (16.7% of screen)

---

## Troubleshooting

### "VTK not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Window won't open"
Make sure your display supports OpenGL. On remote systems, use X11 forwarding.

### "Viewport looks different"
Check `config.py` for color and lighting settings. Gradient backgrounds can be disabled there.

---

## Next Steps

1. **Explore Examples**: Run `python examples.py` (uncomment different examples)
2. **Read Full Docs**: See `README.md` for comprehensive documentation
3. **Customize**: Edit `config.py` to personalize colors and settings
4. **Extend**: Add more geometry types using the `CuboidFactory` pattern
5. **Animate**: Extend the `VTKApplication` class with animation callbacks

---

## Tips & Tricks

💡 **Pro Tips**
- Hold `Shift` while rotating for finer control
- Middle-click to center view on object
- Right-click menu for rendering options
- Each viewport has independent cameras but synchronized actors

🎨 **Customization Ideas**
- Change gradient colors in `viewport.py` `_setup_lighting()`
- Add custom material types in `geometry.py`
- Create new layouts by modifying `get_viewport_configs()`
- Add interactive overlays using the overlay module

📈 **Performance**
- 4 synchronized viewports render in real-time
- Professional lighting provides high visual quality with minimal overhead
- Edge visualization adds subtle visual cues without performance impact

---

**Enjoy your VTK visualization experience!** 🚀✨
