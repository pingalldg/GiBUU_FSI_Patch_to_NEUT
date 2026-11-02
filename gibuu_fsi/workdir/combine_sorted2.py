#!/usr/bin/env python3
"""
combine_sorted.py
=================
Reads FinalEvents_{id}.dat and PertParticles_Init_pos_{id}.dat from a flat
OUTPUT_DIR and writes one ROOT file per campaign.

"""

import argparse
import glob
import os
from typing import Dict, List, Optional, Tuple
import numpy as np
import uproot
import awkward as ak

# Filename prefix/suffix — defined once so extraction is consistent everywhere
_FE_PREFIX = "FinalEvents_"
_FE_SUFFIX = ".dat"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir",  required=True,
                   help="Flat directory containing FinalEvents_{id}.dat etc.")
    p.add_argument("--output-root", required=True,
                   help="Path to write the output ROOT file")
    p.add_argument("--start", type=int, default=None,
                   help="First event ID of campaign (optional filter)")
    p.add_argument("--end",   type=int, default=None,
                   help="Last event ID of campaign (optional filter)")
    return p.parse_args()


def event_id_from_filename(basename):
    # type: (str) -> int
    """Extract integer event ID from e.g. 'FinalEvents_42.dat' → 42.
    Uses plain slicing — works on Python 3.6+."""
    return int(basename[len(_FE_PREFIX):-len(_FE_SUFFIX)])


def parse_final_events(filepath):
    # type: (str) -> Optional[Dict]
    """
    Parse FinalEvents_{id}.dat. Returns dict of lists or None on failure.

    Token layout (0-indexed):
      2=ID  3=Charge  4=perweight  5-7=pos(x,y,z)
      8-11=mom(E,px,py,pz)  12=history  13=prod_id  14=enu
    """
    ids, charges, perweights = [], [], []
    posX, posY, posZ = [], [], []
    momE, momX, momY, momZ = [], [], [], []
    histories, prod_ids, enus = [], [], []

    try:
        with open(filepath) as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                tok = line.split()
                if len(tok) < 15:
                    continue
                try:
                    ids.append(int(tok[2]))
                    charges.append(int(tok[3]))
                    perweights.append(float(tok[4].replace("-318", "e-318")))
                    posX.append(float(tok[5]))
                    posY.append(float(tok[6]))
                    posZ.append(float(tok[7]))
                    momE.append(float(tok[8]))
                    momX.append(float(tok[9]))
                    momY.append(float(tok[10]))
                    momZ.append(float(tok[11]))
                    histories.append(int(tok[12]))
                    prod_ids.append(int(tok[13]))
                    enus.append(float(tok[14]))
                except Exception as e:
                    print("  [WARN] bad line in {}: {}".format(filepath, e))
    except OSError as e:
        print("  [ERROR] {}: {}".format(filepath, e))
        return None

    return dict(
        ids=ids, charges=charges, perweights=perweights,
        posX=posX, posY=posY, posZ=posZ,
        momE=momE, momX=momX, momY=momY, momZ=momZ,
        histories=histories, prod_ids=prod_ids, enus=enus,
    )


def parse_pert_init_pos(filepath):
    # type: (str) -> Tuple[float, float, float]
    """
    Parse PertParticles_Init_pos_{id}.dat.
    Skip comment line, read first data line, return (x, y, z).
    Columns: 0=number 1=ensemble 2=pid 3=charge 4=x 5=y 6=z
    Returns (nan, nan, nan) on any failure.
    """
    try:
        with open(filepath) as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                tok = line.split()
                if len(tok) < 7:
                    print("  [WARN] unexpected format in {}".format(filepath))
                    return np.nan, np.nan, np.nan
                return float(tok[4]), float(tok[5]), float(tok[6])
    except OSError:
        pass
    return np.nan, np.nan, np.nan

def parse_pert_init_mom(filepath):
    # type: (str) -> Tuple[float, float, float, float]
    """
    Parse PertParticles_Init_mom_{id}.dat.
    Skip comment line, read first data line, return (x, y, z).
    Columns: 0=number 1=ensemble 2=pid 3=charge 4=E 5=px 6=py 7=pz
    Returns (nan, nan, nan, nan) on any failure.
    """
    try:
        with open(filepath) as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                tok = line.split()
                if len(tok) < 8:
                    print("  [WARN] unexpected format in {}".format(filepath))
                    return np.nan, np.nan, np.nan, np.nan
                return float(tok[4]), float(tok[5]), float(tok[6]), float(tok[7])
    except OSError:
        pass
    return np.nan, np.nan, np.nan, np.nan

