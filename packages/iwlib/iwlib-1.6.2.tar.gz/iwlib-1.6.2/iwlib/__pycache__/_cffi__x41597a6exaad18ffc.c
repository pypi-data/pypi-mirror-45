
#include <Python.h>
#include <stddef.h>

/* this block of #ifs should be kept exactly identical between
   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py
   and cffi/_cffi_include.h */
#if defined(_MSC_VER)
# include <malloc.h>   /* for alloca() */
# if _MSC_VER < 1600   /* MSVC < 2010 */
   typedef __int8 int8_t;
   typedef __int16 int16_t;
   typedef __int32 int32_t;
   typedef __int64 int64_t;
   typedef unsigned __int8 uint8_t;
   typedef unsigned __int16 uint16_t;
   typedef unsigned __int32 uint32_t;
   typedef unsigned __int64 uint64_t;
   typedef __int8 int_least8_t;
   typedef __int16 int_least16_t;
   typedef __int32 int_least32_t;
   typedef __int64 int_least64_t;
   typedef unsigned __int8 uint_least8_t;
   typedef unsigned __int16 uint_least16_t;
   typedef unsigned __int32 uint_least32_t;
   typedef unsigned __int64 uint_least64_t;
   typedef __int8 int_fast8_t;
   typedef __int16 int_fast16_t;
   typedef __int32 int_fast32_t;
   typedef __int64 int_fast64_t;
   typedef unsigned __int8 uint_fast8_t;
   typedef unsigned __int16 uint_fast16_t;
   typedef unsigned __int32 uint_fast32_t;
   typedef unsigned __int64 uint_fast64_t;
   typedef __int64 intmax_t;
   typedef unsigned __int64 uintmax_t;
# else
#  include <stdint.h>
# endif
# if _MSC_VER < 1800   /* MSVC < 2013 */
#  ifndef __cplusplus
    typedef unsigned char _Bool;
#  endif
# endif
#else
# include <stdint.h>
# if (defined (__SVR4) && defined (__sun)) || defined(_AIX) || defined(__hpux)
#  include <alloca.h>
# endif
#endif

#if PY_MAJOR_VERSION < 3
# undef PyCapsule_CheckExact
# undef PyCapsule_GetPointer
# define PyCapsule_CheckExact(capsule) (PyCObject_Check(capsule))
# define PyCapsule_GetPointer(capsule, name) \
    (PyCObject_AsVoidPtr(capsule))
#endif

#if PY_MAJOR_VERSION >= 3
# define PyInt_FromLong PyLong_FromLong
#endif

#define _cffi_from_c_double PyFloat_FromDouble
#define _cffi_from_c_float PyFloat_FromDouble
#define _cffi_from_c_long PyInt_FromLong
#define _cffi_from_c_ulong PyLong_FromUnsignedLong
#define _cffi_from_c_longlong PyLong_FromLongLong
#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong
#define _cffi_from_c__Bool PyBool_FromLong

#define _cffi_to_c_double PyFloat_AsDouble
#define _cffi_to_c_float PyFloat_AsDouble

#define _cffi_from_c_int_const(x)                                        \
    (((x) > 0) ?                                                         \
        ((unsigned long long)(x) <= (unsigned long long)LONG_MAX) ?      \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromUnsignedLongLong((unsigned long long)(x)) :       \
        ((long long)(x) >= (long long)LONG_MIN) ?                        \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromLongLong((long long)(x)))

