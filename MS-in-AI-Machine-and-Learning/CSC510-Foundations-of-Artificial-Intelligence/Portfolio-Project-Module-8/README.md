# Portfolio Project - Module 8

Program: CubeSat Telemetry Anomaly-Detection and Diagnostic-Planning Assistant

Date: 09/13/2026   
Grade:

---

Foundations of Artificial Intelligence CSC510   
Professor: Dr. Isaac Gang  
Fall A (26FA) – 2026   
Student: Alexander (Alex) Ricciardi 

---

## Assignment Directions


AI Use - Case Problem With Solution
Your final Portfolio Project will be a fully-functioning AI program built to solve a real-world problem of your choosing, utilizing the tools and techniques outlined in this course. Your program will interact with human beings to support decision-making processes by delivering relevant information about the problem.

Your final project submission should include a self-executable Python program. The program should be complete and straightforward to test. The program should leverage methods learned from at least 2 of the modules from this course. The submission must function and be a reasonable attempt at a solution for your chosen problem. The solution does not have to be correct or useful in the real world, but the solution MUST provide reasonable answers without error.

In addition to your program, your submission should include a 2-4 page essay describing the final version of your AI program, the use-case it intends to solve, and the methods you used toward that goal. In your paper, please address the following details:

The tools, libraries, and APIs utilized,
Search methods used and how they contributed toward the program goal,
Inclusion of any deep learning models,
Aspects of your program that utilize expert system concepts,
How your program represent knowledge,
How symbolic planning is used in your program (remember, symbolic planning is not limited to robot navigation).
 

Grading Criteria:
- Your program should be functional, clear, and demonstrate appropriate use of course concepts.
- Your paper should be 2-4 pages in length, not including the cover page and references page.
- Your paper must be formatted according to APA guidelines in the CSU Global Writing Center (available in the left-hand navigation panel).
- Your claims should be supported by evidence. Include at least 3 credible references in addition to the course textbook. The CSU Global Library (available in the left-hand navigation panel) is a good place to find these references.
- All references must be cited in the text and listed on the references page, according to APA formatting.
- See the rubric below for more details about how you will be graded for this assignment.

