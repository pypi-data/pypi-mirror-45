# Copyright 2019 Thomas W. D. Möbius
#
# This file is part of fmristats.
#
# fmristats is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# fmristats is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# It is not allowed to remove this copy right statement.

"""

Takes the *.par file from FSL as input and outputs the respective
reference maps instance for fmristats.

"""

from ..epilog import epilog

import argparse

def define_parser():
    parser = argparse.ArgumentParser(
            description=__doc__,
            epilog=epilog)

    ####################################################################
    # Specific arguments
    ####################################################################

    specific = parser.add_argument_group(
        """Arguments controlling the parsing""")

    specific.add_argument('--par',
            help="""Path to the par files""")

    specific.add_argument('--par-path',
            default='',
            help="""Prefix path to the par files""")

    specific.add_argument('--par-cycle',
            type=int,
            help="""The realignment parameters (Euler angles and
            transformations) saved by McFLIRT are given with respect to
            the centre of mass of the reference scan cycle (Why do you
            have to make just *everything* so complicated, FSL?!). We
            need to apply a translation from the centre of mass of the
            reference cycle to the coordinate system of the session. It
            is for you to find out which scan cycle that is. By default
            it will be some cycle in the middle of the session.""")

    specific = parser.add_argument_group(
        """Arguments for the subject reference space""")

    specific.add_argument('--cycle',
        type=int,
        nargs='+',
        help="""Use the data in scan cycle CYCLE as a template for
        the subject reference space. Enumeration starts at 0 (i.e. the
        first scan cycle is cycle 0). It will be checked whether the
        specified cycle has been marked as a potential outlier (i.e. a
        scan cycle that shows more head movements that usual). You won't
        be able to set an outlying scan cycle as reference. More than
        one cycle can be specified, though, and the list will be used as
        fall backs.""")

    specific.add_argument('--grubbs',
        type=float,
        default=0.1,
        help="""An outlier detection is performed to identify scans
        which may have been acquired during severe head movements. More
        precisely, a Grubbs' outlying test will be performed on the set
        of estimated principle semi axis for each full scan cycle on the
        given level of significance. When using fmririgid to create
        ReferenceMaps, the default is 0.1, and the information of
        outlying scans is saved to disk together with the estimated
        rigid body transformations. Then, when running fmrifit, this
        information is used. When setting --grubbs in fmrifit, outlier
        estimation is performed again.""")

    specific.add_argument('--window-radius',
        type=int,
        nargs='+',
        default=[0],
        help="""Calculate the mean rigid transformation using the this
        window. A --window-radius of 0 does not do anything (the
        default). A WINDOW_RADIUS of n corresponds to all rigid
        transformation n scan cycle before and after each time point
        (including the boundary). Can also be used iteratively by
        providing more than one argument. This effectively produces a
        weighted averaging of rigid transformations.""")

    specific.add_argument('--new-rigids',
            default='fsl',
            help="""Name of the rigid transformations.""")

    ####################################################################
    # File handling
    ####################################################################

    file_handling = parser.add_argument_group(
        """File handling""")

    lock_handling = file_handling.add_mutually_exclusive_group()

    lock_handling.add_argument('-r', '--remove-lock',
        action='store_true',
        help="""Remove lock, if file is locked. This is useful, if used
        together with -s/--skip to remove orphan locks.""")

    lock_handling.add_argument('-i', '--ignore-lock',
        action='store_true',
        help="""Ignore lock, if file is locked. Together with -s/--skip
        this will also remove orphan locks.""")

    skip_force = file_handling.add_mutually_exclusive_group()

    skip_force.add_argument('-f', '--force',
        action='store_true',
        help="""Force re-writing any files""")

    skip_force.add_argument('-s', '--skip',
        action='store_true',
        help="""Do not perform any calculations.""")

    ####################################################################
    # Verbosity
    ####################################################################

    control_verbosity  = parser.add_argument_group(
        """Control the level of verbosity""")

    control_verbosity.add_argument('-v', '--verbose',
        action='count',
        default=0,
        help="""Increase output verbosity""")

    ####################################################################
    # Push
    ####################################################################

    control_verbosity  = parser.add_argument_group(
        """Control whether to save the modified (thus overwrite the
        existing) study instance.""")

    control_verbosity.add_argument('-p', '--push',
        action='store_true',
        help="""Will save the modified (and thus overwrite the existing)
        study instance.""")

    ####################################################################
    # Multiprocessing
    ####################################################################

    control_multiprocessing  = parser.add_argument_group(
        """Multiprocessing""")

    control_multiprocessing.add_argument('-j', '--cores',
        type=int,
        default=1,
        help="""Number of threads to use. The implementation will
        usually try to run as many calculations and loops as possible in
        parallel -- this may suggest that it may be adventurous to
        process all entries in the study protocol sequentially (and this
        is the default). It is possible, however, to generate a thread
        for each protocol entry. Note that this may generate a lot of
        I/O-operations. If you set CORES to 0, then the number of cores
        on the machine will be used.""")

    return parser

