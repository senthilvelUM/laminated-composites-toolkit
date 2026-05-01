"""Verify consistency of the laminate input lists before analysis."""


def check_laminate_inputs(N, ply_materials, ply_orientations, ply_thicknesses):
    """Check that the three parallel ply lists all have length N.

    Called at the top of a laminate run script to catch size-mismatch
    errors before create_laminate() is called.

    Parameters
    ----------
    N : int
        Declared number of plies.
    ply_materials : list of str
        Material names, one per ply.
    ply_orientations : list of float
        Ply orientation angles, one per ply.
    ply_thicknesses : list of float
        Ply thicknesses, one per ply.

    Raises
    ------
    AssertionError
        If any of the three lists has a length other than N.
    """
    assert len(ply_materials) == N, "ply_materials length must equal N"
    assert len(ply_orientations) == N, "ply_orientations length must equal N"
    assert len(ply_thicknesses) == N, "ply_thicknesses length must equal N"
