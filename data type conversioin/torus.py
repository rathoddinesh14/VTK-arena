# mesh a torus
import meshio
import SeismicMesh

hmin = 0.10

torus = SeismicMesh.Torus(r1=1.0, r2=0.5)
points, cells = SeismicMesh.generate_mesh(
    domain=torus,
    edge_length=hmin,
)
points, cells = SeismicMesh.sliver_removal(
    points=points, domain=torus, edge_length=hmin
)
meshio.write_points_cells(
    "torus.vtk",
    points,
    [("tetra", cells)],
)