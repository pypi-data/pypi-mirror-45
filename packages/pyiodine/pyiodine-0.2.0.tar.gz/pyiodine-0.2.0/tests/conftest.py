"""
    Common configuration for all the tests
"""

import random

import pytest

from pyiodine.model import Species, Reaction


def random_species():
    """ Function that generates a random species """
    name = "species" + str(random.randint(0, 9999))
    compartment = "default"
    concentration = random.random()
    kind = "variable" if bool(random.randint(0, 1)) else "constant"
    species = Species(name, compartment, concentration, kind)
    return species


@pytest.fixture(scope="module")
def reactants():
    """ Fixture that generates reactants for a reaction """
    n_species = random.randint(2, 4)
    return {random_species(): random.randint(-9, 1) for _ in range(n_species)}


@pytest.fixture(scope="module")
def products():
    """ Fixture that generates products for a reaction """
    n_species = random.randint(1, 4)
    return {random_species(): random.randint(1, 9) for _ in range(n_species)}


@pytest.fixture(scope="module")
def random_reactions():
    """ Fixture that generates random reactions for a model """
    n_reactions = random.randint(2, 6)
    reactions = []
    for i in range(n_reactions):
        n_reactants = random.randint(2, 4)
        reactants = {
            random_species(): random.randint(-9, 1) for _ in range(n_reactants)
        }
        n_products = random.randint(1, 4)
        products = {random_species(): random.randint(1, 9) for _ in range(n_products)}
        name = f"re{i}"
        rxns = {**reactants, **products}
        reversibility = bool(random.randint(0, 1))
        r_species = [k for k, v in rxns.items() if v < 0]
        p_species = [k for k, v in rxns.items() if v > 0]
        param_values = {"km": 1.0e-3, "vm": 100}
        rate_eqn = f"vm*{r_species[0]}/(km+{p_species[0]})"
        reactions.append(Reaction(name, rxns, rate_eqn, param_values, reversibility))
    return reactions
