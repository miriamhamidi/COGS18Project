import pandas as pd

class ResearchGroup():
    """ Creates research group object.

        Paramaters
        ----------
        df : dataframe
            contains name, prinicipal inverstigator, related courses, student entry level,
            and description for each research group
        row_index : integer
            gives index number for current row in df

        Returns
        -------
        Object with information from df as attributes. 

    """
    def __init__(self, row_index, df):
        self.name = df.loc[row_index, 'research group']
        self.pi = df.loc[row_index, 'PI']
        self.courses = str(df.loc[row_index, 'related classes'])
        self.entry = df.loc[row_index, 'undergrads/grads/na']
        self.description = df.loc[row_index, 'description']


def object_initializer(df):
    """ Creates initial list of all research group from df that will be narrowed down by user inputs later.

        Paramaters
        ----------
        df : dataframe
            contains name, prinicipal inverstigator, related courses, student entry level,
            and description for each research group

        Returns
        -------
        List containing objects for each research group in df.

    """
    research_groups = []

    for i in range(0, len(df.index)):
        current_group = ResearchGroup(i, df)
        research_groups.append(current_group)

    return research_groups

def get_courses(df):
    """ Extracts all courses that are related to research groups to query the user with. 
 
        Paramaters
        ----------
        df : dataframe
            contains related courses as a string with course numbers as three digits separated by commas

        Returns
        -------
        all_courses : list of strings
            List with the all the ECE courses in the df as three digit numbers.

    """
    all_courses = []

    #go to correct row in df
    for research_group in range(0, len(df.index)):
        class_title = ''
        #creates list of characters from cell containing courses
        class_list = list(str(df.loc[research_group, 'related classes']))

        #add number from character list to string for course number 
        for character in class_list:
            if character in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                class_title = class_title + character
                #when course number 3 digits long, append to courses list, clear string
                if len(class_title) == 3:
                    all_courses.append(class_title)
                    class_title = ''

    all_courses = set(all_courses)
    all_courses = list(all_courses)

    return all_courses

def make_courses_taken_list(taken_courses):
    """ Creates list of courses the user from their input string.
 
        Paramaters
        ----------
        taken_courses: string
            user inputted string containing courses they took as three digit numbers separated by commas
 
        Returns
        -------
        taken_list: list of strings
            A list with the all the ECE courses the user took as three digit numbers.
 
    """
    taken_list = []
    class_title = ''

    #refer to similar technique in get_courses function above
    for character in taken_courses:
        if character in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            class_title = class_title + character
            if len(class_title) == 3:
                taken_list.append(class_title)
                class_title = ''

    taken_list = set(taken_list)
    taken_list = list(taken_list)

    return taken_list

def make_elig_list(entry_value, df): #narrow down list by ungraduate or graduate student
    """ Narrows research group list by whether student is a graduate or undergraduate.
 
        Paramaters
        ----------
        entry_value: string, either 'U' or 'G'
            will use this string to remove research groups that specifically 
            exclude graduate or undergraduate students
        df: dataframe
            contains whether each research group has only 'U' for undergraduates, 'G'
            for graduate students, 'B' for both, or 'N' for not listed

        Returns
        -------
        research_groups: list of ResearchGroup objects
            A list with all research groups the user is still eligible for. 

    """
    research_groups = object_initializer(df) 

    #we only remove groups opposite to user, so 'B' and 'N' groups stay regardless of entry_value
    if entry_value == 'U':
        for group in research_groups:
            if group.entry == 'G':
                research_groups.remove(group)

    elif entry_value == 'G':
        for group in research_groups:
            if group.entry == 'U':
                research_groups.remove(group)

    return research_groups

def narrow_by_course(taken_courses, eligibility_list):
    """ Narrows research group list to those related to courses of interest to user.

        Paramaters
        ----------
        taken_courses: list
            list of 3 digit course numbers user inputted as strings
        eligibility_list: list
            list of courses user is eligibile for (already filtered by grad or ugrad)

        Returns
        -------
        new_list: list of ResearchGroup objects
            list of research groups the user is both eligible for and interested
            in based on courses indicated

    """
    new_list = []

    for course in taken_courses:
        for group in eligibility_list:
 
            #see if the course user inputted is in or equal to any of the group's courses
            if (course in str(group.courses)) or (course == str(group.courses)):         
                new_list.append(group)

            #do not add an eligible group if it has no courses of interest to user
            elif course != str(group.courses):
                pass

            else:
                if group in new_list:
                    pass

    return new_list

def make_input_prof_list(profs_chosen):
    """ Creates list of professors the user has chosen.
        
        Paramaters
        ----------
        profs_chosen: string
            user inputted string containing professor names separated by commas
       
        Returns
        -------
        prof_list: list of strings
            A list with the all the professors the user took.
             
    """
    prof_list = []
    prof_name = ''

    #going through each character in input string
    for character in profs_chosen:

        #whenever there is a letter, add the letter to a string
        if character != ',':
            prof_name = prof_name + character

        #when there is a comma, add the current string to the list and clear it for next name    
        else:
            prof_list.append(prof_name)
            prof_name = ''

    #Because there is no comma for the last name in the list, add leftover string
    if prof_name != '':
        prof_list.append(prof_name)

    return prof_list

