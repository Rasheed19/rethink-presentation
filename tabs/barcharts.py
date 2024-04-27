from utils.helper_functions import get_image_code_ui


def page() -> None:

    FILES = [
        "pulse_project_eol_transfromation_comparison.jpg",
        "pulse_project_shap_feature_importance.jpg",
        "tl-feature-importance.jpg",
    ]
    CODES = [
        r"""
def plot_target_transform_comparison(
    data: np.ndarray,
    bins: int,
    x_label: str,
    save_name: str,
    fig_labels: List[str] = None,
) -> None:
    data_transformed = quantile_transform(
        X=data.reshape(-1, 1),
        n_quantiles=data.shape[0],
        output_distribution="normal",
    )

    label_data_dict = dict(
        zip([x_label, f"Transformed {x_label}"], [data, data_transformed])
    )
    fig = plt.figure(figsize=set_size(subplots=(1, 2)))

    if fig_labels is None:
        fig_labels = ["a", "b"]

    for i, key in enumerate(label_data_dict):
        ax = fig.add_subplot(1, 2, i + 1)
        ax.text(
            x=-0.1,
            y=1.2,
            s=r"\bf \Large {}".format(fig_labels[i]),
            transform=ax.transAxes,
            fontweight="bold",
            va="top",
        )
        ax.hist(label_data_dict[key], bins=bins, alpha=0.75, color="red", ec="black")

        ax.set_xlabel(key)

        if i == 0:
            ax.set_ylabel("Count")

        ax.spines[
            [
                "top",
                "right",
            ]
        ].set_visible(False)

    plt.savefig(f"{save_name}.pdf", bbox_inches="tight")
    plt.show()

    return None
""",
        r"""
def plot_feature_importance(
    analysis_result: dict, threshold: int, tag: str, fig_labels: List[str] = None
) -> None:
    fig = plt.figure(figsize=set_size(subplots=(1, 3)))

    if fig_labels is None:
        fig_labels = ["a", "b", "c"]

    for i, value in enumerate(analysis_result.values()):
        ax = fig.add_subplot(1, 3, i + 1)
        ax.text(
            x=-0.1,
            y=1.2,
            s=r"\bf \Large {}".format(fig_labels[i]),
            transform=ax.transAxes,
            fontweight="bold",
            va="top",
        )

        ax.bar(
            value["features"][-threshold:][::-1],
            value["importance"][-threshold:][::-1],
            color="red",
            ec="black",
            alpha=0.75,
        )
        ax.tick_params(axis="x", rotation=90)
        ax.spines[["top", "right"]].set_visible(False)

        if i != 0:
            ax.set_yticklabels([])

        if i == 0:
            ax.set_ylabel("Feature importance")

    plt.savefig(fname=f"pulse_project_{tag}.pdf", bbox_inches="tight")
    plt.show()

    return None
""",
        r"""
import pandas as pd
from sksurv.base import SurvivalAnalysisMixin
from sklearn.inspection import permutation_importance
from sksurv.metrics import concordance_index_censored

def score_survival_model(
    model: SurvivalAnalysisMixin, X: pd.DataFrame, y: np.ndarray
) -> float:
    prediction = model.predict(X)
    result = concordance_index_censored(
        y["cycled_to_eol"], y["end_of_life"], prediction
    )
    return result[0]


def plot_feature_importance(
    model: SurvivalAnalysisMixin,
    X: pd.DataFrame,
    y: np.ndarray,
    model_type: str,
    figure_label: str | None = None,
) -> None:

    result = permutation_importance(
        estimator=model,
        X=X,
        y=y,
        scoring=score_survival_model,
        n_repeats=100,
        random_state=42,
    )

    result_df = pd.DataFrame(
        {
            k: result[k]
            for k in (
                "importances_mean",
                "importances_std",
            )
        },
        index=X.columns,
    ).sort_values(by="importances_mean", ascending=False)

    print(f"Feature importance:\n {result_df}")

    _, ax = plt.subplots(figsize=set_size())

    if figure_label is not None:
        ax.text(
            x=-0.1,
            y=1.0,
            s=r"\bf \Large {}".format(figure_label),
            transform=ax.transAxes,
            fontweight="bold",
            va="top",
        )
    ax.bar(
        result_df.index,
        result_df["importances_mean"].abs(),
        color="blue",
        ec="black",
        alpha=0.75,
    )
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x", rotation=90)
    ax.set_ylabel("Drop in C-index")

    FIGURE_NAME: str = (
        f"{model_type}_feature_importance.pdf"
        if figure_label is None
        else f"{model_type}_feature_importance_{figure_label}.pdf"
    )

    plt.savefig(
        fname=FIGURE_NAME,
        bbox_inches="tight",
    )

    return None
""",
    ]

    for p, c in zip(FILES, CODES):
        get_image_code_ui(path_to_image=f"./assets/{p}", code=c)
