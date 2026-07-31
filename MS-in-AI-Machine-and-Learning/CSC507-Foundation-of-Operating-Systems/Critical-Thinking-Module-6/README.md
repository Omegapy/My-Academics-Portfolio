# Critical Thinking Module 6
Project: CTA6 - Real-Time Process Scheduling

Data:  06/21/2026  
Grade: 100% | A

---

Foundation of Operating Systems CSC507  
Professor: Dr. Joseph Issa  
Spring C (26SC) – 2026   
Student: Alexander (Alex) Ricciardi 

---

Program Requirements:
- Ubuntu
- Python
- Bash (Terminal)

---

## Assignment Directions

Evaluate Real-Time Process Scheduling

In an earlier module, you created programs that read the contents of a large file and process it, writing the results into another large file. What if the files were 10x bigger, i.e. instead of a million rows, they were 10 million rows? Which of the following methods would have the fastest processing time:

1. Run the process as it is, with the larger files.
2. Break the input file up into 10 files and schedule the process on each one to run in real-time, then combine the resulting files into a single output file. 
3. Break the input file up into 2 files and schedule the process on each one to run in real-time, then combine the resulting files into a single output file. 
4. Break the input file up into 5 files and schedule the process on each one to run in real-time, then combine the resulting files into a single output file. 
5. Break the input file up into 20 files and schedule the process on each one to run in real-time, then combine the resulting files into a single output file.

Can you think of other ways to increase efficiency and reduce processing time? Describe in detail or provide a script to do so, with expected results for each method. Feel free to create such scripts and run them, to have actual results instead of theoretical results.

**Grading Criteria**  
- Your paper should be 2-3 pages in length, not including the cover page and references page.
- Your paper must be formatted according to APA guidelines in the CSU Global Writing Center (available in the left-hand navigation panel).
- Your claims should be supported by evidence.  Include at least 3 credible references. The CSU Global Library (available in the left-hand navigation panel) is a good place to find these references.
- All references must be cited in the text and listed on the references page, according to APA formatting.

---

**Project Map:**

- CTA6 - Real-Time Process Scheduling.pdf contains the APA essay and screenshots

Root Files and Folders

| Path                                       | Description                                                                                                                                                             |
|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `README.md`                                | Assignment overview, requirements, rubric, links, and this file map.                                                                                                    |
| `CTA6 - Real-Time Process Scheduling.pdf` | Main CAT-6 written paper for submission.                                                                                                                                |
| `cat6_realtime_scheduling_benchmark.py`    | Python benchmark harness that creates or reuses the 10,000,000-line input file, runs the scheduling/file-processing methods, verifies outputs, and records CSV results. |
| `run_cat6_benchmark.sh`                    | Bash runner that captures Ubuntu system information and launches the Python benchmark with configurable environment variables.                                          |
| `benchmark_output/`                        | Generated benchmark evidence, including the large input file, result CSV, system information, method output files, and temporary split-file workspace.                  |


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

