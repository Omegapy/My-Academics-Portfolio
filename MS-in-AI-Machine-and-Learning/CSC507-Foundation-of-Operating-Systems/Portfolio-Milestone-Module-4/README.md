# Portfolio Milestone Module 4 

Data: 06/07/2026  
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

## Assignment Goal

Read `file1.txt`, double each number, and write the result to
`newfile1.txt`. Compare the required Bash implementation with three Python
processing methods:

1. Read the entire file into memory before processing.
2. Read and process one row at a time.
3. Split the file into two parts and read each part into memory separately.

## File Map

| File                          | Description                                                  |
|-------------------------------|--------------------------------------------------------------|
| README.md                     | This file                                                    |
| file1.txt                     | One-million-row source file from CTA3                        |
| file2.txt                     | Second one-million-row file from CTA3                        |
| double_numbers.sh             | Bash writes newfile1.txt                                     |
| double_numbers.py             | Benchmark with three methods                                 |
| newfile1.txt                  | Generated output file containing doubled file1.txt values    |
| benchmark_results.csv         | Combined Bash and Python timing results                      |
| bash_benchmark_result.csv     | Single-row Bash timing file used by the Python benchmark     |
| benchmark_results_test.csv    | Small-file Python timing results from the 10-line test run   |
| tempfile.txt                  | 10-line test input created from file1.txt                    |
| newfile1_test.txt             | Bash output from the 10-line test run                        |
| newfile1_test_python.txt      | Python output from the 10-line test run                      |
| Results Analysis.docx         | Analysis of the Bash and Python results                      |
| test_run.png                  | Screenshot of the small test run                             |
| full_run.png                  | Screenshot of the full benchmark run                         |
| verification.png              | Screenshot of line-count and doubled-value verification  |

## How to Run

Run all commands from the module directory:

```bash
cd Portfolio-Milstone-Module-4
./double_numbers.sh
python3 double_numbers.py --include-bash-result
```

The Bash script creates `newfile1.txt` and writes a Bash timing row to
`bash_benchmark_result.csv`. The Python script reruns the three Python methods,
verifies each output, and writes the combined results to `benchmark_results.csv`.

To run a small test file first:

```bash
cd ~/CSU/CSC-507/Portfolio-Milstone-Module-4
head -n 10 file1.txt > tempfile.txt
INPUT_FILE=tempfile.txt OUTPUT_FILE=newfile1_test.txt ./double_numbers.sh
python3 double_numbers.py \
  --input-file tempfile.txt \
  --output-file newfile1_test_python.txt \
  --csv-file benchmark_results_test.csv
```

## Verification Commands

```bash
wc -l file1.txt file2.txt newfile1.txt
head -n 10 file1.txt newfile1.txt
cat benchmark_results.csv
```


---

# Assignment

**This assignment is a Portfolio Milestone for Module 4.**

From the previous exercises, you have 2 files in your Linux installation: file1.txt and file2.txt, both with one million rows of random numbers. Create a new script, double_numbers.sh, to read each line of file1.txt, storing the number from each line into a variable, then write a value that is double the original number into another file called newfile1.txt. Once this is done for the entire contents of file1.txt, display the time it took to run. Your script might look as follows:

#!/bin/bash

SECONDS=0

while read -r number

do

  let "number *= 2"

  echo $number >> newfile1.txt

done < file1.txt

duration=$SECONDS

echo $duration

You may want to create a smaller file to work with until the process is working correctly. You can use the "head" command to grab the first 10 rows of file1.txt into another file, and use that file in your script:

head file1.txt > tempfile.txt

For proper syntax of reading files into variables, read this: How to read file line by line in Bash scriptLinks to an external site..

You can also use the "head" command to quickly verify that newfile1.txt contains numbers that are double the value of the corresponding rows of file1.txt:

head file1.txt newfile1.txt

Once you have the script working to your satisfaction, delete newfile1.txt and run double_numbers.sh. You should now have a file called newfile1.txt containing one million lines. You should also have information indicating how long this process took to run.

Using Python, create a program to perform this task, with 3 methods of doing this:

1. Read the entire contents of file1.txt into memory, then process each row.
2. Read one row of file1.txt at a time and process it.
3. Split file1.txt into 2 parts and read each part into memory separately.

Be sure to capture execution times for each method. How do they compare to each other, and to that of the double_numbers.sh script? Were there any surprises for you, or did the results match your expectations? Describe your findings in detail.

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
