"""
Overlay module for creating text overlays and HUD elements.
"""
import vtk


class TextOverlay:
    """Creates 2D text overlays for viewports."""
    
    @staticmethod
    def create_text_actor(text, position=(0, 0), font_size=14, color=(1, 1, 1)):
        """
        Create a 2D text actor.
        
        Args:
            text: Text string to display
            position: (x, y) position as percentage (0-100)
            font_size: Font size in pixels
            color: RGB color tuple (0-1 range)
            
        Returns:
            vtkTextActor
        """
        text_actor = vtk.vtkTextActor()
        text_actor.SetInput(text)
        text_actor.GetTextProperty().SetFontSize(font_size)
        text_actor.GetTextProperty().SetColor(*color)
        text_actor.GetTextProperty().SetJustificationToLeft()
        text_actor.GetTextProperty().SetVerticalJustificationToTop()
        text_actor.SetDisplayPosition(int(position[0]), int(position[1]))
        return text_actor
    
    @staticmethod
    def create_corner_text(text, corner="top-left", font_size=12, color=(0.8, 0.8, 0.8)):
        """
        Create text in a viewport corner.
        
        Args:
            text: Text string
            corner: "top-left", "top-right", "bottom-left", "bottom-right"
            font_size: Font size
            color: RGB color tuple
            
        Returns:
            vtkTextActor
        """
        text_actor = vtk.vtkTextActor()
        text_actor.SetInput(text)
        prop = text_actor.GetTextProperty()
        prop.SetFontSize(font_size)
        prop.SetColor(*color)
        prop.SetFontFamilyToTimes()
        prop.BoldOn()
        
        if "top" in corner:
            prop.SetVerticalJustificationToTop()
            y_pos = 40
        else:
            prop.SetVerticalJustificationToBottom()
            y_pos = 20
        
        if "right" in corner:
            prop.SetJustificationToRight()
            x_pos = -40
        else:
            prop.SetJustificationToLeft()
            x_pos = 40
        
        text_actor.SetDisplayPosition(x_pos, y_pos)
        return text_actor
    
    @staticmethod
    def create_fps_monitor():
        """
        Create an FPS counter actor.
        
        Returns:
            vtkTextActor
        """
        fps_actor = vtk.vtkTextActor()
        fps_actor.GetTextProperty().SetFontSize(10)
        fps_actor.GetTextProperty().SetColor(0.0, 1.0, 0.0)
        fps_actor.SetDisplayPosition(10, 10)
        return fps_actor