#define _cffi_from_c_int(x, type)                                        \
    (((type)-1) > 0 ? /* unsigned */                                     \
        (sizeof(type) < sizeof(long) ?                                   \
            PyInt_FromLong((long)x) :                                    \
         sizeof(type) == sizeof(long) ?                                  \
            PyLong_FromUnsignedLong((unsigned long)x) :                  \
            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \
        (sizeof(type) <= sizeof(long) ?                                  \
            PyInt_FromLong((long)x) :                                    \
            PyLong_FromLongLong((long long)x)))

#define _cffi_to_c_int(o, type)                                          \
    ((type)(                                                             \
     sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \
                                         : (type)_cffi_to_c_i8(o)) :     \
     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \
                                         : (type)_cffi_to_c_i16(o)) :    \
     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \
                                         : (type)_cffi_to_c_i32(o)) :    \
     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \
                                         : (type)_cffi_to_c_i64(o)) :    \
     (Py_FatalError("unsupported size for type " #type), (type)0)))

#define _cffi_to_c_i8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[1])
#define _cffi_to_c_u8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[2])
#define _cffi_to_c_i16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[3])
#define _cffi_to_c_u16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[4])
#define _cffi_to_c_i32                                                   \
                 ((int(*)(PyObject *))_cffi_exports[5])
#define _cffi_to_c_u32                                                   \
                 ((unsigned int(*)(PyObject *))_cffi_exports[6])
#define _cffi_to_c_i64                                                   \
                 ((long long(*)(PyObject *))_cffi_exports[7])
#define _cffi_to_c_u64                                                   \
                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])
#define _cffi_to_c_char                                                  \
                 ((int(*)(PyObject *))_cffi_exports[9])
#define _cffi_from_c_pointer                                             \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])
#define _cffi_to_c_pointer                                               \
    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])
#define _cffi_get_struct_layout                                          \
    ((PyObject *(*)(Py_ssize_t[]))_cffi_exports[12])
#define _cffi_restore_errno                                              \
    ((void(*)(void))_cffi_exports[13])
#define _cffi_save_errno                                                 \
    ((void(*)(void))_cffi_exports[14])
#define _cffi_from_c_char                                                \
    ((PyObject *(*)(char))_cffi_exports[15])
#define _cffi_from_c_deref                                               \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])
#define _cffi_to_c                                                       \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])
#define _cffi_from_c_struct                                              \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])
#define _cffi_to_c_wchar_t                                               \
    ((wchar_t(*)(PyObject *))_cffi_exports[19])
#define _cffi_from_c_wchar_t                                             \
    ((PyObject *(*)(wchar_t))_cffi_exports[20])
#define _cffi_to_c_long_double                                           \
    ((long double(*)(PyObject *))_cffi_exports[21])
#define _cffi_to_c__Bool                                                 \
    ((_Bool(*)(PyObject *))_cffi_exports[22])
#define _cffi_prepare_pointer_call_argument                              \
    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])
#define _cffi_convert_array_from_object                                  \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])
#define _CFFI_NUM_EXPORTS 25

typedef struct _ctypedescr CTypeDescrObject;

static void *_cffi_exports[_CFFI_NUM_EXPORTS];
static PyObject *_cffi_types, *_cffi_VerificationError;

static int _cffi_setup_custom(PyObject *lib);   /* forward */

static PyObject *_cffi_setup(PyObject *self, PyObject *args)
{
    PyObject *library;
    int was_alive = (_cffi_types != NULL);
    (void)self; /* unused */
    if (!PyArg_ParseTuple(args, "OOO", &_cffi_types, &_cffi_VerificationError,
                                       &library))
        return NULL;
    Py_INCREF(_cffi_types);
    Py_INCREF(_cffi_VerificationError);
    if (_cffi_setup_custom(library) < 0)
        return NULL;
    return PyBool_FromLong(was_alive);
}

static int _cffi_init(void)
{
    PyObject *module, *c_api_object = NULL;

    module = PyImport_ImportModule("_cffi_backend");
    if (module == NULL)
        goto failure;

    c_api_object = PyObject_GetAttrString(module, "_C_API");
    if (c_api_object == NULL)
        goto failure;
    if (!PyCapsule_CheckExact(c_api_object)) {
        PyErr_SetNone(PyExc_ImportError);
        goto failure;
    }
    memcpy(_cffi_exports, PyCapsule_GetPointer(c_api_object, "cffi"),
           _CFFI_NUM_EXPORTS * sizeof(void *));

    Py_DECREF(module);
    Py_DECREF(c_api_object);
    return 0;

  failure:
    Py_XDECREF(module);
    Py_XDECREF(c_api_object);
    return -1;
}

#define _cffi_type(num) ((CTypeDescrObject *)PyList_GET_ITEM(_cffi_types, num))

