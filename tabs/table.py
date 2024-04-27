from utils.helper_functions import get_image_code_ui


def page() -> None:
    FILES = [
        "cathode-group-cell-number.png",
        "model-description.png",
        "eol-rul-model-performance.png",
        "clf-performance.png",
        "eol-rul-model-time-range-performance.png",
        "leave-one-cathode-out-validation.png",
    ]
    CODES = [
        r"""
\begin{table}[H]
    \centering
        \caption{The breakdown of cathode groups by the number of cells. The `Original' column refers to the actual number (300 in total) of cells in the downloaded data. The `Processed' column corresponds to the number of cells in each group after cells that do not undergo pulse testing (9 cells), those that have reached the EOL before the first pulse test (23 cells), and those with irregular pulse voltage profiles (3 cells) have been removed (details in Section \ref{subsec:data-analysis}).
        } \vspace{-0.3cm}
    \small
    \begin{tabular}{lcc} 
    \hline
   \multirow{2}{*}{Cathode group} & \multicolumn{2}{c}{Number of cells}\\
   \cline{2-3}
   & Original & Processed
    \\
    \hline 
     Li$_{1.2}$Ni$_{0.3}$Mn$_{0.6}$O$_2$ & 6 & 6\\
     Li$_{1.35}$Ni$_{0.33}$Mn$_{0.67}$O$_{2.35}$ & 4 & 2 \\
     FCG (Full concentration gradient NMC) & 8 & 8\\ 
     NMC811 & 15 & 15\\
     NMC622 & 20 & 20\\
     NMC532 & 100 & 89\\
     NMC111 & 16 & 16\\
     HE5050 & 78 & 77\\
     5Vspinel & 53 & 32\\
    \hline
    \multicolumn{1}{r}{\textbf{Total}} & 300 & 265 \\
    \hline
    \end{tabular}
    \normalsize
    \label{tab:cathode-group-cell-number}
\end{table}
""",
        r"""
\begin{table}[H]
    \centering
        \caption{Description of the machine learning models considered in this study. Voltage and Current profiles are denoted by $V$ and $I$ respectively.
        %\gbox{any change }
        } \vspace{-0.3cm}
    \small
    \begin{tabular}{lp{160pt}p{80pt}} 
    \hline
   Model name & \centering{Model input} & What is predicted 
    \\
    \hline \hline
    EOL model & $V$, $I$ profiles of a single set of pulse tests carried out within the first 100 cycles; see Equation~(\ref{eq:eol-feature-matrix}) for the corresponding feature matrix  & EOL\\
    \hline
    RUL model & $V$, $I$ profiles of a single set of  pulse tests carried out \emph{at any cycle $n$ before the EOL}; see Equation~(\ref{eq:rul-br-feature-matrix}) for the corresponding feature matrix & $\text{RUL} = \text{EOL}-n$\\
    \hline
    Classification model & $V$, $I$ profiles of a single set of pulse tests carried out \emph{at any cycle} $n$; see Equation~(\ref{eq:rul-br-feature-matrix}) for the corresponding feature matrix & passed EOL (0); not passed EOL (1)\\
    \hline
    \end{tabular}
    \normalsize
    \label{tab:model-description}
\end{table}
""",
        r"""
\begin{table}[H]
    \centering
    \caption{Performance metrics of the individual models that predict the EOL and RUL. The $95\%$ confidence interval is obtained via bootstrap pivotal confidence intervals.}
    \vspace{-0.3cm}
    \small
    \begin{tabular}{lccccccc}
     \hline
     && \multicolumn{3}{c}{\textbf{MAE (cycles)}} && \multicolumn{2}{c}{\textbf{RMSE (cycles)}}\\
      \cline{3-4} \cline{6-7}
     && Value & CI && Value & CI\\
     \hline
     \multirow{2}{*}{EOL} & Train & 1.98 & [1.49, 2.43] && 3.82 & [2.83, 4.86]\\
     & Test & 85.16 & [57.31, 108.89] && 147.98 & [97.14, 202.36]\\ 
     \hline
     \multirow{2}{*}{RUL} & Train & 6.69 & [6.25, 7.12] && 10.80 & [10.00, 11.58]\\
    & Test & 91.47 & [83.69, 98.87] && 133.75 & [121.28, 146.13]\\
     \hline
    \end{tabular}
    \normalsize
    \label{tab:eol-rul-model-performance}
\end{table}
""",
        r"""
\begin{table}[H]
    \centering
    \caption{Performance metrics of the classification model that predicts whether a cell has passed its EOL or not based on pulse testing data. The 95\% confidence interval (CI) was calculated using the concept of bootstrap pivotal CI.}
    \vspace{-0.3cm}
\scriptsize
\begin{tabular}{lccccccc}
     \hline
     & \multicolumn{2}{c}{\textbf{Train}} && \multicolumn{2}{c}{\textbf{Test}}\\
      \cline{2-3} \cline{5-6}
     & Value (\%) & CI && Value (\%) & CI\\
      \hline
     Precision & 100 & [100, 100] &&  92.94 &  [91.01, 95.03]\\ 
     Recall & 100 & [100, 100]  && 93.08 & [91.19, 95.12]\\
     $F_1$-score & 100 & [100, 100] && 93.01 & [91.63, 94.5]\\
     AUC ROC & 100 & [100, 100] && 98.36 & [97.85, 98.93]\\
     Accuracy & 100 & [100, 100] && 94.44 & [93.37, 95.63]\\
     \hline
     \end{tabular}
    \normalsize
    \label{tab:clf-performance}
\end{table}
""",
        r"""
\begin{table}[H]
    \centering
    \caption{Cross-validation results from EOL, RUL, and classification models obtained under different time ranges of the HPPC test. The window considered here ensures that there are two complete discharge and charge regimes in each range. This experiment is motivated by using data under different SOCs, which applies to situations where non-fully charged cells are supplied for making predictions.}
    \vspace{-0.3cm}
    \small
    \begin{tabular}{lcccc}
    \hline
     & \multirow{2}{*}{Time range (sec)} & \multirow{2}{*}{SOC range (\%)} & \multicolumn{2}{c}{\textbf{MAE (cycles)}}\\
     \cline{4-5}
     &&& $\bar{x}$ & $\sigma$\\
     \hline
     \multirow{3}{*}{EOL} & 0-40 & 100-80 & 118.75 & 20.88\\
     & 40-80 & 80-60 & 117.09 & 25.87\\
     & 80-120 & 60-40 & 124.72 & 25.15\\
     \hline
     \multirow{3}{*}{RUL} & 0-40  & 100-80 & 75.37 & 6.41\\
     & 40-80 & 80-60 & 79.10 & 3.16\\
     & 80-120 & 60-40 & 72.01 & 1.16\\
     \hline
     &&& \multicolumn{2}{c}{\textbf{$\mathbf{F_1}$-score (\%)}}\\
     \cline{4-5}
     &&& $\bar{x}$ & $\sigma$\\
     \hline
     \multirow{3}{*}{Classification} & 0-40 & 100-80 & 91.25 & 1.37\\
     & 40-80 & 80-60 & 92.34 & 1.32\\
     & 80-120 & 60-40 & 92.68 & 0.73\\
     \hline
    \end{tabular}
    \normalsize
    \label{tab:eol-rul-model-time-range-performance}
\end{table}
""",
        r"""
\begin{table}[H]
    \centering
        \caption{Comparison of the performance of our proposed model in predicting EOL. The model was trained on all but one cathode chemistry and then tested on the left-out cathode group. In places where numbers are marked with a dagger ($\dagger$) and an asterisk ($*$), it means the metric is obtained from the Extratrees and NuSVR of \cite{Paulson2022} respectively. Meaning of symbols: measured voltage at time $t$ ($V$), current ($I$), capacity ($Q$), internal resistance (IR), state of health (SOH), state of charge (SOC), and charge time ($t_c$).
        } \vspace{-0.3cm}
    \small
    \begin{tabular}{lcc} 
    \hline
    \multirow{2}{*}{Cathode group} & \multicolumn{2}{c}{MAE (cycles)}\\
   \cline{2-3}
   & \textbf{This work} & \cite[Table 2a, 2b]{Paulson2022}
    \\
    \hline 
     NMC111 & 175.04 & $507^\dagger$, $287^*$\\
     NMC532 & 297.61 & $221^\dagger$, $152^*$\\
     NMC622 & 199.66 & $156^\dagger$, $117^*$\\
     NMC811 & 129.44 & $98^\dagger$, $104^*$\\
     HE5050 & 249.84 & $181^\dagger$, $276^*$\\
     5Vspinel & 283.80 & $318^\dagger$, $91^*$\\
    \hline
    \hline 
    Data used & $V$, $I$ & $I$, $V$, SOH, $t_c$, SOC, $Q$, IR\\
    Data regime & Single HPPC test & 100-cycle data (regular cycling)\\
    \hline
    \end{tabular}
    \normalsize
    \label{tab:leave-one-cathode-out-validation}
\end{table}
""",
        r"""
\begin{table}[H]
    \centering
    \caption{Comparison of the performance of models on the test set of target data. Comparison is made for each case of using 5Vspinel, HE5050, and NMC532 as target data. Meaning of abbreviations: DP depicts direct prediction which means using source model to make direct prediction on the test set of target data; DM means direct modelling on the target data; and TL means transfer learning model. The best scores are coloured.}
    \vspace{-0.3cm}
    \small
    \begin{tabular}{lcccc}
    \hline
     &  \multirow{2}{*}{\textbf{Model type}} &  \multirow{2}{*}{\textbf{C-index}} &  \multirow{2}{2.5cm}{\textbf{Cumulative dynamic AUC}} &  \multirow{2}{2cm}{\textbf{Integrated brier score}}\\
     \\
     \hline
     \multirow{3}{*}{5Vspinel} & DP & 0.3636 & 0.3221 & 0.4032\\
     & DM & 0.4818 & 0.4538 & 0.2883\\
     & TL & \colorbox{green}{0.5545} & \colorbox{green}{0.5817} & \colorbox{green}{0.2287}\\
     \hline
     \multirow{3}{*}{HE5050} & DP & 0.3875 & 0.3881 & 0.3960 \\
     & DM & 0.7542 & 0.8437  & 0.1326 \\
     & TL & \colorbox{green}{0.8000} & \colorbox{green}{0.9101} & \colorbox{green}{0.1205}\\
     \hline
     \multirow{3}{*}{NMC532} & DP & 0.5582 & 0.5491 & 0.2229\\
     & DM & \colorbox{green}{0.9206} & 0.9789 & 0.0405\\
     & TL & \colorbox{green}{0.9206} & \colorbox{green}{0.9815} & \colorbox{green}{0.0377}\\
     \hline
    \end{tabular}
    \normalsize
    \label{tab:dp-dm-tl-comparison}
\end{table}
""",
    ]

    for p, c in zip(FILES, CODES):
        get_image_code_ui(path_to_image=f"./assets/{p}", code=c, language="latex")
