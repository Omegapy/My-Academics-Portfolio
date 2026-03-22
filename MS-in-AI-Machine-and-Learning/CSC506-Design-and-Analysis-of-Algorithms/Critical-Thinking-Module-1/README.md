# Critical Thinking Module 1 - Data Structures & Complexity
Program Name: Data Structures Interactive Demo

Data:  03/22/2026  
Grade:
---

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover
Spring A (26SA) – 2026   
Student: Alexander (Alex) Ricciardi   

---

**Project Description:**

The project includes a Python 3.12+ terminal UI application that demonstrates the functionality of three data structures: stack, queue, and linked list.   
It also includes a complexity analyzer, that predicts the time complexity of common operations for each data structure. Finally, it includes a performance comparison report that compares the predicted vs. actual operation times. The analysis is performed using a Jupyter notebook and the results are presented in a HTML report.

---

**Assignment:**

Requirements. 
1. Implement three fundamental data structures: stack, queue, and linked list.
2. Create a simple interface that shows how each data structure works.
3. Build a complexity analyzer that predicts time/space complexity for common operations (insert, delete, search).
4. Include visual demonstrations showing when to use each data structure.
5. Add performance testing that compares predicted vs. actual operation times.

Deliverables. 
1. Working implementations of stack, queue, and linked list with clear documentation
2. User interface demonstrating each data structure's operations
3. Complexity prediction tool showing Big-O estimates for operations
4. Performance comparison report with charts showing prediction accuracy
5. 1-page analysis explaining data structure importance and selection criteria
6. Demo video (3-5 minutes) showing tool functionality

---

Program Requirements:
- Python 3.12+
- `colorama` (install via `pip install colorama`)
- `matplotlib`, `pandas`, `jupyter` (for the analysis notebook)

---

**How to Run:**

```bash
# Option 1: Run from inside the CTA-1 folder
python main.py

# Launch the notebook from inside the CTA-1 folder
jupyter notebook analysis/complexity_report.ipynb

```

---

Video describing the project structure:  
https://youtu.be/j2OdmCRERt4

**Project Map:**

``` 
CTA-1/
├── CTA-1 - Data Structures Demonstration Screenshots.docx    # Screenshot UI Data Structures demo 
├── Data Structure Importance and Selection Criteria.docx     # 1 page Written analysis 
├── project_video                  # see https://youtu.be/j2OdmCRERt4
├── main.py                        # Entry point, welcome banner, launches app
├── README.md                      # This file
├── complexity_report.html         # HTML of the analysis from the Jupyter notebook
├── data_structures/
│   ├── __init__.py                
│   ├── node.py                    # Shared Node dataclass (building block)
│   ├── stack_ds.py                # Stack -> LIFO
│   ├── queue_ds.py                # Queue -> FIFO
│   └── linked_list_ds.py          # Singly linked list
├── utilities/
│   ├── __init__.py
│   ├── README.md                  # Notes for the reusable CTA-1 helper package
│   ├── menu_banner_utilities.py   # Banner/menu for the console UI
│   └── validation_utilities.py    # Shared input-validation utilities
├── ui/
│   ├── __init__.py               
│   ├── app.py                     # Main menu + sub-menu routing
│   └── display_helpers.py         # Visual diagrams + educational explanations
└── analysis/                      # Complexity analysis & benchmarking
    ├── __init__.py                
    ├── complexity_analyzer.py     # Rules-based Big O 
    ├── benchmark_utils.py         # Benchmark runner / CSV export 
    ├── complexity_report.ipynb    # Jupyter notebook, main analysis 
    ├── benchmark_results.csv      # Images benchmark data
    └── charts/                    # Images PNG charts
        ├── stack_visual.png
        ├── stack_timings.png
        ├── queue_visual.png
        ├── queue_timings.png
        ├── linked_list_visual.png
        ├── linked_list_timings.png
        ├── prediction_accuracy.png
        └── summary_comparison.png
```

---

**Operations Supported:**

| Data Structure | Operations                                             |
|----------------|--------------------------------------------------------|
| **Stack**      | Push, Pop, Peek, Display                               |
| **Queue**      | Enqueue, Dequeue, Front, Display                       |
| **Linked List**| Prepend, Append, Insert After, Delete, Search, Display |

---

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 