/**********/


#include <iwlib.h>

static int _cffi_const_ioctl(PyObject *lib)
{
  PyObject *o;
  int res;
  int(* i)(int, unsigned long, ...);
  i = (ioctl);
  o = _cffi_from_c_pointer((char *)i, _cffi_type(0));
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "ioctl", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return ((void)lib,0);
}

static PyObject *
_cffi_f_iw_ether_ntop(PyObject *self, PyObject *args)
{
  struct ether_addr const * x0;
  char * x1;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:iw_ether_ntop", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { iw_ether_ntop(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_iw_freq2float(PyObject *self, PyObject *arg0)
{
  iwfreq const * x0;
  Py_ssize_t datasize;
  double result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(4), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = iw_freq2float(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_double(result);
}

static PyObject *
_cffi_f_iw_get_ext(PyObject *self, PyObject *args)
{
  int x0;
  char * x1;
  int x2;
  struct iwreq * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:iw_get_ext", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca((size_t)datasize);
    memset((void *)x3, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(5), arg3) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = iw_get_ext(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_iw_get_kernel_we_version(PyObject *self, PyObject *noarg)
{
  int result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = iw_get_kernel_we_version(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_iw_get_range_info(PyObject *self, PyObject *args)
{
  int x0;
  char const * x1;
  iwrange * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:iw_get_range_info", &arg0, &arg1, &arg2))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(6), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(6), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(7), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca((size_t)datasize);
    memset((void *)x2, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(7), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = iw_get_range_info(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_iw_get_stats(PyObject *self, PyObject *args)
{
  int x0;
  char const * x1;
  iwstats * x2;
  iwrange * x3;
  int x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:iw_get_stats", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(6), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(6), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca((size_t)datasize);
    memset((void *)x2, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(8), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(7), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca((size_t)datasize);
    memset((void *)x3, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(7), arg3) < 0)
      return NULL;
  }

  x4 = _cffi_to_c_int(arg4, int);
  if (x4 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = iw_get_stats(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_iw_print_bitrate(PyObject *self, PyObject *args)
{
  char * x0;
  int x1;
  int x2;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:iw_print_bitrate", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(2), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { iw_print_bitrate(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_iw_print_freq_value(PyObject *self, PyObject *args)
{
  char * x0;
  int x1;
  double x2;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:iw_print_freq_value", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(2), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  x2 = (double)_cffi_to_c_double(arg2);
  if (x2 == (double)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { iw_print_freq_value(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_iw_scan(PyObject *self, PyObject *args)
{
  int x0;
  char * x1;
  int x2;
  wireless_scan_head * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:iw_scan", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca((size_t)datasize);
    memset((void *)x3, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(9), arg3) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = iw_scan(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_iw_set_ext(PyObject *self, PyObject *args)
{
  int x0;
  char * x1;
  int x2;
  struct iwreq * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:iw_set_ext", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca((size_t)datasize);
    memset((void *)x3, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(5), arg3) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = iw_set_ext(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_iw_sockets_close(PyObject *self, PyObject *arg0)
{
  int x0;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { iw_sockets_close(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_iw_sockets_open(PyObject *self, PyObject *noarg)
{
  int result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = iw_sockets_open(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_int(result, int);
}

static int _cffi_const_IFNAMSIZ(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IFNAMSIZ);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IFNAMSIZ", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_ioctl(lib);
}

static int _cffi_const_IW_ENCODE_DISABLED(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_ENCODE_DISABLED);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_ENCODE_DISABLED", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IFNAMSIZ(lib);
}

static int _cffi_const_IW_ENCODING_TOKEN_MAX(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_ENCODING_TOKEN_MAX);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_ENCODING_TOKEN_MAX", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_ENCODE_DISABLED(lib);
}

static int _cffi_const_IW_ESSID_MAX_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_ESSID_MAX_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_ESSID_MAX_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_ENCODING_TOKEN_MAX(lib);
}

static int _cffi_const_IW_MODE_ADHOC(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_MODE_ADHOC);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_MODE_ADHOC", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_ESSID_MAX_SIZE(lib);
}

static int _cffi_const_IW_MODE_AUTO(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_MODE_AUTO);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_MODE_AUTO", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_MODE_ADHOC(lib);
}

static int _cffi_const_IW_MODE_INFRA(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_MODE_INFRA);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_MODE_INFRA", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_MODE_AUTO(lib);
}

static int _cffi_const_IW_MODE_MASTER(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_MODE_MASTER);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_MODE_MASTER", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_MODE_INFRA(lib);
}

static int _cffi_const_IW_MODE_MONITOR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_MODE_MONITOR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_MODE_MONITOR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_MODE_MASTER(lib);
}

static int _cffi_const_IW_MODE_REPEAT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_MODE_REPEAT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_MODE_REPEAT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_MODE_MONITOR(lib);
}

static int _cffi_const_IW_MODE_SECOND(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_MODE_SECOND);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_MODE_SECOND", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_MODE_REPEAT(lib);
}

static int _cffi_const_IW_NUM_OPER_MODE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(IW_NUM_OPER_MODE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "IW_NUM_OPER_MODE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_MODE_SECOND(lib);
}

static int _cffi_const_SIOCGIFFLAGS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIFFLAGS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIFFLAGS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_IW_NUM_OPER_MODE(lib);
}

static int _cffi_const_SIOCGIWAP(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWAP);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWAP", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIFFLAGS(lib);
}

static int _cffi_const_SIOCGIWAPLIST(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWAPLIST);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWAPLIST", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWAP(lib);
}

static int _cffi_const_SIOCGIWAUTH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWAUTH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWAUTH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWAPLIST(lib);
}

static int _cffi_const_SIOCGIWENCODE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWENCODE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWENCODE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWAUTH(lib);
}

static int _cffi_const_SIOCGIWENCODEEXT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWENCODEEXT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWENCODEEXT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWENCODE(lib);
}

static int _cffi_const_SIOCGIWESSID(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWESSID);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWESSID", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWENCODEEXT(lib);
}

static int _cffi_const_SIOCGIWFRAG(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWFRAG);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWFRAG", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWESSID(lib);
}

static int _cffi_const_SIOCGIWFREQ(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWFREQ);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWFREQ", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWFRAG(lib);
}

static int _cffi_const_SIOCGIWGENIE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWGENIE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWGENIE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWFREQ(lib);
}

static int _cffi_const_SIOCGIWMODE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWMODE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWMODE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWGENIE(lib);
}

static int _cffi_const_SIOCGIWMODUL(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWMODUL);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWMODUL", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWMODE(lib);
}

static int _cffi_const_SIOCGIWNAME(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWNAME);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWNAME", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWMODUL(lib);
}