def main():
    args = parse_args()

    # Discover FinalEvents files, sort by event ID numerically
    all_files = sorted(
        glob.glob(os.path.join(args.output_dir, "FinalEvents_*.dat")),
        key=lambda p: event_id_from_filename(os.path.basename(p)),
    )

    # Filter to campaign range if given
    if args.start is not None and args.end is not None:
        all_files = [
            f for f in all_files
            if args.start <= event_id_from_filename(os.path.basename(f)) <= args.end
        ]

    print("Found {} FinalEvents files to process".format(len(all_files)))
    if not all_files:
        print("ERROR: no files found — check --output-dir and campaign range.")
        raise SystemExit(1)

    # Accumulators
    incident_numbers = []
    id_list, charge_list, perweight_list = [], [], []
    posX_list, posY_list, posZ_list = [], [], []
    momE_list, momX_list, momY_list, momZ_list = [], [], [], []
    history_list, prod_id_list, enu_list = [], [], []
    posinitx_list, posinity_list, posinitz_list = [], [], []
    mominitE_list,mominitpx_list,mominitpy_list,mominitpz_list=[],[],[],[]
    skipped = 0
    count_ok = 0

    for fpath in all_files:
        event_id = event_id_from_filename(os.path.basename(fpath))

        # Parse FinalEvents
        parsed = parse_final_events(fpath)
        if parsed is None:
            skipped += 1
            continue

        # Parse PertParticles_Init_pos
        init_pos_path = os.path.join(
            args.output_dir,
            "PertParticles_Init_pos_{}.dat".format(event_id)
        )
        # Parse PertParticles_Init_mom
        init_mom_path = os.path.join(
            args.output_dir,
            "PertParticles_Init_mom_{}.dat".format(event_id)
        )
        posinitx, posinity, posinitz = parse_pert_init_pos(init_pos_path)
        mominitE, mominitpx, mominitpy, mominitpz = parse_pert_init_mom(init_mom_path)
        if np.isnan(posinitx):
            print("  [WARN] event {}: PertParticles_Init_pos missing — NaN stored".format(event_id))
        if np.isnan(mominitpx):
            print("  [WARN] event {}: PertParticles_Init_mom missing — NaN stored".format(event_id))
        incident_numbers.append(event_id)
        id_list.append(np.array(parsed["ids"],        dtype=np.int32))
        charge_list.append(np.array(parsed["charges"], dtype=np.int32))
        perweight_list.append(np.array(parsed["perweights"], dtype=np.float64))
        posX_list.append(np.array(parsed["posX"],     dtype=np.float64))
        posY_list.append(np.array(parsed["posY"],     dtype=np.float64))
        posZ_list.append(np.array(parsed["posZ"],     dtype=np.float64))
        momE_list.append(np.array(parsed["momE"],     dtype=np.float64))
        momX_list.append(np.array(parsed["momX"],     dtype=np.float64))
        momY_list.append(np.array(parsed["momY"],     dtype=np.float64))
        momZ_list.append(np.array(parsed["momZ"],     dtype=np.float64))
        history_list.append(np.array(parsed["histories"], dtype=np.int32))
        prod_id_list.append(np.array(parsed["prod_ids"],  dtype=np.int32))
        enu_list.append(np.array(parsed["enus"],      dtype=np.float64))
        posinitx_list.append(posinitx)
        posinity_list.append(posinity)
        posinitz_list.append(posinitz)
        mominitE_list.append(mominitE)
        mominitpx_list.append(mominitpx)
        mominitpy_list.append(mominitpy)
        mominitpz_list.append(mominitpz)	
        count_ok += 1
        if count_ok % 1000 == 0:
            print("  ... {} events processed".format(count_ok))

    print("\nDone: {} events written, {} skipped".format(count_ok, skipped))

    if count_ok == 0:
        print("ERROR: no events to write.")
        raise SystemExit(1)

    tree = {
        "incident"  : np.array(incident_numbers, dtype=np.int64),
        "ID"        : ak.Array(id_list),
        "Charge"    : ak.Array(charge_list),
        "perweight" : ak.Array(perweight_list),
        "posX"      : ak.Array(posX_list),
        "posY"      : ak.Array(posY_list),
        "posZ"      : ak.Array(posZ_list),
        "momE"      : ak.Array(momE_list),
        "momX"      : ak.Array(momX_list),
        "momY"      : ak.Array(momY_list),
        "momZ"      : ak.Array(momZ_list),
        "history"   : ak.Array(history_list),
        "prod_id"   : ak.Array(prod_id_list),
        "enu"       : ak.Array(enu_list),
        "posinitx"  : np.array(posinitx_list, dtype=np.float64),
        "posinity"  : np.array(posinity_list, dtype=np.float64),
        "posinitz"  : np.array(posinitz_list, dtype=np.float64),
        "mominitE"  : np.array(mominitE_list, dtype=np.float64),
        "mominitpx"  : np.array(mominitpx_list, dtype=np.float64),
        "mominitpy"  : np.array(mominitpy_list, dtype=np.float64),
        "mominitpz"  : np.array(mominitpz_list, dtype=np.float64),    
}

    os.makedirs(os.path.dirname(os.path.abspath(args.output_root)), exist_ok=True)
    print("Writing {} ...".format(args.output_root))
    with uproot.recreate(args.output_root) as f:
        f["Events"] = tree
    print("Done -> {}".format(args.output_root))


if __name__ == "__main__":
    main()

