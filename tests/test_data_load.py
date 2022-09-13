from src import data_load
import pandas as pd

def test_readData():
    dataload = data_load.DataLoader()
    dataload.readData("tests/test_data.xlsx")
    assert len(dataload.students) == 20
    assert len(dataload.ward_data) == 5
    assert len(dataload.uni_placements) == 60

def test_cohort_generation():
    dataload = data_load.DataLoader()
    cohort_df = pd.DataFrame(
        {
            'uni_col':['uni'],
            'qual_col':['qual'],
            'start_col':['start']
        })
    cohort_df = dataload.createCohort(cohort_df,'student_cohort','uni_col','qual_col','start_col')
    assert cohort_df['student_cohort'][0] == 'uni_qual start'

def test_relative_date_calc():
    dataload = data_load.DataLoader()
    date_df = pd.DataFrame(
        {
            'start_date':['01/01/2020'],
            'end_date':['15/01/2020']
        })
    date_df = dataload.calcRelDateWeeks(date_df,date_df,'weeks_diff','end_date','start_date')
    assert date_df['weeks_diff'][0] == 2

def test_relative_date_calc_negative_diff():
    dataload = data_load.DataLoader()
    date_df = pd.DataFrame(
        {
            'start_date':['15/01/2020'],
            'end_date':['01/01/2020']
        })
    date_df = dataload.calcRelDateWeeks(date_df,date_df,'weeks_diff','end_date','start_date')
    assert date_df['weeks_diff'][0] == -2


def test_placement_cleaning():
    dataload = data_load.DataLoader()
    dataload.students = pd.DataFrame({
        'prev_placements':["ward1,ward2,'ward3',ward4"],
        'allprevwards':['']
    })
    dataload.cleanPrevPlacements()
    print(dataload.students["allprevwards"])
    assert len(dataload.students["allprevwards"][0]) == len(['ward1','ward2','ward3','ward4'])
    assert all([a == b for a, b in zip(dataload.students["allprevwards"][0], ['ward1','ward2','ward3','ward4'])])

def test_cleanStudentPlacementCohorts():
    dataload = data_load.DataLoader()
    cohort_df = pd.DataFrame(
        {
            'university':['uni'],
            'qualification':['qual'],
            'course_start':['start']
        })
    dataload.students = cohort_df
    dataload.uni_placements = cohort_df
    dataload.cleanStudentPlacementCohorts()

    assert dataload.students['student_cohort'][0] == 'uni_qual start'
    assert dataload.uni_placements['student_cohort'][0] == 'uni_qual start'

def test_cleanWardAuditExp():
    dataload = data_load.DataLoader()
    dataload.ward_data = pd.DataFrame(
        {
            'education_audit_exp':['2020/01/15']
        })
    dataload.uni_placements = pd.DataFrame(
        {
            'placement_start_date':['2020/01/01','2020/02/30','2019/09/15'],
        })
    dataload.calcWardAuditExp()
    assert dataload.ward_data['education_audit_exp_week'][0] == 17