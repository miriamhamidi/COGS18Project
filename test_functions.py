def test_PIlist_assembler():   
    """Tests the function that is parsing the proffessor names from input string.
    """
    import functions as s
    
    assert s.make_input_prof_list('') == []
    print(s.make_input_prof_list('teacher1,teacher2,,teacher3,,,'))
    assert s.make_input_prof_list('teacher1,teacher2,,teacher3,,,') == ['teacher1', 'teacher2', '', 'teacher3', '', '']
    assert s.make_input_prof_list('onlyoneteacher') == ['onlyoneteacher']
    assert isinstance (s.make_input_prof_list('typowith1234$%^'),list)
    
def test_object_initializer():   
    """Tests the function that is creating objects for each research group
    """
    import functions as s
    import pandas as pd
    research_groups = s.object_initializer(pd.read_excel('fixed_names1111.xlsx',header=0))
    
    for group in research_groups:
        assert group.name != None
        assert group.pi != None
        assert group.entry != None
        assert group.courses != None
        assert group.description != None
  
    assert len(research_groups) == len(pd.read_excel('fixed_names1111.xlsx',header=0).index)

def test_narrow_by_course():   
    """Tests that filters the research groups by courses
    """
    
    import functions as s
    import pandas as pd
    x=pd.read_excel('fixed_names1111.xlsx',header=0)
    
    grad_eligibility_list = s.make_elig_list('G',x)
    ugrad_eligibility_list = s.make_elig_list('U',x)
               
    assert s.narrow_by_course([],grad_eligibility_list) == []
    assert s.narrow_by_course([],ugrad_eligibility_list) == []
    
    assert len(s.narrow_by_course(['123','005','101','240'],grad_eligibility_list)) == 4
    assert len(s.narrow_by_course(['107'],grad_eligibility_list)) == 2      
               
               
           
           
           
           
           
           
           
           
           
           
           
           
 