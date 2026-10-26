from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class Battery:
    """Define the physical characteristics of a battery storage system."""

    power_mw: float
    capacity_mwh: float
    round_trip_efficiency: float = 0.90
    min_soc: float = 0.10
    max_soc: float = 0.90
    initial_soc: float = 0.50
    degradation_cost: float = 5.0

    def __post_init__(self):
        """Validate battery parameters."""

        if self.power_mw <= 0 or self.capacity_mwh <= 0:
            raise ValueError("Power and capacity must be positive")

        if not 0 < self.round_trip_efficiency <= 1:
            raise ValueError("Efficiency must be between 0 and 1")

        if not 0 <= self.min_soc <= self.initial_soc <= self.max_soc <= 1:
            raise ValueError("Invalid SOC configuration")

        if self.degradation_cost < 0:
            raise ValueError("Degradation cost cannot be negative")

    @property
    def charge_efficiency(self) -> float:
        """Return charging efficiency."""
        return sqrt(self.round_trip_efficiency)

    @property
    def discharge_efficiency(self) -> float:
        """Return discharging efficiency."""
        return sqrt(self.round_trip_efficiency)

    @property
    def usable_capacity_mwh(self) -> float:
        """Return energy available within permitted SOC limits."""
        return self.capacity_mwh * (self.max_soc - self.min_soc)

    @property
    def initial_energy_mwh(self) -> float:
        """Return stored energy at the beginning of optimisation."""
        return self.capacity_mwh * self.initial_soc
