# Portfolio Milestone Module 3 

Data: 05/31/2026  
Grade: 100% | A

---

Foundation of Operating Systems CSC507  
Professor: Dr. Joseph Issa 
Spring C (26SC) – 2026   
Student: Alexander (Alex) Ricciardi 

---
Program Requirements:
- Ubuntu Desktop 24.04.1 LTS
- Bash or a Linux shell
- Python 3

---

## How to Run in the Linux Terminal

Run these commands from the repository root:


```bash
cd CTAs/Portfolio-Milstone-Module-3
chmod +x bash_random_file1_benchmark.sh
./bash_random_file1_benchmark.sh
python3 create_file2.py
wc -l file1.txt file2.txt
```

Expected result:

- `bash_random_file1_benchmark.sh` deletes the previous `file1.txt`, creates a new `file1.txt` with 1,000,000 random-number lines, and prints start time, end time, elapsed seconds, and elapsed `HH:MM:SS`.
- `create_file2.py` creates `file2.txt` with 1,000,000 random-number lines and benchmarks the sequential, buffered, threaded, and multiprocessing Python methods.
- `benchmark_results.csv` contains one row for each Python method.
- `wc -l file1.txt file2.txt` should report:

```text
1000000 file1.txt
1000000 file2.txt
2000000 total
```

The script should be run from the `Portfolio-Milstone-Module-3/` directory so `file1.txt`, `file2.txt`, and `benchmark_results.csv` are created in the correct assignment folder.

### Optional Python Benchmark Controls

The Python program defaults to the full assignment benchmark:

```bash
python3 create_file2.py
```

For a small syntax or smoke test, run a reduced line count:

```bash
python3 create_file2.py --line-count 1000 --chunk-size 100 --workers 2
```

Available options:

```bash
python3 create_file2.py \
  --line-count 1000000 \
  --methods sequential,buffered,threaded,multiprocessing \
  --workers "$(python3 -c 'import os; print(os.cpu_count() or 1)')" \
  --chunk-size 50000 \
  --csv benchmark_results.csv
```

---

## Expected result:

Capture the Ubuntu terminal after running the Bash script, Python benchmark, and `wc -l file1.txt file2.txt` verification command. The screenshot should show:

- Bash start time, end time, elapsed seconds, and elapsed `HH:MM:SS`.
- Python timing results for all four methods.
- `wc -l` line counts showing one million lines in both generated files.

---

## File Map

| File                              | Purpose                                                                                                                                               |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `README.md`                       | This file and file map.                                                                                                                               |
| `bash_random_file1_benchmark.sh`  | Bash benchmark file. It deletes the old `file1.txt`, creates one million random-number lines with `$RANDOM`, and reports elapsed time with `SECONDS`. |
| `create_file2.py`                 | Python benchmark file. It creates `file2.txt` and compares sequential, buffered, threaded, and multiprocessing methods.                               |
| `results_summary.pdf`            | Results summary from benchmarks                                                                                                                       |
| `benchmark_results.csv`           | Created by `create_file2.py`; Python runtime results after the Ubuntu run.                                                                            |
| `file1.txt`                       | Created by `bash_random_file1_benchmark.sh`; contains 1,000,000 random-number lines after the Ubuntu run.                                             |
| `file2.txt`                       | Created by `create_file2.py`; contains 1,000,000 random-number lines after the Ubuntu run.                                                            |


---

# Assignment

**This assignment is a Portfolio Milestone for Module 3.**

In a Linux installation, use Bash or a Linux shell to:

1. Display the system time before and after the process, and use Bash `SECONDS` to report elapsed runtime.
2. Modify the `for` loop to repeat one million times.
3. Delete the prior `file1.txt`.
4. Run the script and verify the new `file1.txt`.

Then create a Python program to generate `file2.txt`, compare execution times, and test at least two additional methods for improving execution time. This implementation compares sequential writing, buffered writing, threaded chunk generation, and multiprocessing chunk generation.

The written findings are in [`module3_results_summary.md`](module3_results_summary.md).

### Course Context

- [Module 1](../../Module-1/) introduces operating-system foundations.
- [Module 2](../../Module-2/) introduces processes and threads.
- [Module 3](../../Module-3/) introduces concurrency, synchronization, and scheduling.
- [Portfolio Milestone Module 2](../Portfolio-Milstone-Module-2/) provides the earlier 1,000-line Bash and Python template.

---

My Links:

<a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" align="left" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></a>
<a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" align="left" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></a>

[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)

<a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></a>
<a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></a><br>
