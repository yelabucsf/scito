#include <Python.h>
#include "cluster.h"


int fastfactorial(int n, int diss_kind){

    if (diss_kind == MANHATTAN)
        PySys_WriteStdout("LOL");
    if(n<=1)
        return 1;
    else
        return n * fastfactorial(n-1, 1);
}


static PyObject* factorial(PyObject *self, PyObject *args){
    int n;
    DISS_KIND diss_kind;
    if (!PyArg_ParseTuple(args,"ii",&n, &diss_kind))
        return NULL;
    int result = fastfactorial(n, diss_kind);
    return Py_BuildValue("i",result);
}

static PyMethodDef mainMethods[] = {
        {"factorial",factorial,METH_VARARGS,"Calculate the factorial of n"},
        {NULL,NULL,0,NULL}
};

static PyModuleDef cmath11 = {
        PyModuleDef_HEAD_INIT,
        "cmath11","Factorial Calculation",
        -1,
        mainMethods
};

PyMODINIT_FUNC PyInit_cmath11(void){
    return PyModule_Create(&cmath11);
}