---
## Program requirements

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/) [![NumPy 2.5](https://img.shields.io/badge/NumPy-2.5%20compatible-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![scikit-learn 1.9](https://img.shields.io/badge/scikit--learn-1.9%20compatible-F7931E?style=flat&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/) [![Streamlit 1.63](https://img.shields.io/badge/Streamlit-1.63%20compatible-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/) [![pandas 3](https://img.shields.io/badge/pandas-3%20compatible-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/) [![Plotly 7](https://img.shields.io/badge/Plotly-7%20compatible-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/python/)

---

## The program

This program helps a user review unusual satellite telemetry. A telemetry segment is a group of
recorded readings summarized as one row of numerical features. For a selected segment, the program
estimates an anomaly probability, finds similar reviewed cases, applies logic rules, and uses A*
search to suggest an ordered set of simulated diagnostic checks.

The included OPS-SAT Anomaly Detection (OPS-SAT-AD) feature table supports authentic-data analysis
without a separate download. Small simulated examples are also included so a reader can see normal,
anomalous, uncertain, and conflicting-evidence cases. Both interfaces use the same analysis code.
The model is fitted locally when a session starts; no API key or paid service is needed.

Start with [Setup](#setup), then choose either [Run from the command line](#run-from-the-command-line)
or [Run the Streamlit app](#run-the-streamlit-app).

The accompanying written essay is [Portfolio-Project-Module-8-Essay.docx](./Portfolio-Project-Module-8-Essay.docx), which addresses the theoretical concepts, methodology, and APA requirements. An application overview with visual walkthrough screenshots is provided in [app-screenshots.pdf](./app-screenshots.pdf).


App Home Page:     
<img width="588" height="918" alt="image" src="https://github.com/user-attachments/assets/389ed300-e529-423f-ac9b-f4ec23511c5d" />


---

## Setup

Use **Python 3.12**, the version used to verify this copy. Open a terminal in
`Portfolio-Project-Module-8`, or in the repository folder if you cloned this folder as
its own Git repository. All commands below run from the directory containing this README.

Create a virtual environment called `.venv` **inside this folder**. It keeps this program's
libraries separate from other Python projects. The environment itself is not included in the
submission; each reader creates one for their computer.

### macOS or Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
```

If PowerShell prevents activation, use the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

---

## Run from the command line

**The command-line interface (CLI) runs the full analysis without opening Streamlit.** These
commands provide a direct way to review the program for the assignment.

Show the available flags:

```bash
python cubesat_telemetry_ai.py --help
```

Run all four simulated examples without prompts:

```bash
python cubesat_telemetry_ai.py --demo --no-color
```

The output identifies each scenario, then displays its prediction, similar cases, logic-rule
results, and simulated plan. The uncertain and conflicting scenarios explain why a manual review
is needed. These examples demonstrate program behavior; they do not measure benchmark performance.

Run one scenario and display evaluation metrics for the simulated data:

```bash
python cubesat_telemetry_ai.py --demo anomalous --evaluate --no-color
```

Evaluate the included authentic feature table and analyze segment `1`:

```bash
python cubesat_telemetry_ai.py --dataset data/dataset.csv --profile authentic --evaluate --segment 1 --no-color
```

The evaluation reports precision, recall, F1, accuracy, and a confusion matrix on the 529 held-out
segments. Those are the complete evaluation rows, including normal and anomalous examples. They
are separate from the rows used to train the model and select its threshold.

Select one simulated segment directly:

```bash
python cubesat_telemetry_ai.py --dataset data/demo_opssat_fixture.csv --profile fixture --segment demo-046 --no-color
```

### Interactive use

Start an interactive session with the included authentic data:

```bash
python cubesat_telemetry_ai.py --no-color
```

At the prompt, enter an exact segment ID such as `1`, or a one-based row selector such as `#1`.
After the result, enter `y` to analyze another segment using the same fitted model or `n` to stop.
Enter `q` at the segment prompt to quit. Invalid selections produce a message and another prompt.

For an interactive session using only the small simulated dataset:

```bash
python cubesat_telemetry_ai.py --dataset data/demo_opssat_fixture.csv --profile fixture --no-color
```

### CLI flags

| Flag | Purpose |
| --- | --- |
| `--help` | List options and exit without loading data. |
| `--dataset PATH` | Choose a local feature CSV. The default is the included `data/dataset.csv`. |
| `--profile authentic` | Validate the exact OPS-SAT-AD v2 feature file; this is the default. |
| `--profile fixture` | Use the simulated-data validation rules with an explicit dataset path. |
| `--segment ID` | Analyze an exact ID or a row selector such as `--segment '#1'` without prompts. |
| `--evaluate` | Print held-out evaluation metrics. Used alone, it evaluates and exits. |
| `--demo [NAME]` | Run `all`, `normal`, `anomalous`, `uncertain`, or `conflicting`. Omitting the name runs all four. |
| `--seed INTEGER` | Set the split and model seed; the default is `2137`. |
| `--no-color` | Print plain text without terminal color codes. |

`--demo` selects its own dataset, profile, and scenario segment. Use it without `--dataset`,
`--profile`, or `--segment`. `--evaluate`, `--seed`, and `--no-color` can accompany it. Keep the
default seed for the four named examples; changing it can change the fitted model and the
resulting route. For a reproducible comparison on authentic data:

```bash
python cubesat_telemetry_ai.py --evaluate --segment 1 --seed 2137 --no-color
```

A successful non-interactive command returns exit code `0`. Invalid arguments or data return `2`
with an error message. Results are printed in the terminal; the program does not save a report.

---

## Run the Streamlit app

With the same environment activated:

```bash
python -m streamlit run streamlit_app.py
```

Open the local address printed in the terminal, usually `http://localhost:8501`. Leave the terminal
running while using the app. Press `Ctrl+C` there to stop the server.

The app starts with **Authentic OPS-SAT-AD v2**. Use **Data profile** in the sidebar to select
**Deterministic demo fixture** when reviewing the simulated examples.

- **Analyze telemetry** screens the held-out segments. Filter by channel or screening status,
  then select a segment to inspect its probability, feature values, similar cases, rule results,
  and proposed checks. Channel codes identify source telemetry channels, not diagnosed subsystems.
- **Data and AI walkthrough** explains the data, model, evaluation, similarity search, logic rules,
  A* planning, and module structure. Choose a stage to see its inputs and outputs for the current
  data profile and selected example.

The two pages share the selected data profile. Switching to the walkthrough does not require a
second installation or a different command.

---

## How the analysis works

The program uses 18 numerical features per segment. It separates the official training rows into
model-fitting and threshold-validation subsets, while keeping the official test rows for
evaluation and screening.

1. **Classification:** a multilayer perceptron (MLP), with hidden layers of 32, 16, and 8 units,
   estimates anomaly probability. Features are standardized using training data.
2. **Similarity search:** Euclidean distance retrieves up to three reviewed cases from each class
   for comparison with the selected segment.
3. **Logic rules:** numerical conditions and historical evidence become facts. Horn rules derive
   advisory conclusions and record which premises supported them.
4. **Planning:** A* search orders applicable simulated diagnostic checks using action costs and
   their preconditions.

⚠️ The probability threshold is set using validation data. Probabilities within 0.05 above or below this threshold are treated as uncertain. Results that disagree with historical cases may also need manual review. Suggested faults are possible explanations to investigate, and the user decides what to do next.

---

## File map and module responsibilities

Main program, data, documentation, and verification files:

```text
Portfolio-Project-Module-8/
├── README.md                              # Main documentation, setup instructions, and CLI/Streamlit guides
├── Portfolio-Project-Module-8-Essay.docx  # Academic essay accompanying the portfolio project
├── app-screenshots.pdf                    # Visual demonstration and screenshots of the Streamlit application
├── streamlit_app.py                      # Native two-page Streamlit application entry point and router
├── requirements.txt                      # Direct runtime Python dependencies
├── .streamlit/
│   └── config.toml                       # Streamlit server and theme configuration
├── app_pages/
│   ├── analyze_telemetry.py              # Screening, telemetry segment inspection, and recommendation UI
│   └── how_it_works.py                   # Interactive Data and AI pipeline walkthrough UI
├── assets/
│   └── footer.html                       # Shared HTML footer with branding and author profiles
├── cubesat_telemetry_ai.py               # CLI entry point and analysis coordinator
├── cubesat_cli.py                        # Command-line argument parsing and interactive session input
├── cubesat_config.py                     # System configuration, paths, thresholds, and mappings
├── cubesat_data.py                       # Data validation, partitioning, and segment loading
├── cubesat_display.py                    # Terminal display formatting and report rendering
├── cubesat_frontend.py                   # Presentation context, cached data transforms, and UI helpers
├── cubesat_logic.py                      # Rule translation, Horn clause unification, and forward chaining
├── cubesat_model.py                      # Feature standardization, MLP neural network training, and evaluation
├── cubesat_planner.py                    # Diagnostic action catalog and deterministic A* search planner
├── cubesat_similarity.py                 # Class-aware Euclidean nearest-neighbor historical retrieval
├── cubesat_types.py                      # Enums, data classes, and domain type definitions
├── cubesat_verification.py               # Independent mathematical, structural, and behavioral verification script
└── data/
    ├── README.md                         # Data provenance, verification checksums, and schema documentation
    ├── LICENSE-OPS-SAT                   # Publisher's license notice for OPS-SAT-AD data and code
    ├── dataset.csv                       # Authentic OPS-SAT-AD v2 18-feature dataset (Zenodo record 15108715)
    ├── segments.csv                      # Authentic raw segment telemetry data (303,493 rows)
    ├── demo_opssat_fixture.csv           # Deterministic 50-segment simulated fixture for offline use
    └── demo_scenarios.json               # Scenario definitions for normal, anomalous, uncertain, and conflicting cases
```

`cubesat_config.py` and `cubesat_types.py` import no workflow module. Backend modules return structured values and do not prompt or print. `cubesat_cli.py` owns raw input, `cubesat_display.py` owns console presentation, and `cubesat_telemetry_ai.py` coordinates the pipeline without reimplementing backend algorithms. The local import graph is acyclic.

## Included files

| File or folder | Role |
| --- | --- |
| `Portfolio-Project-Module-8-Essay.docx` | Academic essay accompanying the portfolio project, covering the AI use case, methods, and evaluation in APA format. |
| `app-screenshots.pdf` | Visual demonstration document containing comprehensive screenshots of the Streamlit application interfaces and inspection views. |
| `cubesat_telemetry_ai.py` | CLI entry point and analysis coordinator. |
| `cubesat_cli.py`, `cubesat_display.py` | Command-line input handling, argument parsing, and result formatting. |
| `cubesat_config.py`, `cubesat_types.py` | Configuration, paths, threshold constants, and shared domain data types. |
| `cubesat_data.py` | Data validation, partition management, and segment selection. |
| `cubesat_model.py` | Feature standardization, MLP neural network fitting, predictions, and evaluation. |
| `cubesat_similarity.py` | Historical-case comparison using class-aware Euclidean nearest neighbors. |
| `cubesat_logic.py`, `cubesat_planner.py` | Logic rules, forward chaining, and simulated diagnostic A* planning. |
| `cubesat_verification.py` | Independent mathematical, structural, and behavioral verification script checking dataset invariants, model metrics, logic traces, and planning transitions. |
| `streamlit_app.py`, `app_pages/`, `cubesat_frontend.py` | Browser navigation, interactive pages, telemetry charts, and presentation helpers. |
| `assets/footer.html`, `.streamlit/config.toml` | Shared branding footer, app visual styling, and local Streamlit settings. |
| `data/dataset.csv`, `data/segments.csv` | Authentic OPS-SAT-AD v2 feature table (2,123 rows) and raw telemetry readings (303,493 rows) used by both interfaces and the verifier. |
| `data/demo_opssat_fixture.csv`, `data/demo_scenarios.json` | Small simulated examples (50 rows) and named demonstration scenario definitions. |
| `data/README.md`, `data/LICENSE-OPS-SAT` | Data origin, file identity, checksums, preparation instructions, and publisher's license notice. |
| `requirements.txt` | Python runtime dependencies (NumPy, pandas, Plotly, scikit-learn, Streamlit). |

---

## References

- [OPS-SAT-AD v2 dataset and source record](https://zenodo.org/records/15108715)
- [Official OPS-SAT-AD repository](https://github.com/kplabs-pl/OPS-SAT-AD)
- [The OPS-SAT benchmark for detecting anomalies in satellite telemetry](https://doi.org/10.1038/s41597-025-05035-3)
- [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
- [scikit-learn NearestNeighbors](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html)

---

My Links:

<p align="left">
<a href="https://github.com/AngryOwlAI/"><img width="25" height="25" src="https://github.com/user-attachments/assets/ef169f03-2a25-4737-95e8-9b6a85491c9c" alt="AngryOwlAI logo"><img height="30" src="https://img.shields.io/badge/AngryOwlAI-0D1117?style=for-the-badge" alt="AngryOwlAI GitHub organization"></a>
<a href="https://www.alexomegapy.com"><img height="30" src="https://raw.githubusercontent.com/Omegapy/My-Academics-Portfolio/main/assets/branding/code-chronicles-omegapy-shield.gif" alt="Code Chronicles | Omegapy"></a>
<a href="https://medium.com/@alex.omegapy"><img height="30" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
<a href="https://x.com/AlexOmegapy"><img height="30" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.youtube.com/@AngryOwl-AI"><img height="30" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.facebook.com/profile.php?id=100089638857137"><img height="30" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<a href="https://linkedin.com/in/alex-ricciardi"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://www.threads.net/@alexomegapy?hl=en"><img height="30" src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
<a href="https://dev.to/alex_ricciardi"><img height="30" src="https://img.shields.io/badge/DEV.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" alt="DEV.to"></a>
</p>

