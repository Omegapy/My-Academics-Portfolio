# Portfolio Project Module 8: Big Data and Parallel Processing

Date: 07/05/2026  
Grade: 100% | A

---

Course: CSC507 - Foundations of Operating Systems  
Professor: Dr. Joseph Issa  
Term: Spring C 2026  
Student: Alexander (Alex) Ricciardi

---

## Program Requirements

- Ubuntu Desktop 24.04.1 LTS for the real billion-line benchmark.
- Bash.
- Python 3.12-compatible code.
- Existing `file1.txt` and `file2.txt` seed files.
- `hugefile1.txt` and `hugefile2.txt`, built from the Module 8
  `file1.txt` and `file2.txt` files.

---

## Assignement 

**Option #2: Working with Big Data using Parallel Processing**

The goal of this project is to use the concepts taught in this course to develop an efficient way of working with Big Data.

You should have 2 files in your Linux system: hugefile1.txt and hugefile2.txt, with one billion lines in each one. If you do not, please go back to the Module 7 Portfolio Reminder and complete the steps there.

Create a program, using a programming language of your choice, to produce a new file: totalfile.txt, by taking the numbers from each line of the two files and adding them. So, each line in file #3 is the sum of the corresponding line in hugefile1.txt and hugefile2.txt.

For example, if the first 5 lines of your files look as follows:

$ head -5 hugefile*txt

==> hugefile1.txt <==

4131

29929

6483

7659

25003

==> hugefile1.txt <==

8866

19171

11029

4889

27069

then the first 5 lines of totalfile.txt look like this:

$ head -5 totalfile.txt

12997

49100

17512

12548

52072

Because the files of such large sizes cannot be read into memory in their entirety at the same time, you need to use concurrency. Reading the files one line at a time will take a long time, so use what you have learned in this course to optimize this process. Be sure to record the amount of time it takes for each version of your program to complete this task.

Create two programs, where one program reads the first half of the files, and another program reads the second half. Use the OS to launch both programs simultaneously.

Now, break up hugefile1.txt and hugefile2.txt into 10 files each, and run your process on all 10 sets in parallel. How do the run times compare to the original process?

Explain your methods and results in detail. What conclusions can you make about the different methods of optimizing large file processing? How has the information that you learned in this course helped you to accomplish this task?

Your paper should be 2-3 pages OR MORE in length and conform to CSU Global Writing Center. Include at least 3 references in addition to the course textbook. The CSU Global Library is a good place to find these references. You can access the Writing Center and Library by clicking on the links in the course navigation panel.

---

## Project File Map

| File or Folder                                                                 | Purpose                                                                                                                              |
|--------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `README.md`                                                                    | Project map and Ubuntu run instructions.                                                                                             |
| `file1.txt`                                                                    | Module-local one-million-line seed input. NOT shared in assignment due to file size.                                                 |
| `file2.txt`                                                                    | Module-local second one-million-line seed input. NOT shared in assignment due to file size.                                          |
| `hugefile1.txt`                                                                | Outputted/generated billion-line runtime input built from `file1.txt`. NOT shared in assignment due to file size.                    |
| `hugefile2.txt`                                                                | Outputted/generated billion-line runtime input built from `file2.txt`. NOT shared in assignment due to file size.                    |
| `totalfile.txt`                                                                | Outputted/generated summed result file produced from `hugefile1.txt` and `hugefile2.txt`. NOT shared in assignment due to file size. |
| `verify_inputs.sh`                                                             | Captures environment details and verifies required files.                                                                            |
| `build_hugefiles.sh`                                                           | Recovery helper that verifies by default and only builds with `--build`.                                                             |
| `bigdata_sum.py`                                                               | Shared streaming summation core used by all methods.                                                                                 |
| `sum_first_half.py`                                                            | Thin worker for the first half of split inputs.                                                                                      |
| `sum_second_half.py`                                                           | Thin worker for the second half of split inputs.                                                                                     |
| `sum_chunk.py`                                                                 | Thin worker for one numbered ten-way chunk.                                                                                          |
| `run_baseline.sh`                                                              | Runs the single-process baseline and appends benchmark CSV evidence.                                                                 |
| `run_half_parallel.sh`                                                         | Splits into two halves, launches both workers, and concatenates output.                                                              |
| `split_hugefiles.sh`                                                           | Splits both huge files into ten line-preserving chunks.                                                                              |
| `run_ten_parallel.sh`                                                          | Launches ten chunk workers and concatenates chunk outputs.                                                                           |
| `run_all_benchmarks.sh`                                                        | Runs the full benchmark and validation sequence.                                                                                     |
| `validate_outputs.py`                                                          | Performs fast or full output validation.                                                                                             |
| `benchmark_results.csv`                                                        | Ubuntu benchmark evidence; contains timing rows.                                                                                     |
| `benchmark_results.csv`                                                        | Ubuntu benchmark evidence; contains timing rows.                                                                                     |
| `validation_results.csv`                                                       | Ubuntu validation evidence; contains correctness rows.                                                                               |
| `system_info.txt`                                                              | Ubuntu environment evidence; records OS, CPU, memory, disk, and file evidence.                                                       |
| `verification_report.txt`                                                      | Verification and validation report.                                                                                                  |
| `terminal_outputs.txt`                                                         | Captured Ubuntu terminal output from the build and benchmark run.                                                                    |
| `Portfolio Project - Option 2 Working with Big Data using Parallel Processing.docx` | Final paper written from the Module 8-local benchmark evidence.                                                                      |
| `generated/logs/`                                                              | Terminal logs from benchmark scripts.  NOT shared in assignment due to file size.                                                    |
| `generated/half/`                                                              | Half-file split inputs and outputs.  NOT shared in assignment due to file size.                                                      |
| `generated/chunks/`                                                            | Ten-way split inputs and outputs.  NOT shared in assignment due to file size.                                                        |

