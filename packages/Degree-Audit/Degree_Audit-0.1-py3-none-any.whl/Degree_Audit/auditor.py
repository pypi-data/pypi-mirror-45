"""
Degree Requirements Auditor
    Determine progress toward completion of a Master of Science in Computer Science Degree at NKU.
"""

from os import path
import unittest
from jinja2 import Environment
from jinja2 import FileSystemLoader
import webbrowser

class Course:
    """ Represents a college course

    Attributes :
    id -- Designation for the course of the form: CSC 500.
    credits -- Number of credit hours the course is worth.
    completed -- Boolean field indicating completion of the course.
    name -- Title of the course
    grade -- Grade received in course

    Methods :
    __init__
    markComplete -- Set completed and grade field when a course is completed
    """

    id = ""
    credits = 0
    completed = False
    name = ""
    grade = 0

    def __init__(self, id, credits, name):
        """ Instantiate a Course object and set attribute values
        Args:
        id -- id for course
        credits -- credit value for course
        name -- title of course

        Returns:
        Instantiated, initialized Course object
        """

        self.id = id
        self.credits = credits
        self.name = name

    def markcomplete(self, grade):
        """ Set completed and grade field when a course is completed
        Args:
        grade -- grade received in course
        """

        self.completed = True
        self.grade = grade


class Group:
    """ A group of courses and the number of credits required from the group to fulfill a requirement toward the degree.
        For instance, 3 credit hours in CSC 640 or CSC 666 are required.

    Attributes :
    reqCredits -- Total credits required from courses in the group.
    reqComplete -- Boolean representing requirement completion.
    reqIds -- List of ids of the form CSC 500, for courses in the group.
    requirement -- Text description of the number of courses required from the group for output.

    Methods :
    __init__
    checkComplete -- Set completed and grade field when a course is completed
    """

    reqCredits = 0
    reqComplete = False
    reqIds = []
    requirement = ""

    def __init__(self, credits, courseIds, requirement):
        """ Instantiate a Group object and set attribute values
        Args:
        credits -- credit value required from the group
        courseIds -- ids of courses in the group
        requirement -- text description of the requirement

        Returns:
        Instantiated, initialized Group object
        """
        self.reqCredits = credits
        self.reqIds = courseIds
        self.requirement = requirement

    def check_complete(self, courses):
        """ Set completed and grade field when a course is completed
        Args:
        courses -- dictionary indexed by course id and containing course objects for all available courses

        Returns:
        Boolean True if the required credits for the group have been completed, False otherwise
        """

        c = 0       # variable for calculating total credits completed
        for courseId in self.reqIds:
            course = courses[courseId]
            if course.completed:
                c += course.credits
        if c >= self.reqCredits:
            self.reqComplete = True
        return self.reqComplete


