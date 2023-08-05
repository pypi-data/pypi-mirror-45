"""
    Tests for the reaction object
"""

import pytest
import sympy

from pyiodine.model import Reaction


@pytest.mark.usefixtures("reactants", "products")
class TestReaction:
    """
        Tests for the reaction object
    """

    def test_initialization_good(self, reactants, products):
        name = "re1"
        rxns = {**reactants, **products}
        r_species = [k for k, v in rxns.items() if v < 0]
        p_species = [k for k, v in rxns.items() if v > 0]
        param_values = {"km": 1.0e-3, "vm": 100}
        rate_eqn = f"vm*{r_species[0]}/(km+{p_species[0]})"
        reversibility = True
        reaction = Reaction(name, rxns, rate_eqn, param_values, reversibility)
        assert reaction.name == name
        assert reaction.reactants == r_species
        assert reaction.products == p_species

    def test_initialization_bad(self, reactants, products):
        name = "re1"
        rxns = {**reactants, **products}
        r_species = [k for k, v in rxns.items() if v < 0]
        p_species = [k for k, v in rxns.items() if v > 0]
        param_values = {"km": 1.0e-3, "vm": 100}
        rate_eqn = f"vm*{r_species[0]}/(km+{p_species[0]})"
        reversibility = True
        with pytest.raises(ValueError):
            Reaction("re 2", rxns, rate_eqn, param_values, reversibility)
        with pytest.raises(ValueError):
            Reaction(
                name,
                rxns,
                "vm'*{r_species[0]}/(km+{p_species[0]})",
                param_values,
                reversibility,
            )

    def test_param_update(self, reactants, products):
        name = "re1"
        rxns = {**reactants, **products}
        r_species = [k for k, v in rxns.items() if v < 0]
        p_species = [k for k, v in rxns.items() if v > 0]
        param_values = {"km": 1.0e-3, "vm": 100}
        rate_eqn = f"vm*{r_species[0]}/(km+{p_species[0]})"
        reversibility = True
        reaction = Reaction(name, rxns, rate_eqn, param_values, reversibility)
        reaction.update_param("km", 1)
        assert reaction.parameters == {"km": 1, "vm": 100}
        with pytest.raises(KeyError):
            reaction.update_param("re1_km", 100)

    def test_print_declaration(self, reactants, products):
        name = "re1"
        reactant_list = list(reactants)
        product_list = list(products)
        reactant1 = reactant_list[0]
        reactant2 = reactant_list[1]
        product = product_list[0]
        rxns = {reactant1: -1, reactant2: -2, product: 1}
        param_values = {"km": 1.0e-3, "k": 100}
        rate_eqn = f"k*{reactant1}*{reactant2}/(km+{product}**2)"
        reversibility = True
        actual_rxn = f"{name}: {reactant1} + 2 {reactant2} -> {product};"
        actual_rate_eqn = f"{name}_k*{reactant1}*{reactant2}/({name}_km+{product}**2)"
        reaction = Reaction(name, rxns, rate_eqn, param_values, reversibility)
        assert actual_rxn == reaction.rxn_str
        assert sympy.sympify(actual_rate_eqn) == sympy.sympify(
            reaction.rate_eqn_str.strip(";")
        )

    def test_print_parameters(self, reactants, products):
        name = "re1"
        rxns = {**reactants, **products}
        r_species = [k for k, v in rxns.items() if v < 0]
        p_species = [k for k, v in rxns.items() if v > 0]
        param_values = {"km": 1.0e-3, "vm": 100}
        rate_eqn = f"vm*{r_species[0]}/(km+{p_species[0]})"
        reversibility = True
        reaction = Reaction(name, rxns, rate_eqn, param_values, reversibility)
        actual_parameters = [
            f"re1_km = {param_values['km']};",
            f"re1_vm = {param_values['vm']};",
        ]
        assert reaction.print_parameters() == actual_parameters
