"""
    Tests for the model object
"""

import pytest
import tellurium as te

from pyiodine.model import Model


@pytest.mark.usefixtures("random_reactions")
class TestModel:
    """
        Tests for the model object
    """

    def test_initialization(self, random_reactions):
        name = "pyiodine"
        compartments = ["default"]
        model = Model(name, compartments)
        assert model.name == name
        assert model.compartments == compartments
        assert len(model.species) == 0
        assert len(model.reactions) == 0
        for reaction in random_reactions:
            species = reaction._reaction.keys()
            for s in species:
                model.add_species(s.name, s.compartment, s.concentration, s.kind)
            rxn_str = reaction.rxn_str.split(":")[-1].strip(";")
            model.add_reaction(
                reaction.name, rxn_str, reaction._rate_eqn, reaction._param_values
            )
        assert len(model.reactions) == len(random_reactions)

    # NOTE: The other print functions should already be tested in `Reaction` and `Species` tests
    def test_print_compartments(self, random_reactions):
        name = "pyiodine"
        compartments = ["default"]
        model = Model(name, compartments)
        for reaction in random_reactions:
            species = reaction._reaction.keys()
            for s in species:
                model.add_species(s.name, s.compartment, s.concentration, s.kind)
            rxn_str = reaction.rxn_str.split(":")[-1].strip(";")
            model.add_reaction(
                reaction.name, rxn_str, reaction._rate_eqn, reaction._param_values
            )
        assert model.print_compartments() == [
            "const compartment default;",
            "default = 1;",
        ]

    def test_print_model(self, random_reactions):
        name = "pyiodine"
        compartments = ["default"]
        model = Model(name, compartments)
        for reaction in random_reactions:
            species = reaction._reaction.keys()
            for s in species:
                model.add_species(s.name, s.compartment, s.concentration, s.kind)
            rxn_str = reaction.rxn_str.split(":")[-1].strip(";")
            model.add_reaction(
                reaction.name, rxn_str, reaction._rate_eqn, reaction._param_values
            )
        assert te.loada(model.print_model())