class Requirements:
    """ Class representing all requirements for degree completion.

    Attributes :
    totalCredits -- Total credits required from all groups for the degree.
    reqComplete -- List containing all group objects.
    courses -- Dictionary indexed by course id containing course objects for all classes offered.
    requirement -- Text description of the number of courses required from the group for output.
    group1-group4 -- Group objects for degree requirements.

    Methods :
    __init__
    prepare_courses --
    prepare_groups --
    check_credits --
    calc_gpa --
    prepare_audit --

    """

    totalCredits = 30
    reqGroups = []
    courses = {
        'CSC 502': Course('CSC 502', 3, 'Advanced Programming Methods'),
        'CSC 507': Course('CSC 507', 3, 'Concepts of Programming Languages'),
        'CSC 515': Course('CSC 515', 3, 'Android Mobile App Development'),
        'CSC 516': Course('CSC 516', 3, 'iOS Mobile App Development'),
        'CSC 525': Course('CSC 525', 3, 'Artificial Intelligence'),
        'CSC 533': Course('CSC 533', 3, 'Computer Networks'),
        'CSC 539': Course('CSC 539', 3, 'Software Testing and Maintenance'),
        'CSC 540': Course('CSC 540', 3, 'Software Engineering'),
        'CSC 550': Course('CSC 550', 3, 'Database Management'),
        'CSC 556': Course('CSC 556', 3, 'Advanced Web Application Development'),
        'CSC 560': Course('CSC 560', 3, 'Operating Systems'),
        'CSC 562': Course('CSC 562', 3, 'Computer Architecture'),
        'CSC 564': Course('CSC 564', 3, 'Design and Analysis of Algorithms'),
        'CSC 580': Course('CSC 580', 3, 'Computer Graphics'),
        'CSC 582': Course('CSC 582', 3, 'Computer Security'),
        'CSC 585': Course('CSC 585', 3, 'Theory of Computation'),
        'CSC 593': Course('CSC 593', 3, 'Research Seminar'),
        'CSC 594': Course('CSC 594', 3, 'Topics: Computer Science'),
        'CSC 599': Course('CSC 599', 3, 'Intermediate Independent Study'),
        'CSC 601': Course('CSC 601', 3, 'Advanced Programming Workshop'),
        'CSC 625': Course('CSC 625', 3, 'Advanced Artificial Intelligence'),
        'CSC 640': Course('CSC 640', 3, 'Advanced Software Engineering'),
        'CSC 645': Course('CSC 645', 3, 'Software Interface Design and Human Factor'),
        'CSC 650': Course('CSC 650', 3, 'Advanced Database Systems'),
        'CSC 660': Course('CSC 660', 3, 'Advanced Operating Systems'),
        'CSC 666': Course('CSC 666', 3, 'Secure Software Engineering'),
        'CSC 670': Course('CSC 670', 3, 'Social Implications of Computing'),
        'CSC 682': Course('CSC 682', 3, 'Advanced Computer Security'),
        'CSC 685': Course('CSC 685', 3, 'Logic and Computation'),
        'CSC 694': Course('CSC 694', 3, 'Advanced Graduate Topics: Computer Science'),
        'CSC 699': Course('CSC 699', 3, 'Independent Study')
    }
    # FixMe: Prompt for input of credits for 594, 599, 694, 699

    group1 = [
        'CSC 502',
        'CSC 540',
        'CSC 560',
        'CSC 564',
        'CSC 585',
        'CSC 601',
        'CSC 660',
        'CSC 685',
    ]
    group2 = [
        'CSC 640',
        'CSC 666',
    ]
    group3 = [
        'CSC 507',
        'CSC 515',
        'CSC 516',
        'CSC 525',
        'CSC 533',
        'CSC 539',
        'CSC 550',
        'CSC 556',
        'CSC 562',
        'CSC 580',
        'CSC 582',
        'CSC 593',
        'CSC 594',
        'CSC 599',
    ]
    group4 = [
        'CSC 625',
        'CSC 645',
        'CSC 650',
        'CSC 666',
        'CSC 670',
        'CSC 682',
        'CSC 694',
        'CSC 699',
    ]

    def __init__(self):
        """ Instantiate a Requirements object, instantiate Group objects for each group of requirements
         and place Group objects in reqGroups List

        Returns:
        Instantiated, initialized Requirements object
        """

        self.reqGroups = [Group(24, self.group1, "Take all of these"),
            Group(3, self.group2, "Take one of these"),
            Group(6, self.group3, "Take at least two of these"),
            Group(9, self.group4, "Take at least three of these")]

    def prepare_courses(self):
        """ Format course information for use with Jinja templates in html output

        Returns:
        coursedata -- Formatted, indexed by id dictionary of course information for output
        """

        coursedata = {}
        for id, course in self.courses.items():
            coursedata[id] = {'Grade': course.grade, 'Complete': course.completed,
                              'Course': course.id, 'Name': course.name, 'Credits': course.credits}
        return coursedata

    def prepare_groups(self):
        """ Format group course information for use with Jinja templates in html output

        Returns:
        Formatted, integer indexed dictionary for output
        """

        groupdata = {}
        i = 0
        for group in self.reqGroups:
            group.check_complete(self.courses)
            # format a row for displaying group requirement information
            groupdata[i] = {'Grade': 'G', 'Complete': group.reqComplete,
                        'Course': group.requirement, 'Name': '', 'Credits': ''}
            i += 1
            # format rows for courses in the requirement group
            for id in group.reqIds:
                course = self.courses[id]
                groupdata[i] = {'Grade': course.grade, 'Complete': course.completed,
                            'Course': course.id, 'Name': course.name, 'Credits': course.credits}
                i += 1
        return groupdata

    def check_credits(self):
        """ Calculate credits earned from all completed courses excluding waived courses

        Returns:
        Total credits earned toward degree
        """
        c = 0
        for id, course in self.courses.items():
            if course.completed and course.grade is not 'W':
                c += course.credits
        return c

    def calc_gpa(self):
        """ Calculate grade point average for completed courses

        Returns:
        Grade Point Average
        """
        creds = 0
        grades = 0
        for id, course in self.courses.items():
            if course.completed and course.grade is not 'W':
                creds += course.credits
                g = int(course.grade)
                if g >= 90:
                    grades += (4 * course.credits)
                elif g >= 80:
                    grades += (3 * course.credits)
                elif g >= 70:
                    grades += (2 * course.credits)
        return grades/creds

    def prepare_audit(self, input_data):
        """ Prepare data for displaying degree audit for user with user's uploaded completed courses and grades

        Returns:
        Formatted group and course information reflecting user's completed courses and grades
        """
        courses = self.courses
        for id, grade in input_data.items():
            courses[id].markcomplete(grade)
        groupdata = self.prepare_groups()
        return groupdata


