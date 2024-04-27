class Constants:

    CODE_HEADER: str = r""" 
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
import numpy as np
import pandas as pd
from typing import Callable, Tuple, Any, Union, List
import itertools
from sklearn.metrics import confusion_matrix, roc_curve
from sklearn.preprocessing import quantile_transform

# configure plotting style
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 11

FONT = {"family": "serif", "serif": ["Times"], "size": MEDIUM_SIZE}

rc("axes", titlesize=MEDIUM_SIZE)  # fontsize of the axes title
rc("axes", labelsize=SMALL_SIZE)  # fontsize of the x and y labels
rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title

rc("font", **FONT)
rc("text", usetex=True)

# define text width in pt; you can obtain 
# this from your latex editor by
# compiling \the\textwidth
TEXT_WIDTH = 360.0


def set_size(
    width: float = TEXT_WIDTH, fraction: float = 1.0, subplots: tuple = (1, 1)
) -> Tuple[float, float]:
    '''
    Set figure dimensions to avoid scaling in LaTeX. This function
    is extracted from https://jwalton.info/Embed-Publication-Matplotlib-Latex/

    Parameters
    ----------
    width: float or string
            Document width in points, or string of predined document type
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy
    subplots: array-like, optional
            The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    '''
    # for general use
    if width == "thesis":
        width_pt = 426.79135
    elif width == "beamer":
        width_pt = 307.28987
    else:
        width_pt = width

    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**0.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

    return (fig_width_in, fig_height_in)
    """
