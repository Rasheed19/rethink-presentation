import streamlit as st
from tabs import heatmaps, barcharts, scatter, line, table

st.set_page_config(page_title="Rethink presentation", page_icon=":page_facing_up")
st.title("📄 Rethink presentation")

st.expander("💡 About this app. Please read!").info(
    """ 
    Hi there!

    I'm Rasheed. With **Rethink presentation**, 
    I aim to help researchers to produce 
    figures and tables that _blend_ with your
    texts in any LaTeX editor. By blending with
    your texts, I mean you don't need to resize
    figures when preparing your write up as this 
    usually reduces the quality of the figures. In 
    addition, you use the same font and fontsize (as
    in your document) right from creating the figures
    as well as styling them beautifully.
    Figures and tables are produced with Python and Latex 
    respectively which are parts of the results 
    from my PhD study. 

    The codes need not to be followed to
    letters but focus on the parts that create
    and style the entire plots and tables. That is the main
    thing!

    I hope you will be able to use these templates
    and codes as *starting point* to produce 
    amazing and publication-standard results!
    """
)

TABS = st.tabs(
    tabs=[
        "HEATMAPS",
        "BAR CHARTS & HISTOGRAMS",
        "SCATTER PLOTS",
        "LINE PLOTS",
        "MULTI-COLUMN AND MULTI-ROW TABLES",
    ]
)

PAGES = [heatmaps, barcharts, scatter, line, table]

for t, p in zip(TABS, PAGES):
    with t:
        p.page()

st.container(border=True).html(
    """ 
    <h3> Connect with me <img src='https://raw.githubusercontent.com/ShahriarShafin/ShahriarShafin/main/Assets/handshake.gif' width="100px"> </h3>
    <i> Can't find what you are looking for?
    Contact me via the following means and I can 
    help with your preferences or general
    queries! Also, check this app regularly
    to see the latest updates as I am still
    adding more resources.</i>

    <p>
    <a href = 'https://www.linkedin.com/in/rasheed-oyewole-ibraheem-768955246/'> <img width = '32px' align= 'center' src="https://raw.githubusercontent.com/rahulbanerjee26/githubAboutMeGenerator/main/icons/linked-in-alt.svg"/></a>
    <a href = 'https://github.com/Rasheed19/Rasheed19'> <img width = '32px' align= 'center' src="https://raw.githubusercontent.com/rahulbanerjee26/githubAboutMeGenerator/main/icons/github.svg"/></a>
    <a href = 'https://scholar.google.com/citations?user=D6cwjFMAAAAJ&hl=en'> <img width = '32px' align= 'center' src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Google_Scholar_logo.svg"/></a>
    </p>
    """
)
