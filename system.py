from grid import Grid
from typing import Callable

ALL_DIMENSIONALITIES_ALLOWED = -1
# TODO: Odd only?
# TODO: Even only?


class SystemRule:

    def __init__(self, allowed_dimensionalities: list[int], tf: Callable[..., Grid], *tfargs) -> None:
        self.allowed_dimensionalities = allowed_dimensionalities
        # TODO: Current implementation of transition function has a field of view of one previous generation
        #       For true genericity, our implementation should support a configurable field of view
        self.tf = tf
        self.tfargs = tfargs


class System:

    def __init__(self, gen0: Grid, system_rule: SystemRule) -> None:
        assert len(gen0.dimensions) in system_rule.allowed_dimensionalities\
            or system_rule.allowed_dimensionalities == ALL_DIMENSIONALITIES_ALLOWED,\
            "The chosen system rule does not support this grid's dimensionality"

        self.generations = [gen0]
        self.system_rule = system_rule

    def __evolve(self) -> None:

        self.generations.append(

            self.system_rule.tf(

                self.get_latest_gen(),
                self.system_rule.tfargs

            )

        )

    def get_latest_gen(self) -> Grid:
        return self.generations[-1]

    def get_next_gen(self) -> Grid:
        self.__evolve()
        return self.get_latest_gen()

    # TODO:
    # def get_gen(n) -> Grid:

    # TODO:
    # def evolve_to(n) -> None:
