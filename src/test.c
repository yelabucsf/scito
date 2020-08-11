#include <Python.h>
#include "cluster.h"


void fastfactorial(int n, int *res){
    PySys_WriteStdout("LOLO %i", n);
    *res = n + 2;

}


static PyObject* factorial(PyObject *self, PyObject *args){
    int n;
    int res;
    if (!PyArg_ParseTuple(args,"ii", &n, &res))
        return NULL;
    //return Py_BuildValue("i",res);'
    return Py_BuildValue("");
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



