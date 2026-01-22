"""
Geometry module for creating 3D objects.
"""
import vtk
import math


class MaterialFactory:
    """Factory for creating materials and properties."""
    
    @staticmethod
    def create_metallic_material(color=(0.8, 0.8, 0.8)):
        """Create a metallic material property."""
        prop = vtk.vtkProperty()
        prop.SetColor(*color)
        prop.SetSpecular(0.9)
        prop.SetSpecularPower(64)
        prop.SetAmbient(0.2)
        prop.SetDiffuse(0.7)
        return prop
    
    @staticmethod
    def create_matte_material(color=(0.8, 0.2, 0.2)):
        """Create a matte material property."""
        prop = vtk.vtkProperty()
        prop.SetColor(*color)
        prop.SetSpecular(0.2)
        prop.SetSpecularPower(16)
        prop.SetAmbient(0.3)
        prop.SetDiffuse(0.8)
        return prop
    
    @staticmethod
    def create_glossy_material(color=(0.2, 0.5, 0.9)):
        """Create a glossy material property."""
        prop = vtk.vtkProperty()
        prop.SetColor(*color)
        prop.SetSpecular(0.6)
        prop.SetSpecularPower(32)
        prop.SetAmbient(0.25)
        prop.SetDiffuse(0.75)
        return prop


class CuboidFactory:
    """Factory class for creating cuboid geometry."""
    
    @staticmethod
    def create_cuboid(width=1.0, height=1.0, depth=1.0):
        """
        Create a cuboid (box) geometry.
        
        Args:
            width: X-dimension size
            height: Y-dimension size
            depth: Z-dimension size
            
        Returns:
            vtkPolyDataMapper with cuboid geometry
        """
        # Create a cube source
        cube = vtk.vtkCubeSource()
        cube.SetXLength(width)
        cube.SetYLength(height)
        cube.SetZLength(depth)
        cube.Update()
        
        # Create mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube.GetOutputPort())
        
        return mapper
    
    @staticmethod
    def create_actor(mapper, color=(1.0, 1.0, 1.0), material_type="matte"):
        """
        Create a vtkActor with the given mapper and color.
        
        Args:
            mapper: vtkPolyDataMapper
            color: RGB tuple (0-1 range)
            material_type: "matte", "metallic", or "glossy"
            
        Returns:
            vtkActor
        """
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        # Apply material
        if material_type == "metallic":
            prop = MaterialFactory.create_metallic_material(color)
        elif material_type == "glossy":
            prop = MaterialFactory.create_glossy_material(color)
        else:
            prop = MaterialFactory.create_matte_material(color)
        
        actor.SetProperty(prop)
        actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)
        
        return actor


class GeometryHelper:
    """Helper functions for geometry operations."""
    
    @staticmethod
    def get_actor_center(actor):
        """Get center of actor bounds."""
        bounds = actor.GetBounds()
        center = (
            (bounds[0] + bounds[1]) / 2,
            (bounds[2] + bounds[3]) / 2,
            (bounds[4] + bounds[5]) / 2
        )
        return center
    
    @staticmethod
    def get_actor_dimensions(actor):
        """Get dimensions of actor bounds."""
        bounds = actor.GetBounds()
        dimensions = (
            bounds[1] - bounds[0],
            bounds[3] - bounds[2],
            bounds[5] - bounds[4]
        )
        return dimensions
