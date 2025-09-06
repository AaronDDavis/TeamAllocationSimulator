import csv
import random
# importing modules required

def access_csv(csv_file_name):
    """
    This function reads data from a CSV file and organizes it 
    into a dictionary where each tutorial group has a list of dictionaries 
    containing the information of each student in that particular tutorial group.

    Returns:
        dict: A dictionary where keys are tutorial group names and values are lists 
              of student dictionaries. Each student dictionary contains the 
              following keys: "id", "school", "name", "gender", and "CGPA".
    """
    students = {} # Initialize an empty dictionary to store student data
    with open(csv_file_name, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Add student data to the list corresponding to the tutorial group if it exists else create a list
            students.setdefault(row["Tutorial Group"], []).append({
                "id": row["Student ID"],
                "school": row["School"],
                "name": row["Name"],
                "gender": row["Gender"],
                "CGPA": float(row["CGPA"]) # Converting CGPA to float
            })
    return students

def generate_male_female(tutorial):
    """
    This function iterates through a list of student dictionaries and 
    categorizes them based on their gender.

    Args:
        tutorial (list): A list of student dictionaries. 
                         Each dictionary contains a "gender" key.

    Returns:
        tuple: A tuple containing two lists:
            - male: A list of male student dictionaries.
            - female: A list of female student dictionaries.
    """

    # Initialize empty lists to store students of each gender
    male = []
    female = []

    # Iterate through the tutorial
    for student in tutorial:
        if student["gender"] == "Male":
            male.append(student)
        else:
            female.append(student)
    
    return male, female

def calculate_gender_distribution(tutorial_male_num, tutorial_female_num, group_students_distribution):
    """
    This function determines the number of male and female students to be assigned to each group
    while maintaining the overall gender ratio of the tutorial.

    Args:
        tutorial_male_num (int): The total number of male students in the tutorial.
        tutorial_female_num (int): The total number of female students in the tutorial.
        group_students_distribution (list): A list representing the required number of students in each group.

    Returns:
        tuple: A tuple containing two lists:
            - tutorial_male_distribution: A list containing the number of male students in each group.
            - tutorial_female_distribution: A list containing the number of female students in each group.
    """

    tutorial_total = tutorial_male_num + tutorial_female_num # Calculating the total number of students in the tutorial
    
    # Initializing empty lists to store the distribution of male and female students
    tutorial_male_distribution = []
    tutorial_female_distribution = []

    for students_in_group in group_students_distribution:
        # Calculating the number of males and females in each group
        group_male_num = round(tutorial_male_num / tutorial_total * students_in_group)
        group_female_num = students_in_group - group_male_num

        # Appending the calculated numbers to the respective distribution lists
        tutorial_male_distribution.append(group_male_num)
        tutorial_female_distribution.append(group_female_num)

        # Update the remaining number of male and female students
        tutorial_male_num -= group_male_num
        tutorial_female_num -= group_female_num
        tutorial_total = tutorial_male_num + tutorial_female_num

    return tutorial_male_distribution, tutorial_female_distribution

def generate_groups(tutorial_male, tutorial_female, male_distribution, female_distribution, tutorial_cgpa, size):
    """
    Generates groups of students based on gender distribution, CGPA, and school diversity.

    This function attempts to create groups of students that satisfy the specified criteria:
    - Gender balance: The number of male and female students in each group should be as close as possible to the desired distribution.
    - CGPA range: The average CGPA of each group should be within a certain tolerance range of the tutorial average.
    - School diversity: Each group should have a minimum number of unique schools represented.

    Args:
        tutorial_male (list): List of male students in the tutorial.
        tutorial_female (list): List of female students in the tutorial.
        male_distribution (list): Desired distribution of male students across groups.
        female_distribution (list): Desired distribution of female students across groups.
        tutorial_cgpa (float): Average CGPA of the entire tutorial.
        size (int): Desired size of each group.

    Returns:
        list: A list of groups, where each group is a list of student dictionaries.
    """

    # Creating a copy of the original male and female student lists
    tutorial_male_original = tutorial_male[:]
    tutorial_female_original = tutorial_female[:]

    # Initializing the tolerance for CGPA and minimum number of schools required
    cgpa_diff = 0.005
    min_schools_required = size

    # Counter to adjust tolerances/ gender distribution
    k = 0
    l = 0


    # Main loop to generate groups until a suitable arrangement is formed
    while True:
        group_number = 0
        groups = []
        j = 0     # Group recreation attempt counter
        continue_outer = False

        # Loop to create groups until last group
        while len(tutorial_male) + len(tutorial_female) > size+1:
            group = []
            redo_group = False # Flag to indicate whether group needs to be redone

            # Creating a copy of the current male and female lists
            tutorial_male_copy = tutorial_male[:]
            tutorial_female_copy = tutorial_female[:]

            # Selecting students based on gender distribution
            for i in range(male_distribution[group_number]): # Male students
                student = random.choice(tutorial_male)
                group.append(student)
                tutorial_male.remove(student)
            for i in range(female_distribution[group_number]): # Female students
                student = random.choice(tutorial_female)
                group.append(student)
                tutorial_female.remove(student)
            
            # Calculating average cgpa of the group
            group_cgpa = calculate_average_cgpa(group)

            # Checking if the school has sufficient school diversity
            redo_group = calculate_schools(group, min_schools_required)

            # Checking whether the group's CGPA is within the tolerance range
            if not (tutorial_cgpa - cgpa_diff <= group_cgpa <= tutorial_cgpa + cgpa_diff):
                redo_group = True

            # Handling Group Recreation
            if redo_group:
                j += 1
                redo_group = False # reset flag

                if j == 500:
                    j = 0 # reset counter
                    continue_outer = True
                    k += 1 

                    if k == 500:
                        k = 0
                        l += 1

                        # Increase CGPA tolerance
                        cgpa_diff += 0.005

                        # If cgpa range is getting too high and minimum schools required is not very low,
                        # reset cgpa tolerance and decrease minimum schools required.
                        if (cgpa_diff >= 0.015 and min_schools_required > size * 0.75) or (cgpa_diff >= 0.025 and min_schools_required > size * 0.6):
                            cgpa_diff = 0.005
                            min_schools_required -= 1
                        
                        # However, for extreme cases where
                        # both cgpa difference and gender distribution are not good,
                        # change the gender distribution
                        # and reset the other tolerance levels
                        elif (cgpa_diff >= 0.025 and min_schools_required > size * 0.35) and l > 500:
                            l = 0

                            # Adjusting gender distribution only if it is not already very uneven
                            if size//2 in male_distribution:
                                male_distribution, female_distribution = change_gender_distribution(male_distribution[:], female_distribution[:], size)
                            elif size//2 in female_distribution:
                                female_distribution, male_distribution = change_gender_distribution(female_distribution[:], male_distribution[:], size)
                            
                            # resetting cgpa difference and minimum schools required
                            cgpa_diff = 0.005
                            min_schools_required = size

                    break
                else:
                    # reset students in the tutorial
                    tutorial_male = tutorial_male_copy[:]
                    tutorial_female = tutorial_female_copy[:]
                    continue

            # Add valid group to the list
            groups.append(group)
            group_number += 1

        if continue_outer:
            # reset flag
            continue_outer = False
            # reset students in the tutorial
            tutorial_male = tutorial_male_original[:]
            tutorial_female = tutorial_female_original[:]
            continue

        # Merge the remaining students in the last group
        group = tutorial_male + tutorial_female
        
        # Do the same things as done for the other groups to this
        group_cgpa = calculate_average_cgpa(group)
        redo_group =  calculate_schools(group, min_schools_required)

        if (not (tutorial_cgpa - cgpa_diff <= group_cgpa <= tutorial_cgpa + cgpa_diff)) or redo_group:
            tutorial_male = tutorial_male_original[:]
            tutorial_female = tutorial_female_original[:]
            continue

        # If the last group is also valid
        groups.append(group)

        break # to end the outer while loop since a valid arrangement has been found

    return groups

def change_gender_distribution(gender_1_distribution, gender_2_distribution, size):
    """
    This function adjusts the groups to make the distribution slightly but not heavily uneven.

    Args:
        gender_1_distribution (list): A list representing the distribution of the first gender.
        gender_2_distribution (list): A list representing the distribution of the second gender.
        size (int): The desired group size.

    Returns:
        tuple: A tuple containing the modified gender distributions:
            - gender_1_distribution: The adjusted distribution of the first gender.
            - gender_2_distribution: The adjusted distribution of the second gender.
    """

    # Finding a group with exactly half the desired size for gender_1
    i1 = gender_1_distribution.index(size//2)

    try:
        # Finding another group with half the size or one more student of gender_1
        i2 = gender_1_distribution.index(size//2 if gender_1_distribution.count(size//2) > 1 else size//2 + 1, i1+1)
        
        # Adjusting the distribution between the two groups
        gender_1_distribution[i1] -= 1
        gender_2_distribution[i1] += 1
        gender_1_distribution[i2] += 1
        gender_2_distribution[i2] -= 1

    except ValueError: # If the second group of size//2 or size//2 + 1 is not found
        if size//2 - 1 in gender_1_distribution: # If a group of size//2 - 1 is present
            i2 = gender_1_distribution.index(size//2-1) # Access its index

            # Adjusting the distribution between the two groups
            gender_1_distribution[i1] += 1
            gender_2_distribution[i1] -= 1
            gender_1_distribution[i2] -= 1
            gender_2_distribution[i2] += 1
            
    return gender_1_distribution, gender_2_distribution

def calculate_average_cgpa(group):
    """
    Calculates the average CGPA of a group of students.

    This function iterates through a list of student dictionaries, extracts 
    their CGPA values, sums them up, and divides this by the total number of 
    students to compute the average CGPA.

    Args:
        group (list): A list of student dictionaries. Each dictionary
                      contains a "CGPA" key with a numeric value.

    Returns:
        float: The average CGPA of the group. Returns 0 if the group is empty.
    """
    return sum(student["CGPA"] for student in group) / len(group) if group else 0

def calculate_schools(group, min_schools_required):
    """
    Checks if a group has sufficient school diversity.

    This function determines if the number of unique schools in a group
    of students meets the minimum requirement for school diversity.

    Args:
        group (list): A list of student dictionaries.
        min_schools_required (int): The minimum number of unique schools 
                                    required in the group.

    Returns:
        bool: True if the number of unique schools is less than the minimum 
              required, indicating insufficient diversity. False otherwise,
              indicating sufficient diversity.
    """
    schools = {} # Creating an empty dictionary to store the count of students from each school

    for student in group:
        # If the school is already in the dictionary, increment its count by 1.
        # Otherwise, add the school to the dictionary with a count of 1.
        schools[student["school"]] = schools.get(student["school"], 0) + 1

    # Returning True if number of uniques schools < minimum value required, else False
    return len(list(schools.keys())) < min_schools_required

def number_of_students_in_each_group(size):
    """
    Calculates the distribution of students across groups.

    This function determines the number of students to be assigned to each 
    group, ensuring that the total number of students is accommodated 
    while maintaining a distribution that contains more groups of
    the desired size.

    Args:
        size (int): The initial size of each group.

    Returns:
        tuple: A tuple containing two elements:
            - distribution (list): A list representing the number of students in each group.
            - size (int): The adjusted size of the groups after considering the remainder.
    """

    remainder = 50 % size

    if remainder > (size)//2:
        size = size - 1
        remainder = 50 % size
    # Example: When size = 9, remainder = 5 we decrease the ideal size to 8
    # Since size = 8, remainder = 2. When left over students students are added, there will be 2 groups of 9, and 4 groups of 8.

    # Creating a list to store the distribution of students across groups.
    # Initially, all groups are assigned the adjusted group size.
    distribution = [size] * (50//size)
    
    # Distributing the remaining students evenly across the groups,
    # by adding one extra student to the last 'remainder' groups.
    for i in range(remainder):
        distribution[-(i+1)] += 1

    return distribution, size

def input_size():
    """
    Inputs and validates the number of students per group.
    
    This function repeatedly prompts the user for input,
    until a valid integer within the range of 4 to 10 is provided.
    It handles potential errors like non-integer input and out-of-range values.
    
    Returns:
        int: The validated number of students per group.
    """
    
    while True:
        size = input("Please enter number of students per group:")
        
        try:
            # Try to convert the input to an integer
            size = int(size)
        except:
            #Handle non-integer input
            print("Please enter an integer\n")
            continue

        # Checking if the input is within the valid range
        if not (4 <= size <= 10):
            print("Size must be less than 11 and greater than 3\n")
            continue

        # Return input if valid
        return size
    
def main():
    """
    The main function of the program.

    Reads the student data from the CSV file, 
    takes input for the desired group size, and
    generates groups for each tutorial based on gender, CGPA, and school diversity.
    """

    # Read student data from CSV File
    students = access_csv("records.csv")

    # Get desired group from the user
    size = input_size()

    # Determine the number of students in each group
    group_students_distribution, size = number_of_students_in_each_group(size)

    # Iterate through each tutorial
    for tutorial_name, tutorial in students.items():
        print("\n\n" + tutorial_name)
        
        # Separating students into male and female lists
        tutorial_male, tutorial_female = generate_male_female(tutorial)

        # Determining the ideal number of male and female students in each group
        male_distribution_initial, female_distribution_initial = calculate_gender_distribution(len(tutorial_male), len(tutorial_female), group_students_distribution)

        # Generating the groups
        tutorial_groups = generate_groups(tutorial_male, tutorial_female, male_distribution_initial, female_distribution_initial, calculate_average_cgpa(tutorial), size)

        i = 1
        for group in tutorial_groups:
            print(i)
            for student in group:
                print(student)
            print()
            i += 1

if __name__ == "__main__":
    main()