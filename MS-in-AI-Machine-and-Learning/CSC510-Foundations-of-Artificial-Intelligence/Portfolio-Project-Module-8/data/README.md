# OPS-SAT-AD data preparation

Authentic-data mode uses OPS-SAT-AD version 2 from [Zenodo record
15108715](https://zenodo.org/records/15108715). The record metadata reports `CC-BY-4.0`. The
record's bundled `LICENSE` file separately contains an MIT notice for the OPS-SAT software, data,
and documentation. These are recorded as two observed notices; this project does not reinterpret
their legal effect. A copy of the publisher's bundled notice is included as
[LICENSE-OPS-SAT](./LICENSE-OPS-SAT).

The authentic CSV files are intentionally excluded from Git. From the Module 8 project directory,
prepare them with:

```bash
curl -fL https://zenodo.org/api/records/15108715/files/dataset.csv/content \
  -o data/dataset.csv
curl -fL https://zenodo.org/api/records/15108715/files/segments.csv/content \
  -o data/segments.csv
```

Verify the downloaded artifacts before use:

| File | Published MD5 | Reviewed SHA-256 | Size |
| --- | --- | --- | ---: |
| `dataset.csv` | `5246fdc5e4630a4cecbf7fb6bc8b795e` | `b524177da6f516d5c9f63c7acbc385341f0ad42046ef20c1bed2d25e51b98f02` | 507,550 bytes |
| `segments.csv` | `72f109630abb933a386106897a631188` | `d5201e9e751eb2a53a0ff7c11567dc4239f594ea4b479b2aa66fe67ddcbcb9ba` | 18,987,091 bytes |

```bash
md5 data/dataset.csv data/segments.csv
shasum -a 256 data/dataset.csv data/segments.csv
```

Authentic mode enforces these exact sizes, MD5 values, and SHA-256 values before parsing. The
standalone verifier also scans `segments.csv`, requires 303,493 finite raw rows, and cross-checks
each segment's channel, sampling, numeric anomaly indicator, and benchmark split against
`dataset.csv`. It also verifies the raw file's observed `label` field value (`anomaly`). A changed,
truncated, stale, or mixed-version file fails closed with a controlled error.

The program trains from `dataset.csv`. Its verified v2 profile is:

- 2,123 unique segment rows;
- 18 finite numerical feature columns;
- 1,594 official training rows and 529 held-out test rows;
- 1,689 normal and 434 anomalous rows;
- nine channels: `CADC0872`, `CADC0873`, `CADC0874`, `CADC0884`, `CADC0886`, `CADC0888`,
  `CADC0890`, `CADC0892`, and `CADC0894`.

`demo_opssat_fixture.csv` is a small, deterministic, simulated fixture with the same columns. It is
not the OPS-SAT benchmark and must not be used to claim benchmark performance. Its purpose is to
exercise the complete offline workflow and controlled error paths. `demo_scenarios.json` maps the
named demonstration routes to fixture records; it does not contain executable code.

The Streamlit and command-line interfaces load only local dataset paths selected by their documented
controls or arguments. They do not download, replace, modify, or upload dataset files at runtime.
Prepare authentic inputs with the commands above, then choose **Authentic OPS-SAT-AD v2** in the
Streamlit **Data profile** control or use `--dataset data/dataset.csv --profile authentic` at the
CLI. Choose **Deterministic demo fixture** in Streamlit or use
`--dataset data/demo_opssat_fixture.csv --profile fixture` for simulated offline evidence.

The Streamlit **Data and AI walkthrough** repeats the official record and file links as explicit
learner guidance and shows the same copyable commands. Link controls do not fetch either file during
page rendering. For the authentic profile, the walkthrough derives the deterministic row roles from
the validated local state: 1,275 rows fit the model, 319 rows select the threshold, and 529 rows stay
held out. The two training subsets reconcile to the 1,594 official training-role rows.

The Streamlit screening population is always the selected profile's official held-out rows: 529
segments for the authentic artifact and 10 for the bundled fixture. Its table does not expose the
held-out reviewed labels as predictions. Reviewed labels appear only as historical similarity
provenance and after prediction in the separate evaluation context.

The bundled fixture is labeled `simulated deterministic fixture`. Any other compatible input that
uses fixture-profile validation remains user-provided, simulated, non-operational evidence.
Validation profile is not provenance, and no selected input becomes authentic unless it matches
the pinned artifact identity and authentic profile.

The user-supplied Module 5 milestone under `Milestone-Portfolio-Documents/` was inspected read-only
as provenance for the 18-feature MLP, validation threshold, uncertainty, class-aware metrics, route
behavior, and human decision boundary. The implementation does not modify it.
