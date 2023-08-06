
import os
"""SOCAT: photosynthesis-irradiance parameters for marine phytoplankton


Data DOI:
DOI:10.1594/PANGAEA.874087

References:
DOI:10.5194/essd-10-251-2018

"""
import glob
import pathlib
import zipfile

import numpy as np
import pandas as pd

import requests
import click

DATADIR = os.path.expanduser("~/.oceandata/")
pathlib.Path(DATADIR).mkdir(parents=True, exist_ok=True)

def load(filename="SOCATv6.tsv.zip"):
    """Load tsv file and fix some columns"""
    df = pd.read_csv(os.path.join(DATADIR, FILENAME), sep="\t", skiprows=57)
    df["lat"]    = df["Latitude"]
    df["lon"]    = df["Longitude"]
    df["region"] = df["BG province"]
    df["depth"]  = df["Depth water [m]"]
    df["chl"]    = df["Chl a [µg/l]"]
    df["alpha"]  = df["alpha [(mg C/mg Chl a/h)/(µE/m**2/s)]"] 
    df["PBmax"]  = df["PBmax [mg C/mg Chl a/h]"]
    df["Ek"]     = df["Ek [µmol/m**2/s]"]
    del df["Latitude"], df["Longitude"], df["BG province"]
    del df["Depth water [m]"], df["Chl a [µg/l]"]
    del df["alpha [(mg C/mg Chl a/h)/(µE/m**2/s)]"]
    del df["PBmax [mg C/mg Chl a/h]"], df["Ek [µmol/m**2/s]"]
    df.set_index(pd.DatetimeIndex(df["Date/Time"]), inplace=True)
    del df["Date/Time"]
    return df


def download(url="https://www.socat.info/socat_files/", version="v6",
             filename="SOCATv6.tsv.zip"):
    """Download tsv file from Pangaea server"""
    local_filename = os.path.join(DATADIR, filename)
    try:
        r = requests.get(url=f"{url}/{version}/{filename}",
                         stream=True, timeout=20)
    except requests.ReadTimeout:
        warnings.warn("Connection to server timed out.")
        return False
    if r.ok:
        total_size = int(r.headers.get('Content-Length'))
        if local_filename is None:
            return r.text
        else:
            with open(local_filename, 'wb') as f:
                with click.progressbar(length=total_size,
                                       label='Downloading files') as bar:
                    for chunk in r.iter_content(chunk_size=1024): 
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            bar.update(len(chunk))
            return None
    else:
        raise IOError("Could not download file from server")

def unzip(filename="SOCATv6.tsv.zip"):
    local_filename = os.path.join(DATADIR, filename)
    zip_ref = zipfile.ZipFile(local_filename, 'r')
    zip_ref.extractall(DATADIR)
    zip_ref.close()
