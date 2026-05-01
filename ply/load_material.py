"""Load ply material properties from a YAML file."""

from pathlib import Path
import yaml


def load_material(name):
    """Read a material YAML file and return its properties as a dictionary.

    The material file is expected at materials/{name}.yaml.
    All numerical values are in SI units: Pa for moduli and strengths,
    kg/m^3 for density. Ply thickness is not a material property —
    it is specified per ply in create_ply().

    Parameters
    ----------
    name : str
        Material name, e.g. "unidirectional_carbon_epoxy".
        Corresponds to materials/{name}.yaml.

    Returns
    -------
    dict
        Dictionary with keys: name, type, rho,
        E1, E2, nu12, G12, G13, G23, F1t, F1c, F2t, F2c, F6.
    """
    #  Resolve the path relative to this file's location (the project
    #  root is the parent of the ply/ package directory) rather than
    #  the cwd, so the function works no matter where the runner is
    #  invoked from -- including subfolders like worked_examples/.
    project_root = Path(__file__).resolve().parent.parent
    path = project_root / "materials" / f"{name}.yaml"
    with open(path, "r") as f:
        material = yaml.safe_load(f)

    # Coerce numerical fields to float. This guards against the YAML 1.1
    # quirk where values like "167.4e9" (no sign on the exponent) are
    # parsed as strings instead of floats.
    numeric_keys = ["rho", "E1", "E2", "nu12", "G12", "G13", "G23",
                    "F1t", "F1c", "F2t", "F2c", "F6"]
    for key in numeric_keys:
        material[key] = float(material[key])

    return material
