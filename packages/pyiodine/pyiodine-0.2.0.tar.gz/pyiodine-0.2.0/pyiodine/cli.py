"""
    Console script for pyiodine
"""

import os
import sys

import click

from . import pyiodine
from .simulation import Simulator


@click.command()
@click.option("--timespan", "-t", default=80, type=int)
@click.option("--grid", "-g", default=False, type=bool)
@click.option("--log", "-l", default=False, type=bool)
@click.option("--plot_interval", "-pt", default=None, type=str)
@click.argument("folder_path", type=click.Path())
def simulate(timespan, grid, log, plot_interval, folder_path):
    """Console script to simulate the pyiodine"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    model_file = os.path.join(folder_path, "model.txt")
    if plot_interval:
        start, end = plot_interval.split("-")
        plot_interval = (int(start), int(end))
    with open(model_file, "w") as fid:
        fid.write(pyiodine.print_model())
    simulator = Simulator(pyiodine)
    timeseries_df = simulator.simulate(timespan)
    csv_file = os.path.join(folder_path, "data.csv")
    timeseries_df.to_csv(csv_file)
    if grid:
        plot_file_grid = os.path.join(folder_path, "simulation_grid.png")
        Simulator.plot(
            timeseries_df, plot_file_grid, grid=grid, plot_interval=plot_interval
        )
        if log:
            plot_file_grid_log = os.path.join(folder_path, "simulation_grid_log.png")
            Simulator.plot(
                timeseries_df,
                plot_file_grid_log,
                grid=grid,
                log=log,
                plot_interval=plot_interval,
            )
    plot_file = os.path.join(folder_path, "simulation.png")
    Simulator.plot(timeseries_df, plot_file, plot_interval=plot_interval)
    if log:
        plot_file_log = os.path.join(folder_path, "simulation_log.png")
        Simulator.plot(
            timeseries_df, plot_file_log, log=log, plot_interval=plot_interval
        )


if __name__ == "__main__":
    simulate()
