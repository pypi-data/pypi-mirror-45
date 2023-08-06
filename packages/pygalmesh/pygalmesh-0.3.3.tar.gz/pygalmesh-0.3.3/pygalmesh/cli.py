# -*- coding: utf-8 -*-
#
import argparse
import sys

import meshio

from .__about__ import __version__, __copyright__
from .main import generate_volume_mesh_from_surface_mesh


def volume_from_surface(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)

    mesh = generate_volume_mesh_from_surface_mesh(
        args.infile,
        lloyd=args.lloyd,
        odt=args.odt,
        perturb=args.perturb,
        exude=args.exude,
        edge_size=args.edge_size,
        facet_angle=args.facet_angle,
        facet_size=args.facet_size,
        facet_distance=args.facet_distance,
        cell_radius_edge_ratio=args.cell_radius_edge_ratio,
        cell_size=args.cell_size,
        verbose=not args.quiet,
    )
    meshio.write(args.outfile, mesh)
    return


def _get_parser():
    parser = argparse.ArgumentParser(
        description="Generate volume mesh from surface mesh."
    )

    parser.add_argument("infile", type=str, help="input mesh file")

    parser.add_argument("outfile", type=str, help="output mesh file")

    parser.add_argument(
        "--lloyd",
        "-l",
        type=bool,
        default=False,
        help="Lloyd smoothing (default: false)",
    )

    parser.add_argument(
        "--odt",
        "-o",
        action="store_true",
        default=False,
        help="ODT smoothing (default: false)",
    )

    parser.add_argument(
        "--perturb",
        "-p",
        action="store_true",
        default=False,
        help="perturb (default: false)",
    )

    parser.add_argument(
        "--exude",
        "-x",
        action="store_true",
        default=False,
        help="exude (default: false)",
    )

    parser.add_argument(
        "--edge-size", "-e", type=float, default=0.0, help="edge size (default: 0.0)"
    )

    parser.add_argument(
        "--facet-angle",
        "-a",
        type=float,
        default=0.0,
        help="facet angle (default: 0.0)",
    )

    parser.add_argument(
        "--facet-size", "-s", type=float, default=0.0, help="facet size (default: 0.0)"
    )

    parser.add_argument(
        "--facet-distance",
        "-d",
        type=float,
        default=0.0,
        help="facet distance (default: 0.0)",
    )

    parser.add_argument(
        "--cell-radius-edge-ratio",
        "-r",
        type=float,
        default=0.0,
        help="cell radius/edge ratio (default: 0.0)",
    )

    parser.add_argument(
        "--cell-size", "-c", type=float, default=0.0, help="cell size (default: 0.0)"
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        default=False,
        help="quiet mode (default: False)",
    )

    version_text = ",\n".join(
        [
            "pygalmesh {}".format(__version__),
            "Python {}.{}.{}".format(
                sys.version_info.major, sys.version_info.minor, sys.version_info.micro
            ),
            __copyright__,
        ]
    )
    parser.add_argument("--version", "-v", action="version", version=version_text)

    return parser