from .fmristudy import add_study_arguments

def cmd():
    parser = define_parser()
    add_study_arguments(parser)
    args = parser.parse_args()
    call(args)

cmd.__doc__ = __doc__

########################################################################
#
# Load libraries
#
########################################################################

import os

from os.path import isfile, isdir, join

from multiprocessing.dummy import Pool as ThreadPool

import pandas as pd

import numpy as np

from nibabel.eulerangles import euler2mat, mat2euler

from nibabel.affines import from_matvec

from .fmristudy import get_study

from ..lock import Lock

from ..study import Study

from ..reference import ReferenceMaps

from ..affines import Affine, Affines

########################################################################

def par2referenceFSL (par_file, session, par_cycle):
    rigids_euler = np.array(pd.read_csv(par_file, header=None, delimiter='\s+'))
    number_of_cycles = rigids_euler.shape[0]
    rigids = np.empty((number_of_cycles, 4, 4))
    for i in range(number_of_cycles):
        mat = euler2mat(
            -rigids_euler[i,0], # gieren / yaw   / z
            -rigids_euler[i,1], # rollen / roll  / y
            rigids_euler[i,2]) # nicken / pitch / x
        vec = rigids_euler[i,3:]
        rigids[i] = from_matvec(
            matrix=mat,
            vector=np.array((-vec[1], vec[0], -vec[2])))
    reference_maps = ReferenceMaps(session.name)
    reference_maps.temporal_resolution = session.temporal_resolution
    reference_maps.slice_timing = session.slice_timing
    reference_maps.set_acquisition_maps(Affines(rigids))
    reference_maps.shape = (session.numob, session.shape[session.ep])

    # The realignment parameters (Euler angles and transformations)
    # saved by McFLIRT are given with respect to the centre of mass of
    # the reference scan cycle (Why do you have to make *everything* so
    # complicated, FSL?!). We need to apply a translation from the
    # centre of mass of the reference cycle to the coordinate system of
    # the session.

    n,x,y,z = session.data.shape
    indices = ((slice(0,x), slice(0,y), slice(0,z)))
    lattice = session.reference.apply_to_indices(indices)
    lattice = np.moveaxis(lattice, -1 ,0)
    com = (session.raw[par_cycle] * lattice).sum(axis=(1,2,3)) / session.raw[par_cycle].sum()

    translation_from_com = Affine(from_matvec(np.eye(3), -com))
    reference_maps.reset_reference_space(x=translation_from_com)
    return reference_maps

