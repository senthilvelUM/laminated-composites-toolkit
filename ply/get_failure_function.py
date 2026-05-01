"""Dispatch helper that returns the ply-failure function for a named criterion.

Used by the runners (and any pipeline function that lets the user
choose between failure criteria) to translate a string toggle like
``failure_criterion = "TsaiWu"`` into the actual function with
signature ``(ply, Sigma12) -> Sf``.

Adding a new criterion (Tsai-Hill, Hashin, ...) means dropping a
new ``ply_failure_<Name>`` next to the existing ones and adding one
elif branch here -- nothing else in the pipeline changes, because
all criteria expose the same return shape.
"""

from ply.ply_failure_Hashin import ply_failure_Hashin
from ply.ply_failure_MaxStress import ply_failure_MaxStress
from ply.ply_failure_TsaiWu import ply_failure_TsaiWu


__all__ = ["get_failure_function"]


def get_failure_function(name):
    """Return the ply-failure function selected by ``name``.

    Parameters
    ----------
    name : str
        One of ``"TsaiWu"``, ``"MaxStress"``, ``"Hashin"``.

    Returns
    -------
    callable
        A function with signature ``(ply, Sigma12) -> Sf``,
        identical in shape across all supported criteria so any
        downstream code can substitute one for another.

    Raises
    ------
    ValueError
        If ``name`` does not match a known criterion.  The message
        lists the valid choices to short-circuit typos.
    """
    if name == "TsaiWu":
        return ply_failure_TsaiWu
    if name == "MaxStress":
        return ply_failure_MaxStress
    if name == "Hashin":
        return ply_failure_Hashin
    raise ValueError(
        f"Unknown failure criterion {name!r}. "
        f"Choose 'TsaiWu', 'MaxStress', or 'Hashin'."
    )
