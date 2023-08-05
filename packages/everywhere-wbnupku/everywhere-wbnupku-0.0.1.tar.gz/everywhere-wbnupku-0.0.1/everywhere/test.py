




def test1():
    
    import myobject
    print(myobject.get_counter())
    myobject.set_counter()
    
    print(myobject.get_counter())
    return myobject


def test2(m):
    import myobject
    assert myobject is m
    print(myobject.get_counter())
    myobject.set_counter()

    print(myobject.get_counter())


def main():
   
    test2(test1())
    test1()
    import test3




main()
