from utils.helper_functions import get_image_code_ui


def page() -> None:
    FILES = [
        "pulse_project_stripplot_end_of_life.jpg",
        "pulse_project_eol_rul_parity.jpg",
        "pulse_project_count_end_of_life.jpg",
    ]
    CODES = [
        """
def strip_plot_firstpulse_cycle_life(
    structured_data_with_pulse: dict,
    *,
    pulse_cycle: bool,
    ylabel: str,
    fig_label: str = None,
) -> None:
    cathode_groups = [
        " Li1.35Ni0.33Mn0.67O2.35",
        " Li1.2Ni0.3Mn0.6O2",
        "FCG",
        "NMC811",
        "NMC622",
        "NMC532",
        "NMC111",
        "HE5050",
        "5Vspinel",
    ]
    _, ax = plt.subplots(figsize=set_size())

    groups = []
    cycles = []

    for grp in cathode_groups:
        grp_data = {
            k: structured_data_with_pulse[k]
            for k in structured_data_with_pulse
            if structured_data_with_pulse[k]["summary"]["cathode_group"] == grp
        }
        if pulse_cycle:
            x_values = [list(grp_data[cell]["pulses"])[0] for cell in grp_data]
        else:
            x_values = [grp_data[cell]["summary"]["end_of_life"] for cell in grp_data]

        cycles.extend(x_values)
        groups.extend([grp] * len(x_values))

    cycle_group_df = pd.DataFrame()
    cycle_group_df[ylabel] = cycles
    cycle_group_df["Cathode group"] = groups

    # rename the last two cathodes to have a nice look
    mod_cathode_groups = cathode_groups.copy()
    mod_cathode_groups[0] = r"Li$_{1.35}$Ni$_{0.33}$Mn$_{0.67}$O$_{2.35}$"
    mod_cathode_groups[1] = r"Li$_{1.2}$Ni$_{0.3}$Mn$_{0.6}$O$_2$"

    sns.stripplot(
        data=cycle_group_df,
        x=ylabel,
        y="Cathode group",
        alpha=0.5,
        color="blue",
        marker="o",
        ax=ax,
        linewidth=1,
    )

    if fig_label is not None:
        ax.text(
            x=-0.3,
            y=1.1,
            s=r"\bf \Large {}".format(fig_label),
            transform=ax.transAxes,
            fontweight="bold",
            va="top",
        )
    ax.set_yticks(ticks=cathode_groups, labels=mod_cathode_groups)
    ax.spines[
        [
            "top",
            "right",
        ]
    ].set_visible(False)
    # ax.tick_params(axis="x", rotation=90)

    save_tag = "first_pulse" if pulse_cycle else "end_of_life"
    plt.savefig(
        f"{save_tag}.pdf", bbox_inches="tight"
    )

    return None
""",
        """
def axis_to_fig(axis: Any) -> Callable[[tuple], Any]:
    '''
    Converts axis to fig object.

    Args:
    ----
         axis (object): axis object

    Returns:
    -------
            transformed axis oject.
    '''

    fig = axis.figure

    def transform(coord: Union[tuple, list]):
        return fig.transFigure.inverted().transform(axis.transAxes.transform(coord))

    return transform


def add_sub_axes(axis: Any, rect: Union[tuple, list]) -> Any:
    '''
    Adds sub-axis to existing axis object.

    Args:
    ----
         axis (object):        axis object
         rect (list or tuple): list or tuple specifying axis dimension

    Returns:
    -------
           fig object with added axis.
    '''
    fig = axis.figure
    left, bottom, width, height = rect
    trans = axis_to_fig(axis)
    figleft, figbottom = trans((left, bottom))
    figwidth, figheight = trans([width, height]) - trans([0, 0])

    return fig.add_axes([figleft, figbottom, figwidth, figheight])


def parity_plot(prediction_data_list: List[dict], tag: str) -> None:
    fig = plt.figure(figsize=set_size(subplots=(1, 2)))
    fig_labels = ["a", "b"]
    marker_style = dict(
        facecolor="white",  # Interior color
        # edgecolor='black'    # Border color
    )

    for i, prediction_data in enumerate(prediction_data_list):
        ax = fig.add_subplot(1, 2, i + 1)
        ax.text(
            x=-0.1,
            y=1.2,
            s=r"\bf \Large {}".format(fig_labels[i]),
            transform=ax.transAxes,
            fontweight="bold",
            va="top",
        )

        # ax.scatter(
        #     prediction_data["train"]["actual"],
        #     prediction_data["train"]["prediction"],
        #     color="royalblue",
        #     s=20,
        #     #alpha=0.5,
        #     marker='o',
        #     label="Train",
        #     **marker_style
        # )

        ax.scatter(
            prediction_data["test"]["actual"],
            prediction_data["test"]["prediction"],
            color="red",
            s=20,
            # alpha=0.5,
            marker="o",
            label="Test",
            **marker_style,
        )

        lims = [
            np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
            np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        ]

        # now plot both limits against each other
        ax.plot(lims, lims, "k", zorder=100)
        ax.set_xlim(lims)
        ax.set_ylim(lims)

        ax.spines[
            [
                "top",
                "right",
            ]
        ].set_visible(False)

        if i == 0:
            ax.set_ylabel("Predicted values")

        ax.set_xlabel("Measured values")

        # embed histogram of residuals
        subaxis = add_sub_axes(ax, [0.29, 0.85, 0.3, 0.2])
        residuals = []

        for value in prediction_data.values():
            residuals.extend((value["actual"] - value["prediction"]).tolist())

        subaxis.hist(residuals, bins=50, color="black", alpha=0.75, ec="black")
        subaxis.set_xlim(-max(residuals), max(residuals))
        subaxis.set_xlabel("Residuals")
        subaxis.set_ylabel("Count")
        subaxis.spines[
            [
                "top",
                "right",
            ]
        ].set_visible(False)

    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(handles, labels, loc='upper center',
    #           ncol=2, bbox_to_anchor=(-0.2, -0.4))

    plt.savefig(fname=f"{tag}.pdf", bbox_inches="tight")

    return None
""",
        """
def distribution_of_firstpulse_cycle_life(
    structured_data_with_pulse: dict, pulse: bool = False
) -> None:
    cathode_groups = [
        "5Vspinel",
        "HE5050",
        "NMC111",
        "NMC532",
        "NMC622",
        "NMC811",
        "FCG",
        " Li1.2Ni0.3Mn0.6O2",
        " Li1.35Ni0.33Mn0.67O2.35",
    ]
    _, ax = plt.subplots(figsize=set_size())
    markers = ["o", "s", "D", "^", "v", ">", "<", "p", "8"]
    colors = ["b", "g", "r", "c", "m", "y", "k", "purple", "orange"]

    for i, grp in enumerate(cathode_groups, start=1):
        grp_data = {
            k: structured_data_with_pulse[k]
            for k in structured_data_with_pulse
            if structured_data_with_pulse[k]["summary"]["cathode_group"] == grp
        }
        if pulse:
            x_values = [list(grp_data[cell]["pulses"])[0] for cell in grp_data]
        else:
            x_values = [grp_data[cell]["summary"]["end_of_life"] for cell in grp_data]

        ax.scatter(
            x_values,
            [i] * len(x_values),
            marker=markers[i - 1],
            color=colors[i - 1],
            alpha=0.7,
            facecolor="white",
            label=f"{len(x_values)} cells",
        )

    # rename the last two cathodes to have a nice look
    cathode_groups[-2] = r"Li$_{1.2}$Ni$_{0.3}$Mn$_{0.6}$O$_2$"
    cathode_groups[-1] = r"Li$_{1.35}$Ni$_{0.33}$Mn$_{0.67}$O$_{2.35}$"

    ax.set_yticks(ticks=list(range(1, 10)), labels=cathode_groups)
    ax.spines[
        [
            "top",
            "right",
        ]
    ].set_visible(False)

    handles, labels = ax.get_legend_handles_labels()
    # if not pulse:
    ax.legend(handles, labels, loc="upper center", ncol=3, bbox_to_anchor=(0.45, -0.2))
    ax.set_xlabel("First pulse cycles" if pulse else "End of life")

    save_tag = "first_pulse" if pulse else "end_of_life"
    plt.savefig(
        f"{save_tag}.pdf", bbox_inches="tight"
    )

    return None
""",
    ]

    for p, c in zip(FILES, CODES):
        get_image_code_ui(path_to_image=f"./assets/{p}", code=c)
