"""
    Tests for the species object
"""

import pytest

from pyiodine.model import Species


class TestSpecies:
    """
        Tests for the species object
    """

    def test_initialization(self):
        name = "ahr_gene"
        compartment = "cytoplasm"
        concentration = 10.0
        kind = "constant"
        good_species = Species(
            name=name, compartment=compartment, concentration=concentration, kind=kind
        )
        assert good_species.name == name
        assert good_species.compartment == compartment
        assert good_species.concentration == concentration
        assert good_species.kind == kind
        with pytest.raises(ValueError):
            Species(
                name="ahr gene",
                compartment=compartment,
                concentration=concentration,
                kind=kind,
            )
        with pytest.raises(ValueError):
            Species(
                name=name,
                compartment=compartment,
                concentration=-concentration,
                kind=kind,
            )
        with pytest.raises(ValueError):
            Species(
                name=name,
                compartment=compartment,
                concentration=concentration,
                kind="magic",
            )

    def test_print_declaration(self):
        name = "ahr_gene"
        compartment = "cytoplasm"
        concentration = 10.0
        kind = "constant"
        species = Species(
            name=name, compartment=compartment, concentration=concentration, kind=kind
        )
        actual_declaration = "const species ahr_gene in cytoplasm;"
        assert species.print_declaration() == actual_declaration

    def test_print_concentration(self):
        name = "ahr_gene"
        compartment = "cytoplasm"
        concentration = 10.0
        kind = "constant"
        species = Species(
            name=name, compartment=compartment, concentration=concentration, kind=kind
        )
        actual_init = "ahr_gene = 10.0;"
        assert species.print_concentration() == actual_init