def narrow_by_prof(chosen_profs, eligibility_list):
    """ Narrows research group list to those led by certain professors.

        Paramaters
        ----------
        chosen_profs: list of strings
            list of professor names user chose
        eligibility_list: list
            list of courses user is eligibile for (already filtered by grad or ugrad)
 
        Returns
        -------
        new_list: list of ResearchGroup objects
            list of research groups the user is both eligible for and interested
            in based on professor indicated
 
    """
    new_list = []

    #check the pi attribute of every group to see if it contains prof chosen
    for group in eligibility_list:
        for pi in chosen_profs:
            if pi in group.pi:
                new_list.append(group)

    return new_list

def display_output(eligibility_list):
    """ Display research groups matched, and give user the option to end search or view df.
        
        Paramaters
        ----------
        eligibility_list: list
            list of courses user is eligibile for (filtered by grad or ugrad AND course/prof preference)
                 
        Returns
        -------
        nothing, but wll print outcome or restart program

    """
    import pandas as pd
    print('\n')
    user_input = 'initial'

    #if there is no match in df
    if not eligibility_list:

        #make sure the user is inputting one of the options by checking input
        while user_input not in ('a', 'r', 'e'):
            user_input = input('No research groups matched. Type' + \
                               ' \'r\' to retry with new criteria' + \
                               ' or \'a\' to print all groups in the database' + \
                               ' or \'e\' to end.')
            user_input = str(user_input)

        #will restart search from scratch
        if user_input == 'r':
            start_gui()

        #will print df
        elif user_input == 'a':
            print(pd.read_excel('fixed_names1111.xlsx', header=0))

        #will end program
        elif user_input == 'e':
            print('Thanks for searching.')

    #if the user is eligible for some groups, print what they are
    else:
        print('\n')
        print('Based on your input, these research groups may be of interest to you:')
        print('\n')
        for i in eligibility_list:
            print('\n')
            print(i.name+'...'+i.description)

def start_gui(entry='', criteria='', pi='', taken_courses='', entry_status=True, criteria_status=True):
    """ Display main gui which runs all other functions.

        Paramaters
        ----------
        entry: string
            user input of 'G' or 'U' (made an input here for hard coding examples)

        criteria: string
            user input of choice to narrow list by professor, 'pi', or by courses, 'courses'
 
        pi: string
            user input of any part of professor name
 
        taken_courses: string
            user input of courses they have taken as three digit course numbers
 
        entry_status,criteria_status: boolean
            boolean used to change user prompt if they are not entering the right values


        Returns
        -------
        nothing, but leads to functions that print matched research gruosp

    """

    #import pandas as pd

    global df
    df = pd.read_excel('fixed_names1111.xlsx', header=0)    
    research_groups = object_initializer(df)

    #use this loop rerun prompt until user input is on of correct options
    while entry not in ('G', 'U'):
        if not entry_status:
            print('\n')
            print('You must type \'G\' or \'U\' to continue.')
        entry = input('Are you a grad or undergrad student? Type \'G\' for grad and \'U\' for undergrad:')
        entry_status = False

    #make list of all possible research groups 
    eligibility_list = make_elig_list(entry, df)
    print('\n')
 
    #have user choose a criteria to narrow list by
    while criteria not in ('PI', 'courses'):
        if not criteria_status:
            print('\n')
            print('You must type \'PI\' or \'courses\' to continue.')
        criteria = input('Select a critera for your search through different research groups at UCSD.' + \
                         ' Type \'PI\' to search by professor'+ \
                         ' or type \'courses\' to search by courses: ')
        critera_status = False

    if criteria == 'PI':
        print('\n')
        for group in eligibility_list:
            print(group.pi)
        print('\n')
    
        while pi == '':
            pi = input('Do you want or have had one of these PIs?'+\
                       'Type their first or last name or None: ')
    
        #parsing input, filtering list, then displaying
        chosen_profs = make_input_prof_list(pi)
        eligibility_list = narrow_by_prof(chosen_profs, eligibility_list)
        display_output(eligibility_list)

    elif criteria == 'courses':
        print('\n')
        all_courses = get_courses(df)
        print(all_courses)
        print('\n')

        while taken_courses == '':
            taken_courses = input('Have you taken any of these ECE courses? Do any interest you?' + \
                                  ' List any course numbers that interest you as three digits separated by a comma: ')

        #parsing input, filtering list, then displaying
        taken_courses = make_courses_taken_list(taken_courses)
        eligibility_list = narrow_by_course(taken_courses, eligibility_list)
        display_output(eligibility_list)