---

## Ubuntu Command 

Run these commands from the Module 8 project directory:

```bash
cd ~/path/to/Portfolio-Project-Module-8
chmod +x *.sh
./build_hugefiles.sh --build
./verify_inputs.sh
./run_baseline.sh
./run_half_parallel.sh
./split_hugefiles.sh
./run_ten_parallel.sh
python3 validate_outputs.py --mode fast
```

The full-run alternative is:

```bash
cd ~/path/to/Portfolio-Project-Module-8
chmod +x *.sh
./build_hugefiles.sh --build
./run_all_benchmarks.sh
```

If `hugefile1.txt` and `hugefile2.txt` already exist in this Module 8 folder,
run `./build_hugefiles.sh` instead of `./build_hugefiles.sh --build` to verify
them without rebuilding.

By default, `run_all_benchmarks.sh` performs fast validation after each method
and full validation after the final ten-way output. If the full scan is too
expensive for the Ubuntu machine, use:

```bash
RUN_FULL_VALIDATION=false ./run_all_benchmarks.sh
```

---

## Huge-File Builder

The assignment requires creating `hugefile1.txt` and `hugefile2.txt` from the
Module 8-local `file1.txt` and `file2.txt`. The builder follows that pattern by
appending each seed file 1000 times:

```bash
./build_hugefiles.sh --build
wc -l hugefile*txt
```

To verify existing huge files without rebuilding:

```bash
./build_hugefiles.sh
```

If old huge files must be replaced:

```bash
./build_hugefiles.sh --build --force
```

Build time should be recorded as setup evidence only. It should not be treated
as one of the three Module 8 processing-method runtimes.

The helper builds only from `CTAs/Portfolio-Project-Module-8/file1.txt` and
`CTAs/Portfolio-Project-Module-8/file2.txt`, and writes only to
`CTAs/Portfolio-Project-Module-8/hugefile1.txt` and
`CTAs/Portfolio-Project-Module-8/hugefile2.txt`.

---

## Evidence to Keep for the Paper

After the Ubuntu run completes, keep these files or terminal outputs:

- `benchmark_results.csv`
- `validation_results.csv`
- `system_info.txt`
- `verification_report.txt`
- `generated/logs/full_run.log`
- `wc -l hugefile1.txt hugefile2.txt totalfile.txt`
- `head -5 hugefile1.txt hugefile2.txt totalfile.txt`
- `tail -5 hugefile1.txt hugefile2.txt totalfile.txt`

The retained Ubuntu benchmark files now provide the speedup and correctness
evidence used in `paper.md`.

The final paper phase uses only evidence files and course/reference materials
located inside this Module 8 directory. The generated multi-gigabyte runtime
files are intentionally not required in the macOS workspace because the retained
CSV, report, and terminal-output evidence records the Ubuntu run.

---

## Cleanup

Use these commands only after collecting the needed evidence:

```bash
rm -f totalfile.txt
rm -rf generated/half generated/chunks generated/outputs generated/tmp
```

To remove logs and CSV evidence as well:

```bash
rm -f benchmark_results.csv validation_results.csv system_info.txt verification_report.txt
rm -rf generated/logs
```

Do not commit `hugefile1.txt`, `hugefile2.txt`, `totalfile.txt`, or generated
split chunks. They are intentionally excluded by `.gitignore`, as they exceed file size limits set by GitHub.

---

My Links:

<p align="left">
<a href="https://github.com/AngryOwlAI/"><img width="25" height="25" src="https://github.com/user-attachments/assets/ef169f03-2a25-4737-95e8-9b6a85491c9c" alt="AngryOwlAI logo"><img height="30" src="https://img.shields.io/badge/AngryOwlAI-0D1117?style=for-the-badge" alt="AngryOwlAI GitHub organization"></a>
<a href="https://www.alexomegapy.com"><img width="27" height="27" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53" alt="Code Chronicles logo"></a><a href="https://www.alexomegapy.com"><img height="30" src="https://img.shields.io/badge/Code%20Chronicles%20%7C%20Omegapy-0D1117?style=for-the-badge" alt="Code Chronicles | Omegapy"></a>
<a href="https://medium.com/@alex.omegapy"><img height="30" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
<a href="https://x.com/AlexOmegapy"><img height="30" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.youtube.com/@AngryOwl-AI"><img height="30" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.facebook.com/profile.php?id=100089638857137"><img height="30" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<a href="https://linkedin.com/in/alex-ricciardi"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://www.threads.net/@alexomegapy?hl=en"><img height="30" src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
<a href="https://dev.to/alex_ricciardi"><img height="30" src="https://img.shields.io/badge/DEV.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" alt="DEV.to"></a>
</p>
