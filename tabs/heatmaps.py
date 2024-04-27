from utils.helper_functions import get_image_code_ui


def page() -> None:
    FILES = [
        "pulse_project_combined_similarity_scores.jpg",
        "pulse_project_roc_confusion_matrix.jpg",
    ]
    CODES = [
        r"""
def jaccard_similarity(list1: list, list2: list) -> float:
    set1 = set(list1)
    set2 = set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    return intersection / union

def plot_feature_similarity(data: dict, tag: str, fig_label: str = None) -> None:
    if figure_label is None:
       figure_label = ["g", "h", "i"]

    similarity_scores = []

    for t1 in data.keys():
        temp_sim_score = []
        for t2 in data.keys():
            temp_sim_score.append(
                jaccard_similarity(data[t1].tolist(), data[t2].tolist())
            )

        similarity_scores.append(temp_sim_score)

    similarity_scores = np.array(similarity_scores)

    _, ax = plt.subplots(figsize=set_size(fraction=0.5, subplots=(1, 1)))
    axis_labels = [int(i) for i in data.keys()]
    # ax.set_xticklabels(axis_labels)
    # ax.set_yticklabels(axis_labels)

    # similarity matix is symmetric, only show the lower triangular part
    mask = np.tril(np.ones_like(similarity_scores, dtype=bool))

    sns.heatmap(
        similarity_scores,
        vmin=0,
        vmax=1,
        xticklabels=axis_labels,
        yticklabels=axis_labels,
        linewidth=0.5,
        # linecolor='black',
        ax=ax,
        cbar_kws={"label": "Jaccard similarity"},
        annot=False,
        mask=~mask,
        # fmt=".2f",
        cmap=plt.cm.Reds,
    )

    ax.text(
        x=-0.1,
        y=1.1,
        s=r"\bf \Large {}".format(fig_label),
        transform=ax.transAxes,
        fontweight="bold",
        va="top",
    )

    ax.set_xlabel("Time threshold (s)")
    ax.set_ylabel("Time threshold (s)")

    plt.yticks(rotation=0)
    plt.savefig(
        fname="similarity_scores.pdf",
        bbox_inches="tight",
    )
""",
        r"""
def plot_cunfusion_matrix_roc_curve(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: np.ndarray,
    classes: List[str],
    cmap: Any = plt.cm.Reds,
) -> None:
    fig = plt.figure(figsize=set_size(subplots=(1, 2)))
    fig_labels = ["a", "b"]

    for i, fig_label in enumerate(fig_labels):
        ax = fig.add_subplot(1, 2, i + 1)
        ax.text(
            x=-0.1,
            y=1.2,
            s=r"\bf \Large {}".format(fig_label),
            transform=ax.transAxes,
            fontweight="bold",
            va="top",
        )

        # for the confusion matrix
        if i == 0:
            cm = confusion_matrix(y_true, y_pred)
            cm_percent = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

            ax.imshow(cm_percent, interpolation="nearest", cmap=cmap)
            tick_marks = np.arange(len(classes))

            ax.set_xticks(
                ticks=tick_marks,
                labels=classes,
                rotation=45,
                ha="right",
                rotation_mode="anchor",
            )
            ax.set_yticks(
                ticks=tick_marks,
                labels=classes,
                rotation=45,
                ha="right",
                rotation_mode="anchor",
            )

            fmt = ".2f"
            thresh = cm_percent.max() / 2.0
            for i, j in itertools.product(
                range(cm_percent.shape[0]), range(cm_percent.shape[1])
            ):
                ax.text(
                    j,
                    i,
                    f"{format(cm_percent[i, j] * 100., fmt)}\%",
                    horizontalalignment="center",
                    color="white" if cm_percent[i, j] > thresh else "black",
                )

            ax.set_ylabel("True label")
            ax.set_xlabel("Predicted label")

        # for the roc curve
        else:
            fpr, tpr, _ = roc_curve(y_true, y_score)
            ax.plot(fpr, tpr, "r-", label="XGBoost")
            ax.plot([0, 1], [0, 1], "k--", label="Chance level")
            ax.set_xlabel("False positive rate")
            ax.set_ylabel("True positive rate")
            ax.spines[["top", "right"]].set_visible(False)

            ax.legend()

    plt.savefig(
        "roc_confusion_matrix.pdf", bbox_inches="tight"
    )
    plt.show()

    return None
""",
    ]

    for p, c in zip(FILES, CODES):
        get_image_code_ui(path_to_image=f"./assets/{p}", code=c)
