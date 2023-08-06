#include <x11_client.h>

static PyObject* x11_client_send_key(PyObject *self, PyObject *args)
{
    int keycode;

    if (!PyArg_ParseTuple(args, "i", &keycode))
        return NULL;

    XTestFakeKeyEvent(display, keycode, 1, 0);
    XTestFakeKeyEvent(display, keycode, 0, 0);
    XSync(display, 1);

    return PyLong_FromLong(keycode);
}

static PyObject* x11_client_type(PyObject *self, PyObject *args)
{
    const char *button;

    if (!PyArg_ParseTuple(args, "s", &button))
        return NULL;

    KeySym sym = XStringToKeysym(button);
    KeyCode keycode = XKeysymToKeycode(display, sym);

    XTestFakeKeyEvent(display, keycode, 1, 0);
    XTestFakeKeyEvent(display, keycode, 0, 0);
    XSync(display, 1);

    return PyLong_FromLong(keycode);
}

static PyObject* x11_client_composed_type(PyObject *self, PyObject *args)
{
    int key;
    const char *button;

    if (!PyArg_ParseTuple(args, "is", &key, &button))
        return NULL;

    KeySym sym = XStringToKeysym(button);
    KeyCode keycode = XKeysymToKeycode(display, sym);

    XTestFakeKeyEvent(display, key, 1, 0);

    XTestFakeKeyEvent(display, keycode, 1, 0);
    XTestFakeKeyEvent(display, keycode, 0, 0);

    XTestFakeKeyEvent(display, key, 0, 0);

    XSync(display, 1);

    return PyLong_FromLong(keycode);
}

static PyMethodDef X11ClientMethods[] = {
    {"send_key",  x11_client_send_key, METH_VARARGS, "send key"},
    {"type",  x11_client_type, METH_VARARGS, "type a key"},
    {"composed_type",  x11_client_composed_type, METH_VARARGS, "composed type"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef x11_clientmodule = {
    PyModuleDef_HEAD_INIT,
    "x11_client",
    NULL,
    -1,
    X11ClientMethods
};

PyMODINIT_FUNC PyInit_x11_client(void)
{
    display = XOpenDisplay("");

    PyObject *m;
    m = PyModule_Create(&x11_clientmodule);
    if (m == NULL)
        return NULL;

    return m;
}