class ViewportBorder:
    """Creates decorative borders for viewports."""
    
    @staticmethod
    def create_border_actor(name, color=(1.0, 1.0, 1.0)):
        """
        Create a border outline actor with viewport name.
        
        Args:
            name: Viewport name to display on border
            color: Border color RGB tuple
            
        Returns:
            tuple (vtkActor for border, vtkTextActor for name)
        """
        # Create border outline (subtle background frame)
        quad = vtk.vtkQuadric()
        quad.SetCoefficients(1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        # Create name label
        name_actor = vtk.vtkTextActor()
        name_actor.SetInput(name)
        prop = name_actor.GetTextProperty()
        prop.SetFontSize(14)
        prop.SetColor(*color)
        prop.SetJustificationToCentered()
        prop.SetVerticalJustificationToTop()
        prop.BoldOn()
        name_actor.SetDisplayPosition(0, 15)
        
        return name_actor


class StatisticsOverlay:
    """Creates statistics and measurement overlays."""
    
    @staticmethod
    def create_bounds_text(actor):
        """
        Create text showing actor bounds.
        
        Args:
            actor: vtkActor to get bounds from
            
        Returns:
            vtkTextActor with bounds information
        """
        bounds = actor.GetBounds()
        bounds_text = (
            f"Bounds:\n"
            f"X: {bounds[0]:.2f} - {bounds[1]:.2f}\n"
            f"Y: {bounds[2]:.2f} - {bounds[3]:.2f}\n"
            f"Z: {bounds[4]:.2f} - {bounds[5]:.2f}"
        )
        
        text_actor = vtk.vtkTextActor()
        text_actor.SetInput(bounds_text)
        prop = text_actor.GetTextProperty()
        prop.SetFontSize(11)
        prop.SetColor(0.7, 0.9, 1.0)
        prop.SetJustificationToLeft()
        prop.SetVerticalJustificationToTop()
        text_actor.SetDisplayPosition(15, 80)
        
        return text_actor


class BoundingBoxOverlay:
    """Creates dynamic 2D rectangle overlays for objects."""
    
    @staticmethod
    def create_responsive_bounding_box(actors, renderer, color=(1.0, 0.0, 0.0), line_width=2):
        """
        Create a dynamic 2D rectangle overlay that updates as actors move.
        Uses pixel coordinates for simpler coordinate transformation.
        
        Args:
            actors: List of vtkActor objects to bound
            renderer: vtkRenderer instance for coordinate transformations
            color: RGB color tuple for the box outline (0-1 range)
            line_width: Width of the box lines
            
        Returns:
            vtkActor2D representing a responsive bounding box
        """
        # Create points and lines for the rectangle (in display coordinates)
        points = vtk.vtkPoints()
        lines = vtk.vtkCellArray()
        
        # Initialize with default rectangle
        rect_coords = [
            [10, 10, 0], [100, 10, 0],
            [100, 100, 0], [10, 100, 0]
        ]
        
        for coord in rect_coords:
            points.InsertNextPoint(coord)
        
        # Draw rectangle outline
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
        for edge in edges:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, edge[0])
            line.GetPointIds().SetId(1, edge[1])
            lines.InsertNextCell(line)
        
        # Create polydata
        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetLines(lines)
        
        # Create coordinate object for display coordinates (pixels)
        coordinate = vtk.vtkCoordinate()
        coordinate.SetCoordinateSystemToDisplay()
        
        # Create 2D mapper with display coordinate system
        mapper2d = vtk.vtkPolyDataMapper2D()
        mapper2d.SetInputData(polydata)
        mapper2d.SetTransformCoordinate(coordinate)
        
        # Create 2D actor
        actor2d = vtk.vtkActor2D()
        actor2d.SetMapper(mapper2d)
        actor2d.GetProperty().SetColor(*color)
        actor2d.GetProperty().SetLineWidth(line_width)
        
        # Store references for update callback
        actor2d._bbox_polydata = polydata
        actor2d._bbox_points = points
        actor2d._bbox_actors = actors
        actor2d._bbox_renderer = renderer
        actor2d._bbox_coordinate = coordinate
        
        return actor2d
    
    @staticmethod
    def update_responsive_bounding_box(actor2d):
        """
        Update the bounding box to match the current bounds of tracked actors.
        Call this before each render.
        
        Args:
            actor2d: The 2D bounding box actor created by create_responsive_bounding_box
        """
        if not hasattr(actor2d, '_bbox_actors'):
            return
        
        actors = actor2d._bbox_actors
        renderer = actor2d._bbox_renderer
        points = actor2d._bbox_points
        
        # Check if renderer has an active camera
        if not renderer.GetRenderWindow() or not renderer.GetActiveCamera():
            return
        
        # Calculate combined bounds of all actors
        min_x, max_x = float('inf'), float('-inf')
        min_y, max_y = float('inf'), float('-inf')
        min_z, max_z = float('inf'), float('-inf')
        
        for actor in actors:
            bounds = actor.GetBounds()
            min_x = min(min_x, bounds[0])
            max_x = max(max_x, bounds[1])
            min_y = min(min_y, bounds[2])
            max_y = max(max_y, bounds[3])
            min_z = min(min_z, bounds[4])
            max_z = max(max_z, bounds[5])
        
        # Create all 8 3D corners of the bounding box (to account for perspective)
        corners_3d = [
            [min_x, min_y, min_z], [max_x, min_y, min_z],
            [max_x, max_y, min_z], [min_x, max_y, min_z],
            [min_x, min_y, max_z], [max_x, min_y, max_z],
            [max_x, max_y, max_z], [min_x, max_y, max_z],
        ]
        
        # Project all 3D corners to 2D display coordinates (pixels)
        screen_coords = []
        for corner_3d in corners_3d:
            coord = vtk.vtkCoordinate()
            coord.SetCoordinateSystemToWorld()
            coord.SetValue(corner_3d[0], corner_3d[1], corner_3d[2])
            
            # Get display coordinate (in pixels)
            display_coord = coord.GetComputedDisplayValue(renderer)
            screen_coords.append(display_coord[:2])  # x, y only
        
        if not screen_coords or all(c[0] == 0 and c[1] == 0 for c in screen_coords):
            # Fallback if projection fails
            return
        
        # Find min/max screen coordinates from all projected corners
        min_screen_x = min(c[0] for c in screen_coords)
        max_screen_x = max(c[0] for c in screen_coords)
        min_screen_y = min(c[1] for c in screen_coords)
        max_screen_y = max(c[1] for c in screen_coords)
        
        # Add padding in pixels
        padding = 10
        min_screen_x = max(0, min_screen_x - padding)
        max_screen_x = max_screen_x + padding
        min_screen_y = max(0, min_screen_y - padding)
        max_screen_y = max_screen_y + padding
        
        # Update rectangle points in display coordinates (pixels)
        new_coords = [
            [min_screen_x, min_screen_y, 0],
            [max_screen_x, min_screen_y, 0],
            [max_screen_x, max_screen_y, 0],
            [min_screen_x, max_screen_y, 0]
        ]
        
        for i, coord_val in enumerate(new_coords):
            points.SetPoint(i, coord_val)
        
        points.Modified()
