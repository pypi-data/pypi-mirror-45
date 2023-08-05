from cpython.pystate cimport PyGILState_Ensure, PyGILState_Release, PyGILState_STATE


cdef PyGILState_STATE * s = NULL


def lock_gil():
    if s != NULL:
        s[0] = PyGILState_Ensure()


def unlock_gil():
    global s
    if s != NULL:
        s_ = s
        s = NULL;
        PyGILState_Release(s_[0])
