import os
import shutil
import cProfile
import pstats
from bdb import BdbQuit
from pathlib import Path

import click

import vivarium
from vivarium.framework.engine import run_simulation
from .utilities import verify_yaml

import logging
logging.getLogger(__name__)


@click.group()
def simulate():
    pass


@simulate.command()
@click.argument('model_specification', callback=verify_yaml,
                type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option('--results_directory', '-o', type=click.Path(resolve_path=True),
              default=os.path.expanduser('~/vivarium_results/'),
              help='Top level output directory to write results to')
@click.option('--verbose', '-v', is_flag=True, help='Report each time step')
@click.option('--log', type=click.Path(dir_okay=False, resolve_path=True), help='Path to log file')
@click.option('--pdb', 'with_debugger', is_flag=True, help='Drop into python debugger if an error occurs.')
def run(model_specification, results_directory, verbose, log, with_debugger):
    log_level = logging.DEBUG if verbose else logging.ERROR
    logging.basicConfig(filename=log, level=log_level)

    try:
        run_simulation(model_specification, results_directory)
    except (BdbQuit, KeyboardInterrupt):
        raise
    except Exception as e:
        if with_debugger:
            import pdb
            import traceback
            traceback.print_exc()
            pdb.post_mortem()
        else:
            logging.exception("Uncaught exception {}".format(e))
            raise


@simulate.command()
def test():
    logging.basicConfig(level=logging.DEBUG)
    model_specification = Path(vivarium.__file__).resolve().parent / 'examples' / 'disease_model' / 'disease_model.yaml'
    results_directory = Path('~/vivarium_results').expanduser()

    try:
        run_simulation(str(model_specification), str(results_directory))
        click.echo()
        click.secho("Installation test successful!", fg='green')
    except (BdbQuit, KeyboardInterrupt):
        raise
    except Exception as e:
        logging.exception("Uncaught exception {}".format(e))
        raise
    finally:
        shutil.rmtree(results_directory, ignore_errors=True)


@simulate.command()
@click.argument('model_specification', callback=verify_yaml,
                type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option('--results_directory', '-o', type=click.Path(resolve_path=True),
              default=os.path.expanduser('~/vivarium_results/'),
              help='Top level output directory to write results to')
@click.option('--process/--no-process', default=False,
               help=('Automatically process the profile to human readable format  with pstats, '
                     'sorted by cumulative runtime, and dump to a file'))
def profile(model_specification, results_directory, process):
    model_specification = Path(model_specification)
    results_directory = Path(results_directory)

    out_stats_file = results_directory / f'{model_specification.name}'.replace('yaml', 'stats')
    command = f'run_simulation("{model_specification}", "{results_directory}")'
    cProfile.runctx(command, globals=globals(), locals=locals(), filename=out_stats_file)

    if process:
        out_txt_file = results_directory / (out_stats_file.name + '.txt')
        with open(out_txt_file, 'w') as f:
            p = pstats.Stats(str(out_stats_file), stream=f)
            p.sort_stats('cumulative')
            p.print_stats()

