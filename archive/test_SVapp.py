from SVapp import graham_value
from SVapp import parameters

#------------------------------------------------- 
def test_graham_value():
    assert graham_value(None,1) is  None
    assert graham_value(1,None) is  None 
    assert graham_value(-1,1) is  None
    assert graham_value(1,-1) is  None
    assert graham_value(5,10) == 33.54

#-------------------------------------------------     
def test_parameters():
    session = None
    assert parameters('LNR.TO',session) is not None
    assert parameters('qwerty.TO',session) is None

#-------------------------------------------------   

if __name__ =="__main__" :
    try:
        test_graham_value()
        print('Function test_graham_value: ALL tests passed successfully!')
    except Exception as e:
        print('Error in test_graham_value:', {e})
    
    try:
        test_parameters()
        print('Function test_parameters: ALL tests passed successfully!')
    except Exception as e:
        print('Error in test_parameters:', {e})