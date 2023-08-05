cdef extern from "./ext/add.h":
    int add(int first,int second)

def py_add(first: int,second: int) -> int:
    return add(first,second)