static int _cffi_const_SIOCGIWNICKN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWNICKN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWNICKN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWNAME(lib);
}

static int _cffi_const_SIOCGIWNWID(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWNWID);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWNWID", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWNICKN(lib);
}

static int _cffi_const_SIOCGIWPOWER(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWPOWER);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWPOWER", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWNWID(lib);
}

static int _cffi_const_SIOCGIWPRIV(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWPRIV);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWPRIV", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWPOWER(lib);
}

static int _cffi_const_SIOCGIWRANGE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWRANGE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWRANGE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWPRIV(lib);
}

static int _cffi_const_SIOCGIWRATE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWRATE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWRATE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWRANGE(lib);
}

static int _cffi_const_SIOCGIWRETRY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWRETRY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWRETRY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWRATE(lib);
}

static int _cffi_const_SIOCGIWRTS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWRTS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWRTS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWRETRY(lib);
}

static int _cffi_const_SIOCGIWSCAN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWSCAN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWSCAN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWRTS(lib);
}

static int _cffi_const_SIOCGIWSENS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWSENS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWSENS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWSCAN(lib);
}

static int _cffi_const_SIOCGIWSPY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWSPY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWSPY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWSENS(lib);
}

static int _cffi_const_SIOCGIWSTATS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWSTATS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWSTATS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWSPY(lib);
}

static int _cffi_const_SIOCGIWTHRSPY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWTHRSPY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWTHRSPY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWSTATS(lib);
}

