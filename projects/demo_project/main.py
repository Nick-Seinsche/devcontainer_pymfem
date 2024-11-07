import mfem.ser as mfem
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np

from pathlib import Path

ROOT = Path("/workspaces/devcontainer_pymfem/")

mesh = mfem.Mesh.MakeCartesian2D(
    nx=10, ny=10, type=mfem.Element.TRIANGLE,
    generate_edges=True, sx=1.0, sy=1.0
)

mesh.Print(str(ROOT / "projects" / "demo_project" / 'exported_mesh2.mesh'), 8)

# Define the finite element function space
fec = mfem.H1_FECollection(1, mesh.Dimension())  # H1 order=1
fespace = mfem.FiniteElementSpace(mesh, fec)

# Define the essential dofs
ess_tdof_list = mfem.intArray()
ess_bdr = mfem.intArray([1] * mesh.bdr_attributes.Size())
# given the fespace, writes to ess_tdof_list the list of
# vertex indices that are not fixed by eg. diriclet bc.
fespace.GetEssentialTrueDofs(ess_bdr, ess_tdof_list)

# Define constants for alpha (diffusion coefficient) and f (RHS)
alpha = mfem.ConstantCoefficient(1.0)
rhs = mfem.ConstantCoefficient(1.0)

"""
Note
-----
In order to represent a variable diffusion coefficient, you
must use a numba-JIT compiled function. For example:

>>> @mfem.jit.scalar
>>> def alpha(x):
>>>     return x+1.0
"""

# Define the bilinear and linear operators
a = mfem.BilinearForm(fespace)
a.AddDomainIntegrator(mfem.DiffusionIntegrator(alpha))
a.Assemble()
b = mfem.LinearForm(fespace)
b.AddDomainIntegrator(mfem.DomainLFIntegrator(rhs))
b.Assemble()

# Initialize a gridfunction to store the solution vector
x = mfem.GridFunction(fespace)
x.Assign(0.0)

# Form the linear system of equations (AX=B)
A = mfem.OperatorPtr()
B = mfem.Vector()
X = mfem.Vector()
a.FormLinearSystem(ess_tdof_list, x, b, A, X, B)
print("Size of linear system: " + str(A.Height()))

# Solve the linear system using PCG and store the solution in x
AA = mfem.OperatorHandle2SparseMatrix(A)
M = mfem.GSSmoother(AA)
mfem.PCG(AA, M, B, X, 1, 200, 1e-12, 0.0)
a.RecoverFEMSolution(X, b, x)

# Extract vertices and solution as numpy arrays
verts = mesh.GetVertexArray()
sol = x.GetDataArray()

# Plot the solution using matplotlib
verts = np.array(verts)

triang = tri.Triangulation(verts[:, 0], verts[:, 1])

fig, ax = plt.subplots()
ax.set_aspect("equal")
tpc = ax.tripcolor(triang, sol, shading="gouraud")
fig.colorbar(tpc)

plt.savefig("/workspaces/devcontainer_pymfem/projects/demo_project/plot.png")