class AuditorTest(unittest.TestCase):
    a = {'CSC 502': 99, 'CSC 507': 95, 'CSC 515': 92, 'CSC 525': 90}
    b = {'CSC 502': 89, 'CSC 507': 85, 'CSC 515': 85, 'CSC 525': 80}

    def test_mark_complete(self):
        r = Requirements()
        for id in self.a:
            r.courses[id].markcomplete(self.a[id])
        self.assertEqual(r.courses['CSC 507'].completed, True)

    def test_calc_gpa_a(self):
        r = Requirements()
        for id in self.a:
            r.courses[id].markcomplete(self.a[id])
        self.assertEqual(r.calc_gpa(), 4.0)

    def test_calc_gpa_b(self):
        r = Requirements()
        for id in self.b:
            r.courses[id].markcomplete(self.b[id])
        self.assertEqual(r.calc_gpa(), 3.0)

    def test_check_credits(self):
        r = Requirements()
        for id in self.a:
            r.courses[id].markcomplete(self.a[id])
        self.assertEqual(r.check_credits(), 12)


def audit_report(file):
    """ Opens a browser and displays a completed degree audit of user's progress toward earning a MSCS degree at NKU
    Argument:
    Requires a .txt file with completed courses and grades
    Must be of the form:
        CSC 502, 98
        CSC 540, 86
        ...

    Returns:
    Html file with completed degree audit and GPA
    """

    read_data = {}
    try:
        with open(file) as f:
            if path.getsize(file) > 0:
                for line in f:
                    i = line.index(',')
                    id = line[0:i].strip()
                    grade = line[i+1:].strip()
                    read_data[id] = grade
                f.close()
            else:
                raise ImportError('Empty File')
                return -1
    except FileNotFoundError:
        print('File Not Found')
        return -1
    requirements = Requirements()
    group_data = requirements.prepare_audit(read_data)
    creds = requirements.check_credits()
    gpa = requirements.calc_gpa()
    j2_env = Environment(loader=FileSystemLoader('Degree_Audit/templates'),
                         trim_blocks=True)
    template = j2_env.get_template('audit.html')
    o = template.render(group_data=group_data, creds=creds, gpa=gpa, index=len(group_data))
    with open('Output.html', 'w', encoding='utf-8') as output:
        output.write(o)
        output.close()
    webbrowser.open(path.join(path.curdir, 'Output.html'), new=2, autoraise=True)
    return output


#if __name__ == '__main__':
#    unittest.main()