static int _cffi_const_SIOCGIWTXPOW(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCGIWTXPOW);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCGIWTXPOW", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWTHRSPY(lib);
}

static int _cffi_const_SIOCIWFIRSTPRIV(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCIWFIRSTPRIV);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCIWFIRSTPRIV", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCGIWTXPOW(lib);
}

static int _cffi_const_SIOCIWLASTPRIV(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCIWLASTPRIV);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCIWLASTPRIV", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCIWFIRSTPRIV(lib);
}

static int _cffi_const_SIOCSIWAP(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWAP);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWAP", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCIWLASTPRIV(lib);
}

static int _cffi_const_SIOCSIWAUTH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWAUTH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWAUTH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWAP(lib);
}

static int _cffi_const_SIOCSIWCOMMIT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWCOMMIT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWCOMMIT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWAUTH(lib);
}

static int _cffi_const_SIOCSIWENCODE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWENCODE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWENCODE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWCOMMIT(lib);
}

static int _cffi_const_SIOCSIWENCODEEXT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWENCODEEXT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWENCODEEXT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWENCODE(lib);
}

static int _cffi_const_SIOCSIWESSID(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWESSID);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWESSID", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWENCODEEXT(lib);
}

static int _cffi_const_SIOCSIWFRAG(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWFRAG);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWFRAG", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWESSID(lib);
}

static int _cffi_const_SIOCSIWFREQ(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWFREQ);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWFREQ", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWFRAG(lib);
}

static int _cffi_const_SIOCSIWGENIE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWGENIE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWGENIE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWFREQ(lib);
}

static int _cffi_const_SIOCSIWMLME(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWMLME);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWMLME", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWGENIE(lib);
}

static int _cffi_const_SIOCSIWMODE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWMODE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWMODE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWMLME(lib);
}

static int _cffi_const_SIOCSIWMODUL(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWMODUL);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWMODUL", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWMODE(lib);
}

static int _cffi_const_SIOCSIWNICKN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWNICKN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWNICKN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWMODUL(lib);
}

static int _cffi_const_SIOCSIWNWID(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWNWID);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWNWID", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWNICKN(lib);
}

static int _cffi_const_SIOCSIWPMKSA(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWPMKSA);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWPMKSA", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWNWID(lib);
}

static int _cffi_const_SIOCSIWPOWER(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWPOWER);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWPOWER", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWPMKSA(lib);
}

static int _cffi_const_SIOCSIWPRIV(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWPRIV);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWPRIV", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWPOWER(lib);
}

static int _cffi_const_SIOCSIWRANGE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWRANGE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWRANGE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWPRIV(lib);
}

static int _cffi_const_SIOCSIWRATE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWRATE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWRATE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWRANGE(lib);
}

static int _cffi_const_SIOCSIWRETRY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWRETRY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWRETRY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWRATE(lib);
}

static int _cffi_const_SIOCSIWRTS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWRTS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWRTS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWRETRY(lib);
}

static int _cffi_const_SIOCSIWSCAN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWSCAN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWSCAN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWRTS(lib);
}

static int _cffi_const_SIOCSIWSENS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWSENS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWSENS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWSCAN(lib);
}

static int _cffi_const_SIOCSIWSPY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWSPY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWSPY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWSENS(lib);
}

static int _cffi_const_SIOCSIWSTATS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWSTATS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWSTATS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWSPY(lib);
}

static int _cffi_const_SIOCSIWTHRSPY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWTHRSPY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWTHRSPY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWSTATS(lib);
}

static int _cffi_const_SIOCSIWTXPOW(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(SIOCSIWTXPOW);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "SIOCSIWTXPOW", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWTHRSPY(lib);
}

static void _cffi_check_struct_iw_freq(struct iw_freq *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->m) << 1);
  (void)((p->e) << 1);
  (void)((p->i) << 1);
  (void)((p->flags) << 1);
}
static PyObject *
_cffi_layout_struct_iw_freq(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct iw_freq y; };
  static Py_ssize_t nums[] = {
    sizeof(struct iw_freq),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct iw_freq, m),
    sizeof(((struct iw_freq *)0)->m),
    offsetof(struct iw_freq, e),
    sizeof(((struct iw_freq *)0)->e),
    offsetof(struct iw_freq, i),
    sizeof(((struct iw_freq *)0)->i),
    offsetof(struct iw_freq, flags),
    sizeof(((struct iw_freq *)0)->flags),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_iw_freq(0);
}

