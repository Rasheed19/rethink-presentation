from utils.helper_functions import get_image_code_ui


def page() -> None:
    FILES = [
        "pulse_project_v_i_twin_plot.jpg",
        "pulse_project_time_threshold_effect.jpg",
        "pulse_project_sample_filtered_capacity.jpg",
        "batch-survival-analysis-plot.jpg",
    ]
    CODES = [
        """
def plot_full_pulse_profile(
    path_to_sample_cell: str,
    pulse_cycle: int,
    style: str = "cropped",
) -> None:
    if style not in ["cropped", "uncropped"]:
        raise ValueError(
            f"style option must be either 'cropped' or 'uncropped', {style} is provided"
        )

    pulse, _ = structure_noah.load_h5_columns_needed(
        path_to_cell=path_to_sample_cell,
        return_all=False if style == "cropped" else True,
    )

    pulse = pulse[
        pulse["cycle_number"]
        == pulse_cycle  # pulse cycle must be valid to have the desird plot
    ]

    if style == "cropped":
        t, y1, y2 = structure_noah.remove_rest_profile_from_pulse(pulse_data=pulse)

    elif style == "uncropped":
        t, y1, y2 = (
            pulse["test_time"].values,
            pulse["current"].values,
            pulse["voltage"].values,
        )
        t = t - t.min()

    # else:
    #     raise ValueError(
    #         f"style option must be either 'cropped' or 'uncropped', {style} is provided"
    #     )

    _, ax1 = plt.subplots(figsize=set_size())
    ax1.plot(t, y1, "-.", label="Current", color="red")
    ax1.set_ylabel("Current (A)")
    ax1.set_xlabel("Time (s)")
    # ax1.set_yticks(ticks=ax1.get_yticks())

    ax2 = ax1.twinx()
    ax2.plot(t, y2, label="Voltage", color="blue")
    ax2.set_ylabel("Voltage (V)")
    # ax2.set_yticks(ticks=ax2.get_yticks())

    for ax, loc in zip([ax1, ax2], [0.4, 0.75]):
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(
            handles, labels, loc="upper center", ncol=1, bbox_to_anchor=(loc, -0.2)
        )

        ax.spines["top"].set_visible(False)

    plt.savefig(
        f"v_i_twin_plot_{style}.svg",
        bbox_inches="tight",
    )

    plt.show()
""",
        """

def plot_time_threshold_effect(threshold_data_dict: dict) -> None:
    fig = plt.figure(figsize=set_size(fraction=1, subplots=(1, 2)))
    fig_labels = ["a", "b"]

    for i, (key, value) in enumerate(threshold_data_dict.items()):
        ax = fig.add_subplot(1, 2, i + 1)
        ax.text(
            x=-0.15,
            y=1.2,
            s=r"\bf \Large {}".format(fig_labels[i]),
            transform=ax.transAxes,
            fontweight="bold",
            va="top",
        )
        ax.plot(
            value[0],
            value[1] if key in ["rul", "eol"] else np.array(value[1]) * 100.0,
            color="red",
            marker="o",
            label="Mean",
        )
        ax.axvline(x=120, linestyle="--", color="black")
        ax.text(
            x=0.2,
            y=1.1,
            s=r"$t$ = 120 s, 40\% SOC",
            transform=ax.transAxes,
            va="top",
        )
        ax.set_yticks(ticks=ax.get_yticks())  # to have more granulality on the y-axis

        if key in ["rul", "eol"]:
            ax.set_ylabel("MAE (cycles)")

        elif key == "classification":
            ax.set_ylabel(r"$F_1$-score (\%)")

        ax.set_xlabel("Time threshold (s)")
        ax.spines[["top", "right"]].set_visible(False)

    plt.savefig(
        fname="time_threshold_effect.pdf",
        bbox_inches="tight",
    )

    return None
""",
        """
def plot_filtered_capacity(sample_cells: List[str], structured_data: dict) -> None:
    fig = plt.figure(figsize=set_size(subplots=(3, 3)))
    fig_labels = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

    for i, cell in enumerate(sample_cells):
        ax = fig.add_subplot(3, 3, i + 1)
        ax.text(
            x=-0.15,
            y=1.4,
            s=r"\bf \Large {}".format(fig_labels[i]),
            transform=ax.transAxes,
            fontweight="bold",
            va="top",
        )
        ax.plot(
            structured_data[cell]["summary"]["cycle"],
            structured_data[cell]["summary"]["capacity"],
            label="Measured capacity",
        )
        ax.plot(
            structured_data[cell]["summary"]["cycle"],
            structured_data[cell]["summary"]["filtered_capacity"],
            label="Filtered capacity",
            color="red",
        )

        ax.axvline(
            x=structured_data[cell]["summary"]["end_of_life"],
            label="End of life",
            linestyle="--",
            color="black",
        )

        if i in [6, 7, 8]:
            ax.set_xlabel("Cycle")

        if i in [0, 3, 6]:
            ax.set_ylabel("Capacity (Ah)")

        cathode_group = structured_data[cell]["summary"]["cathode_group"]
        if cathode_group == " Li1.2Ni0.3Mn0.6O2":
            cathode_group = r"Li$_{1.2}$Ni$_{0.3}$Mn$_{0.6}$O$_2$"
        elif cathode_group == " Li1.35Ni0.33Mn0.67O2.35":
            cathode_group = r"Li$_{1.35}$Ni$_{0.33}$Mn$_{0.67}$O$_{2.35}$"

        ax.set_title(f"{cathode_group}")
        ax.spines[
            [
                "top",
                "right",
            ]
        ].set_visible(False)

    fig.tight_layout(pad=0.1)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="upper center", ncol=3, bbox_to_anchor=(-0.8, -1.0))

    plt.savefig(
        "sample_filtered_capacity.pdf",
        bbox_inches="tight",
    )
    plt.show()

    return None
""",
        """
def plot_kaplan_meier_surv_prob(
    loaded_data: dict[str, dict], batch_names: list[str]
) -> None:

    from sksurv.nonparametric import kaplan_meier_estimator

    _, ax = plt.subplots(figsize=set_size())
    marker_types = [
        "o",
        "x",
        "+",
        "*",
        "s",
        "d",
        "^",
        "v",
        "<",
        ">",
        "p",
        "h",
        "D",
        "|",
        "4",
        "8",
        "P",
    ]
    for batch_name, marker in zip(batch_names, marker_types):

        y = loaded_data[batch_name]["y"]

        time, surv_prob = kaplan_meier_estimator(
            event=y["cycled_to_eol"], time_exit=y["end_of_life"], conf_type=None
        )

        ax.step(
            time,
            surv_prob,
            where="post",
            label=batch_name,
            linewidth=1,
            marker=marker,
            markersize=2.5,
        )

    ax.set_ylabel(r"Kaplan-Meier survival probability estimate, $\hat{S}(t)$")
    ax.set_xlabel(r"Cycle, $t$")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="upper center", ncol=4, bbox_to_anchor=(0.5, -0.2))
    ax.spines[
        [
            "top",
            "right",
        ]
    ].set_visible(False)

    plt.savefig(
        f"surv_proj_km_surv_prob.pdf",
        bbox_inches="tight",
    )

    return None
""",
    ]

    for p, c in zip(FILES, CODES):
        get_image_code_ui(path_to_image=f"./assets/{p}", code=c)
