#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
import argparse

__all__ = ['create_parser']

def create_parser():
    """Create the argument parser for the main application.

    Returns
    -------
    argparse.ArgumentParser
        The application command-line parser.
    """
    description = ['This is the UI for running the Dome Seeing Monitor.']

    parser = argparse.ArgumentParser(description=' '.join(description),
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--profile', dest='profile', action='store_true',
                        help='Supply a filename to trigger profiling the code.')
    parser.add_argument('-t', '--telemetry_dir', dest='telemetry_dir',
                        help='Provide an alternater full path for telemetry saving.')
    parser.add_argument('-c', '--config', dest='config_file',
                        help='Supply a YAML configuration file.')

    return parser