static void _cffi_check_struct_iw_param(struct iw_param *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->value) << 1);
  (void)((p->disabled) << 1);
}
static PyObject *
_cffi_layout_struct_iw_param(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct iw_param y; };
  static Py_ssize_t nums[] = {
    sizeof(struct iw_param),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct iw_param, value),
    sizeof(((struct iw_param *)0)->value),
    offsetof(struct iw_param, disabled),
    sizeof(((struct iw_param *)0)->disabled),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_iw_param(0);
}

static void _cffi_check_struct_iw_point(struct iw_point *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { void * *tmp = &p->pointer; (void)tmp; }
  (void)((p->length) << 1);
  (void)((p->flags) << 1);
}
static PyObject *
_cffi_layout_struct_iw_point(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct iw_point y; };
  static Py_ssize_t nums[] = {
    sizeof(struct iw_point),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct iw_point, pointer),
    sizeof(((struct iw_point *)0)->pointer),
    offsetof(struct iw_point, length),
    sizeof(((struct iw_point *)0)->length),
    offsetof(struct iw_point, flags),
    sizeof(((struct iw_point *)0)->flags),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_iw_point(0);
}

static void _cffi_check_struct_iw_quality(struct iw_quality *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->qual) << 1);
  (void)((p->level) << 1);
  (void)((p->noise) << 1);
  (void)((p->updated) << 1);
}
static PyObject *
_cffi_layout_struct_iw_quality(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct iw_quality y; };
  static Py_ssize_t nums[] = {
    sizeof(struct iw_quality),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct iw_quality, qual),
    sizeof(((struct iw_quality *)0)->qual),
    offsetof(struct iw_quality, level),
    sizeof(((struct iw_quality *)0)->level),
    offsetof(struct iw_quality, noise),
    sizeof(((struct iw_quality *)0)->noise),
    offsetof(struct iw_quality, updated),
    sizeof(((struct iw_quality *)0)->updated),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_iw_quality(0);
}

static void _cffi_check_struct_iw_range(struct iw_range *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->we_version_compiled) << 1);
  { struct iw_quality *tmp = &p->max_qual; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_iw_range(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct iw_range y; };
  static Py_ssize_t nums[] = {
    sizeof(struct iw_range),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct iw_range, we_version_compiled),
    sizeof(((struct iw_range *)0)->we_version_compiled),
    offsetof(struct iw_range, max_qual),
    sizeof(((struct iw_range *)0)->max_qual),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_iw_range(0);
}

