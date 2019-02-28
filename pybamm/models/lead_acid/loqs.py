#
# Lead-acid LOQS model
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import pybamm
import os


class LOQS(pybamm.BaseModel):
    """Leading-Order Quasi-Static model for lead-acid.

    Attributes
    ----------

    rhs: dict
        A dictionary that maps expressions (variables) to expressions that represent
        the rhs
    initial_conditions: dict
        A dictionary that maps expressions (variables) to expressions that represent
        the initial conditions
    boundary_conditions: dict
        A dictionary that maps expressions (variables) to expressions that represent
        the boundary conditions
    variables: dict
        A dictionary that maps strings to expressions that represent
        the useful variables

    """

    def __init__(self):
        super().__init__()

        whole_cell = ["negative electrode", "separator", "positive electrode"]
        # Variables
        c_e = pybamm.Variable("c", domain=[])
        eps_n = pybamm.Variable("eps_n", domain=[])
        eps_s = pybamm.Variable("eps_s", domain=[])
        eps_p = pybamm.Variable("eps_p", domain=[])

        # Parameters
        sp = pybamm.standard_parameters
        spla = pybamm.standard_parameters_lead_acid
        # Current function
        i_cell = sp.current_with_time

        # ODEs
        j_n = i_cell / sp.l_n
        j_p = -i_cell / sp.l_p
        deps_n_dt = -spla.beta_surf_n * j_n
        deps_p_dt = -spla.beta_surf_p * j_p
        dc_e_dt = (
            1
            / (sp.l_n * eps_n + sp.l_s * eps_s + sp.l_p * eps_p)
            * (
                (sp.s_n - sp.s_p) * i_cell
                - c_e * (sp.l_n * deps_n_dt + sp.l_p * deps_p_dt)
            )
        )
        self.rhs = {
            c_e: dc_e_dt,
            eps_n: deps_n_dt,
            eps_s: pybamm.Scalar(0),
            eps_p: deps_p_dt,
        }
        # Initial conditions
        self.initial_conditions = {
            c_e: spla.c_e_init,
            eps_n: spla.eps_n_init,
            eps_s: spla.eps_s_init,
            eps_p: spla.eps_p_init,
        }
        # ODE model -> no boundary conditions
        self.boundary_conditions = {}

        # Variables
        j0_n = pybamm.interface.exchange_current_density(c_e, ["negative electrode"])
        j0_p = pybamm.interface.exchange_current_density(c_e, ["positive electrode"])
        Phi = -sp.U_n_ref - j_n / (2 * j0_n)
        V = Phi + sp.U_p_ref - j_p / (2 * j0_p)
        # Phis_n = pybamm.Scalar(0)
        # Phis_p = V
        # Concatenate variables
        # eps = pybamm.Concatenation(eps_n, eps_s, eps_p)
        # Phis = pybamm.Concatenation(Phis_n, pybamm.Scalar(0), Phis_p)
        # self.variables = {"c": c, "eps": eps, "Phi": Phi, "Phis": Phis, "V": V}
        self.variables = {
            "c": pybamm.Broadcast(c_e, whole_cell),
            "Phi": pybamm.Broadcast(Phi, whole_cell),
            "V": V,
            "int(epsilon_times_c)dx": (sp.l_n * eps_n + sp.l_s * eps_s + sp.l_p * eps_p)
            * c_e,
        }

        # Overwrite default parameter values
        self.default_parameter_values = pybamm.ParameterValues(
            "input/parameters/lead-acid/default.csv",
            {
                "Typical current density": 1,
                "Current function": os.path.join(
                    os.getcwd(),
                    "pybamm",
                    "parameters",
                    "standard_current_functions",
                    "constant_current.py",
                ),
            },
        )