def call(args):

    ####################################################################
    # Options
    ####################################################################

    remove_lock       = args.remove_lock
    ignore_lock       = args.ignore_lock
    force             = args.force
    skip              = args.skip
    verbose           = args.verbose

    par_cycle     = args.par_cycle
    cycle         = args.cycle
    grubbs        = args.grubbs
    window_radius = args.window_radius

    ####################################################################
    # Study
    ####################################################################

    study = get_study(args)

    if study is None:
        print('Nothing to do.')
        return

    study.set_rigids(args.new_rigids)

    ####################################################################
    # Iterator
    ####################################################################

    study.update_layout({
        'par_file' : join(args.par_path, args.par),
        })

    study_iterator = study.iterate('session', 'reference_maps',
            new=['reference_maps', 'par_file'],
            integer_index=True,
            verbose=args.verbose)

    df = study_iterator.df.copy()

    df['locked'] = False

    ####################################################################
    # Wrapper
    ####################################################################

    def wm(index, name, session, reference_maps, file_reference_maps,
            par_file):
        if session is None:
            df.ix[index,'valid'] = False
            print('{}: Unable to open session.'.format(name.name()))
            return

        if type(reference_maps) is Lock:
            if remove_lock or ignore_lock:
                if verbose:
                    print('{}: Remove lock'.format(name.name()))
                reference_maps.unlock()
                if remove_lock:
                    return
            else:
                if verbose:
                    print('{}: Locked'.format(name.name()))
                return

        elif reference_maps is not None and not force:
            if verbose:
                print('{}: ReferenceMaps already exists. Use -f/--force to overwrite'.format(
                    name.name()))
            return

        if skip:
            return

        if verbose:
            print('{}: Lock: {}'.format(name.name(), file_reference_maps))

        lock = Lock(name, 'fmririgid', file_reference_maps)
        df.ix[index, 'locked'] = True

        dfile = os.path.dirname(file_reference_maps)
        if dfile and not isdir(dfile):
           os.makedirs(dfile)

        lock.save(file_reference_maps)

        ####################################################################
        # Rigid body transformations
        ####################################################################

        if verbose:
            print('{}: Read rigid body transformations'.format(name.name()))

        reference_maps = par2referenceFSL(par_file, session, par_cycle)

        ####################################################################
        # Detect outlying scan cycles
        ####################################################################

        if not np.isclose(grubbs, 1):
            if verbose:
                print('{}: Detect outlying scans'.format(name.name()))
            reference_maps.detect_outlying_scans(grubbs)
            outlying_cycles = reference_maps.outlying_cycles
        else:
            outlying_cycles = None

        ####################################################################
        # Reset reference space
        ####################################################################

        if (outlying_cycles is None) or (cycle is None):
            reference_maps.reset_reference_space(cycle=cycle)
        else:
            if outlying_cycles[cycle].all():
                df.ix[index,'valid'] = False
                print("""{}: All suggested reference cycles have been
                marked as outlying. Unable to proceed. Please specify a
                different scan cycle (using --cycle) as reference.""".format(name.name()))
                lock.conditional_unlock(df, index, verbose, True)
                return
            elif outlying_cycles[cycle].any():
                for c, co in zip (cycle, outlying_cycles[cycle]):
                    if co:
                        print("""{}: Cycle {:d} marked as outlying, using fallback.""".format(
                            name.name(), c))
                    else:
                        print("""{}: Reference cycle is {:d}.""".format(
                            name.name(), c))
                        reference_maps.reset_reference_space(cycle=c)
                        break
            else:
                print("""{}: Reference cycle is {:d}.""".format(name.name(), cycle[0]))
                reference_maps.reset_reference_space(cycle=cycle[0])

        ####################################################################
        # Average rigid body transformations
        ####################################################################

        for r in window_radius:
            if r > 0:
                if verbose:
                    print('{}: Flatten head locations using a radius of {} scan cycles'.format(
                        name.name(), r))
                reference_maps.mean(r)

        ####################################################################
        # Save to disk
        ####################################################################

        try:
            if verbose:
                print('{}: Save: {}'.format(name.name(), file_reference_maps))

            reference_maps.save(file_reference_maps)
            df.ix[index,'locked'] = False

        except Exception as e:
            df.ix[index,'valid'] = False
            print('{}: Unable to create: {}'.format(name.name(), file_reference_maps))
            print('{}: Exception: {}'.format(name.name(), e))
            lock.conditional_unlock(df, index, verbose, True)
            return

    ####################################################################

    if args.cores == 0:
        args.cores = None

    if len(df) > 1 and ((args.cores is None) or (args.cores > 1)):
        try:
            pool = ThreadPool(args.cores)
            for index, name, files, instances in study_iterator:
                session         = instances['session']
                reference_maps  = instances['reference_maps']
                file_reference_maps = files['reference_maps']
                par_file = files['par_file']

                if session is None:
                    print('{}: No Session found'.format(name.name()))
                else:
                    pool.apply_async(wm, args=\
                    (index, name, session, reference_maps,
                        file_reference_maps, par_file)
                    )

            pool.close()
            pool.join()
        except Exception as e:
            pool.close()
            pool.terminate()
            print('Pool execution has been terminated')
            print(e)
        finally:
            files = df.ix[df.locked, 'reference_maps'].values
            if len(files) > 0:
                for f in files:
                    print('Unlock: {}'.format(f))
                    os.remove(f)
    else:
        try:
            print('Process protocol entries sequentially')
            for index, name, files, instances in study_iterator:
                session         = instances['session']
                reference_maps  = instances['reference_maps']
                file_reference_maps = files['reference_maps']
                par_file = files['par_file']

                if session is None:
                    print('{}: No Session found'.format(name.name()))
                else:
                    wm(index, name, session, reference_maps,
                            file_reference_maps, par_file)
        finally:
            files = df.ix[df.locked, 'reference_maps'].values
            if len(files) > 0:
                for f in files:
                    print('Unlock: {}'.format(f))
                    os.remove(f)

    ####################################################################
    # Write study to disk
    ####################################################################

    if args.out is not None:
        if args.verbose:
            print('Save: {}'.format(args.out))

        dfile = os.path.dirname(args.out)
        if dfile and not isdir(dfile):
           os.makedirs(dfile)

        study.save(args.out)

    if args.push:
        if args.verbose:
            print('Save: {}'.format(args.study))
        study.save(args.study)