static void _cffi_check_struct_iw_statistics(struct iw_statistics *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { struct iw_quality *tmp = &p->qual; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_iw_statistics(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct iw_statistics y; };
  static Py_ssize_t nums[] = {
    sizeof(struct iw_statistics),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct iw_statistics, qual),
    sizeof(((struct iw_statistics *)0)->qual),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_iw_statistics(0);
}

static void _cffi_check_struct_iwreq(struct iwreq *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { union iwreq_data *tmp = &p->u; (void)tmp; }
  { char(*tmp)[/*...*/] = &p->ifr_name; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_iwreq(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct iwreq y; };
  static Py_ssize_t nums[] = {
    sizeof(struct iwreq),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct iwreq, u),
    sizeof(((struct iwreq *)0)->u),
    offsetof(struct iwreq, ifr_name),
    sizeof(((struct iwreq *)0)->ifr_name),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_iwreq(0);
}

static void _cffi_check_struct_sockaddr(struct sockaddr *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { char(*tmp)[14] = &p->sa_data; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_sockaddr(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct sockaddr y; };
  static Py_ssize_t nums[] = {
    sizeof(struct sockaddr),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct sockaddr, sa_data),
    sizeof(((struct sockaddr *)0)->sa_data),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_sockaddr(0);
}

static void _cffi_check_struct_wireless_config(struct wireless_config *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->has_mode) << 1);
  (void)((p->mode) << 1);
  (void)((p->essid_on) << 1);
  { char(*tmp)[] = &p->essid; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_wireless_config(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct wireless_config y; };
  static Py_ssize_t nums[] = {
    sizeof(struct wireless_config),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct wireless_config, has_mode),
    sizeof(((struct wireless_config *)0)->has_mode),
    offsetof(struct wireless_config, mode),
    sizeof(((struct wireless_config *)0)->mode),
    offsetof(struct wireless_config, essid_on),
    sizeof(((struct wireless_config *)0)->essid_on),
    offsetof(struct wireless_config, essid),
    0,  /* char[] */
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_wireless_config(0);
}

static void _cffi_check_struct_wireless_scan(struct wireless_scan *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { wireless_scan * *tmp = &p->next; (void)tmp; }
  (void)((p->has_ap_addr) << 1);
  (void)((p->has_stats) << 1);
  (void)((p->has_maxbitrate) << 1);
  { iwparam *tmp = &p->maxbitrate; (void)tmp; }
  { iwstats *tmp = &p->stats; (void)tmp; }
  { struct wireless_config *tmp = &p->b; (void)tmp; }
  { sockaddr *tmp = &p->ap_addr; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_wireless_scan(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct wireless_scan y; };
  static Py_ssize_t nums[] = {
    sizeof(struct wireless_scan),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct wireless_scan, next),
    sizeof(((struct wireless_scan *)0)->next),
    offsetof(struct wireless_scan, has_ap_addr),
    sizeof(((struct wireless_scan *)0)->has_ap_addr),
    offsetof(struct wireless_scan, has_stats),
    sizeof(((struct wireless_scan *)0)->has_stats),
    offsetof(struct wireless_scan, has_maxbitrate),
    sizeof(((struct wireless_scan *)0)->has_maxbitrate),
    offsetof(struct wireless_scan, maxbitrate),
    sizeof(((struct wireless_scan *)0)->maxbitrate),
    offsetof(struct wireless_scan, stats),
    sizeof(((struct wireless_scan *)0)->stats),
    offsetof(struct wireless_scan, b),
    sizeof(((struct wireless_scan *)0)->b),
    offsetof(struct wireless_scan, ap_addr),
    sizeof(((struct wireless_scan *)0)->ap_addr),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_wireless_scan(0);
}

static void _cffi_check_struct_wireless_scan_head(struct wireless_scan_head *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { wireless_scan * *tmp = &p->result; (void)tmp; }
  (void)((p->retry) << 1);
}
static PyObject *
_cffi_layout_struct_wireless_scan_head(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct wireless_scan_head y; };
  static Py_ssize_t nums[] = {
    sizeof(struct wireless_scan_head),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct wireless_scan_head, result),
    sizeof(((struct wireless_scan_head *)0)->result),
    offsetof(struct wireless_scan_head, retry),
    sizeof(((struct wireless_scan_head *)0)->retry),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_wireless_scan_head(0);
}

static void _cffi_check_union_iwreq_data(union iwreq_data *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { struct iw_point *tmp = &p->essid; (void)tmp; }
  { struct iw_point *tmp = &p->data; (void)tmp; }
  { iwfreq *tmp = &p->freq; (void)tmp; }
  { sockaddr *tmp = &p->ap_addr; (void)tmp; }
  (void)((p->mode) << 1);
  { iwparam *tmp = &p->bitrate; (void)tmp; }
  { iwparam *tmp = &p->power; (void)tmp; }
  { iwparam *tmp = &p->nwid; (void)tmp; }
}
static PyObject *
_cffi_layout_union_iwreq_data(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; union iwreq_data y; };
  static Py_ssize_t nums[] = {
    sizeof(union iwreq_data),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(union iwreq_data, essid),
    sizeof(((union iwreq_data *)0)->essid),
    offsetof(union iwreq_data, data),
    sizeof(((union iwreq_data *)0)->data),
    offsetof(union iwreq_data, freq),
    sizeof(((union iwreq_data *)0)->freq),
    offsetof(union iwreq_data, ap_addr),
    sizeof(((union iwreq_data *)0)->ap_addr),
    offsetof(union iwreq_data, mode),
    sizeof(((union iwreq_data *)0)->mode),
    offsetof(union iwreq_data, bitrate),
    sizeof(((union iwreq_data *)0)->bitrate),
    offsetof(union iwreq_data, power),
    sizeof(((union iwreq_data *)0)->power),
    offsetof(union iwreq_data, nwid),
    sizeof(((union iwreq_data *)0)->nwid),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_union_iwreq_data(0);
}

static int _cffi_const_iw_operation_mode(PyObject *lib)
{
  PyObject *o;
  int res;
  char const * * i;
  i = (iw_operation_mode);
  o = _cffi_from_c_pointer((char *)i, _cffi_type(10));
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "iw_operation_mode", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_SIOCSIWTXPOW(lib);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_const_iw_operation_mode(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"iw_ether_ntop", _cffi_f_iw_ether_ntop, METH_VARARGS, NULL},
  {"iw_freq2float", _cffi_f_iw_freq2float, METH_O, NULL},
  {"iw_get_ext", _cffi_f_iw_get_ext, METH_VARARGS, NULL},
  {"iw_get_kernel_we_version", _cffi_f_iw_get_kernel_we_version, METH_NOARGS, NULL},
  {"iw_get_range_info", _cffi_f_iw_get_range_info, METH_VARARGS, NULL},
  {"iw_get_stats", _cffi_f_iw_get_stats, METH_VARARGS, NULL},
  {"iw_print_bitrate", _cffi_f_iw_print_bitrate, METH_VARARGS, NULL},
  {"iw_print_freq_value", _cffi_f_iw_print_freq_value, METH_VARARGS, NULL},
  {"iw_scan", _cffi_f_iw_scan, METH_VARARGS, NULL},
  {"iw_set_ext", _cffi_f_iw_set_ext, METH_VARARGS, NULL},
  {"iw_sockets_close", _cffi_f_iw_sockets_close, METH_O, NULL},
  {"iw_sockets_open", _cffi_f_iw_sockets_open, METH_NOARGS, NULL},
  {"_cffi_layout_struct_iw_freq", _cffi_layout_struct_iw_freq, METH_NOARGS, NULL},
  {"_cffi_layout_struct_iw_param", _cffi_layout_struct_iw_param, METH_NOARGS, NULL},
  {"_cffi_layout_struct_iw_point", _cffi_layout_struct_iw_point, METH_NOARGS, NULL},
  {"_cffi_layout_struct_iw_quality", _cffi_layout_struct_iw_quality, METH_NOARGS, NULL},
  {"_cffi_layout_struct_iw_range", _cffi_layout_struct_iw_range, METH_NOARGS, NULL},
  {"_cffi_layout_struct_iw_statistics", _cffi_layout_struct_iw_statistics, METH_NOARGS, NULL},
  {"_cffi_layout_struct_iwreq", _cffi_layout_struct_iwreq, METH_NOARGS, NULL},
  {"_cffi_layout_struct_sockaddr", _cffi_layout_struct_sockaddr, METH_NOARGS, NULL},
  {"_cffi_layout_struct_wireless_config", _cffi_layout_struct_wireless_config, METH_NOARGS, NULL},
  {"_cffi_layout_struct_wireless_scan", _cffi_layout_struct_wireless_scan, METH_NOARGS, NULL},
  {"_cffi_layout_struct_wireless_scan_head", _cffi_layout_struct_wireless_scan_head, METH_NOARGS, NULL},
  {"_cffi_layout_union_iwreq_data", _cffi_layout_union_iwreq_data, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__x41597a6exaad18ffc",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__x41597a6exaad18ffc(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (((void)lib,0) < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init_cffi__x41597a6exaad18ffc(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__x41597a6exaad18ffc", _cffi_methods);
  if (lib == NULL)
    return;
  if (((void)lib,0) < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
