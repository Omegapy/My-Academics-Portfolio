#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Module Type: executable script
# -----------------------------------------------------------------------------
# Project: CubeSat Telemetry AI Portfolio Program
# Author: Alexander S. Ricciardi
# Date: 09/13/2026
# -----------------------------------------------------------------------------
# Course: Foundations of Artificial Intelligence CSC510
# Professor: Dr. Isaac Gang
# Term: Fall A (26FA) - 2026
# Assignment: AI Use-Case Problem With Solution - Portfolio Project
# -----------------------------------------------------------------------------
# Project Description:
# Analyze OPS-SAT telemetry with classification, similarity, symbolic reasoning,
# and simulated diagnostic planning while preserving human decision authority.
# ------------------------------------------------------------------------------
# Assignment:
# Your final Portfolio Project will be a fully-functioning AI program built to solve
# a real-world problem of your choosing, utilizing the tools and techniques outlined
# in this course. Your program will interact with human beings to support decision-making
# processes by delivering relevant information about the problem.
#
# Your final project submission should include a self-executable Python program. The
# program should be complete and straightforward to test. The program should leverage
# methods learned from at least 2 of the modules from this course. The submission
# must function and be a reasonable attempt at a solution for your chosen problem.
# The solution does not have to be correct or useful in the real world, but the
# solution MUST provide reasonable answers without error.
#
# In addition to your program, your submission should include a 2-4 page essay
# describing the final version of your AI program, the use-case it intends to
# solve, and the methods you used toward that goal. In your paper, please address
# the following details:
# - The tools, libraries, and APIs utilized,
# - Search methods used and how they contributed toward the program goal,
# - Inclusion of any deep learning models,
# - Aspects of your program that utilize expert system concepts,
# - How your program represent knowledge,
# - How symbolic planning is used in your program (remember, symbolic planning
# is not limited to robot navigation).
# -----------------------------------------------------------------------------
# Module Purpose:
# - Configure the application and share the data-profile choice across its pages.
# - Route navigation to the screening page or the Data and AI walkthrough.
#
# Usage / Integration:
# - From this directory, run ../.venv/bin/python -m streamlit run streamlit_app.py.
# - Streamlit reruns this entry point before executing the selected app_pages script.
#
# Contents Overview:
# - initialize_session_state(): Set the initial data-profile choice.
# - Shared source selector, page definitions, navigation, selected-page execution, and footer.
#
# Dependencies:
# - Standard Library: pathlib, xml.etree.ElementTree
# - Third-Party: streamlit
# - Local Project: cubesat_frontend
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Route the two-page local CubeSat telemetry Streamlit application.

Streamlit runs this script again after an interaction. The shared profile selector is
created before the selected page, so both pages read the same choice from session state.
That state holds presentation choices; cubesat_frontend owns the separate resource cache
that reuses fitted assistants.

The entry point defines navigation and runs one selected page. Each page then loads the
current profile and assembles its own screening view or teaching example.
"""

# __________________________________________
# IMPORTS
# ==========================================

from pathlib import Path # Locate the bundled footer beside this script.
from xml.etree import ElementTree # Preserve the footer links when rendering each badge.

# pyrefly: ignore [missing-import]
import streamlit as st # Shared controls and selected-page execution.

# Use the same profile labels as the pages and fitted-resource adapter.
from cubesat_frontend import AUTHENTIC_PROFILE_LABEL, PROFILE_OPTIONS

# __________________________________________
# PAGE CONFIGURATION AND SHARED STATE
# ==========================================

# Apply shared browser and layout settings before creating page elements.
st.set_page_config(
    page_title="CubeSat telemetry analysis",
    layout="wide",
    initial_sidebar_state="auto",
)


# --- initialize_session_state()
def initialize_session_state() -> None:
    """Set the initial source choice without replacing an existing session value.

    Streamlit reruns the entry script as users interact. setdefault supplies authentic
    mode for a new session and preserves a prior selection on later runs. Fitted model
    objects are kept separately in cubesat_frontend's resource cache.
    """
    st.session_state.setdefault("data_profile", AUTHENTIC_PROFILE_LABEL)


# ---


# __________________________________________
# SHARED PROFILE CONTROLS
# ==========================================
# Initialize presentation state before either page resolves its source.
# The selector updates the profile choice used by the frontend resource cache.

initialize_session_state()

# The shared selector runs before either page reads data_profile from session state.

# Both pages use this sidebar choice to resolve their local data source.
with st.sidebar:
    # Group the shared source control separately from page-specific filters.
    st.subheader("Analysis source", anchor=False)
    # Preserve the selected profile across page visits and reruns.
    st.selectbox(
        "Data profile",
        PROFILE_OPTIONS,
        key="data_profile", # Both pages read this key.
        help=(
            "Authentic mode checks the expected local OPS-SAT-AD v2 data file. "
            "The demo fixture is a fixed set of simulated examples included with the app."
        ),
        # Streamlit binds the keyed profile value to the URL across page navigation.
        bind="query-params",
        persist_state="session",
    )
    st.caption("Review recorded data on this computer. The app does not upload or download data.")


# __________________________________________
# PAGE DEFINITIONS AND NAVIGATION
# ==========================================
# Register the two scripts, then let navigation choose which one executes this rerun.

# The page records describe navigation. Their scripts execute when the selected page runs.
# Open screening when no other page route is selected.
analyze_page = st.Page(
    "app_pages/analyze_telemetry.py",
    title="Analyze telemetry",
    default=True,
)

# Register the teaching page alongside the default analysis page.
methods_page = st.Page(
    "app_pages/how_it_works.py", # Script executed for this page.
    title="Data and AI walkthrough", # Visible navigation label.
    url_path="data-and-ai-walkthrough", # Walkthrough route.
)

# Resolve the current route; analysis is the default for the app root.
selected_page = st.navigation(
    [analyze_page, methods_page], # The two registered page choices.
    position="top", # Shared navigation above page content.
)


# __________________________________________
# CONTENT RESERVATION AND SHARED FOOTER
# ==========================================
# Create the footer before running a page that may stop early on a controlled error.
# The reserved content slot keeps that page visually above the footer.

# Reserve content above the shared footer so a page's st.stop() cannot hide the badges.

# Later page output is inserted into this reserved position.
page_content = st.container()

# Read the shared badge groups from the bundled footer asset.
footer = ElementTree.parse(Path(__file__).parent / "assets" / "footer.html").getroot()
st.space("small")
# Give both pages the same footer, including controlled early-stop states.
with st.container(key="profile_footer", gap="small"):
    # Keep each linked badge intact while native containers handle spacing and wrapping.
    for group in footer.findall("nav"): # Keep the asset group order.
        with st.container(
            horizontal=True,
            wrap=True,
            horizontal_alignment="center",
            vertical_alignment="center",
            gap="small",
        ):
            # Render each link within its original badge group.
            for link in group.findall("a"):
                # Retain the supplied destination, image, and alternative text.
                st.html(ElementTree.tostring(link, encoding="unicode"), width="content")


# __________________________________________
# SELECTED-PAGE EXECUTION
# ==========================================
# Run the chosen direct page script inside the earlier content slot.

# DISPATCH: Execute the page returned by navigation with the shared source already available.
with page_content:
    selected_page.run()


# __________________________________________
# END OF FILE
# ==========================================
