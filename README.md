# Team Allocation Simulator for SC1003

This is a Python-based **Team Allocation Simulator** developed individually for the mini-project in the Nanyang Technological University (NTU) course **SC1003: Introduction to Computational Thinking and Programming**. The project addresses the challenge of efficiently forming balanced and diverse student teams in a large course with 6,000 students.

The script processes a `records.csv` file containing student data and groups them within their respective tutorial sections. The core objective is to create teams that are fair and diverse by considering multiple criteria simultaneously.

<br>


---

## Key Features

This simulator forms teams based on the following principles to ensure fairness and diversity:

* **Custom Team Size**: The user can specify the number of students per team, ranging from **4 to 10**.
* **School Diversity**: The algorithm strives to create teams with a mix of students from different schools, avoiding a majority from a single school.
* **Gender Balance**: It promotes gender diversity by preventing teams from being dominated by a single gender.
* **Academic Balance**: It ensures teams are academically balanced by keeping the average CGPA of each group close to the tutorial's overall average, thus avoiding teams of only very high or very low-performing students.

<br>


---

## How It Works

The script employs an iterative, randomized algorithm that intelligently adjusts its own constraints to find an optimal solution.

1.  **Data Loading**: The program begins by reading the `records.csv` file and structuring the student data into a dictionary, where each key represents a tutorial group.
2.  **User Input**: It prompts the user to enter a desired team size (from 4 to 10). The script then calculates the distribution of team sizes to accommodate all 50 students in a tutorial group.
3.  **Criteria Calculation**: For each tutorial group, it calculates the overall CGPA average and the male-to-female ratio. These values serve as the baseline for forming balanced teams.
4.  **Iterative Group Generation**: This is the core of the algorithm (`generate_groups` function).
    * The script enters a loop, attempting to form teams that meet all criteria.
    * It randomly assigns students to a group based on the calculated gender distribution.
    * It then validates the newly formed group against the **CGPA** and **school diversity** rules.
    * If a group fails validation, the script discards it and retries with a different random selection of students.
5.  **Adaptive Tolerance**: If the algorithm struggles to find a valid team composition after numerous attempts, it gradually **loosens the constraints**.
    * It first increases the acceptable CGPA deviation from the mean (`cgpa_diff`).
    * If that's not enough, it reduces the minimum number of unique schools required per team (`min_schools_required`).
    * In extreme cases, it even makes minor adjustments to the gender distribution to explore new combinations.
    * This adaptive approach ensures that the program will always find a viable solution, even for tutorial groups with a skewed demographic.
6.  **Output**: Once a valid set of teams is formed for a tutorial group, the results are printed to the console before the program moves to the next tutorial group.

<!--*[A flowchart illustrating the team generation algorithm should be placed here]* -->

<br>

---

## How to Run the Program

No external analytical libraries are required, as the project relies solely on Python's standard `csv` and `random` modules, per the project requirements.

1.  Ensure you have Python 3 installed.
2.  Place the `records.csv` file in the same directory as the `Mini Project Final.py` script.
3.  Run the script from your terminal:
    ```bash
    python "TeamAllocationSimulator.py"
    ```
4.  When prompted, enter the desired number of students per group (an integer between 4 and 10).

The program will then process all 120 tutorial groups and print the final team rosters for each one.