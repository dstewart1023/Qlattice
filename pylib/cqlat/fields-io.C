#include "lib.h"

namespace qlat
{  //

template <class M>
PyObject* write_sfw_field_ctype(ShuffledFieldsWriter& sfw,
                                const std::string& fn, PyField& pf)
{
  const Field<M>& f = *(Field<M>*)pf.cdata;
  const long ret = write(sfw, fn, f);
  return py_convert(ret);
}

template <class M>
PyObject* read_sfr_field_ctype(ShuffledFieldsReader& sfr, const std::string& fn,
                               PyField& pf)
{
  Field<M>& f = *(Field<M>*)pf.cdata;
  const long ret = read(sfr, fn, f);
  return py_convert(ret);
}

template <class M>
PyObject* write_sfw_sfield_ctype(ShuffledFieldsWriter& sfw,
                                 const std::string& fn, PyField& pf,
                                 const ShuffledBitSet& sbs)
{
  const SelectedField<M>& f = *(SelectedField<M>*)pf.cdata;
  const long ret = write(sfw, fn, f, sbs);
  return py_convert(ret);
}

template <class M>
PyObject* read_sfr_sfield_ctype(ShuffledFieldsReader& sfr,
                                const std::string& fn, PyObject* p_sbs,
                                PyObject* p_sfield, PyObject* p_fsel)
{
  SelectedField<M>& sf = py_convert_type_sfield<M>(p_sfield);
  if (p_sbs != Py_None) {
    pqassert(p_fsel == NULL)
    const ShuffledBitSet& sbs = py_convert_type<ShuffledBitSet>(p_sbs);
    const long ret = read(sfr, fn, sbs, sf);
    return py_convert(ret);
  } else {
    pqassert(p_fsel != NULL)
    FieldSelection& fsel = py_convert_type<FieldSelection>(p_fsel);
    const long ret = read(sfr, fn, sf, fsel);
    return py_convert(ret);
  }
  pqassert(false);
  Py_RETURN_NONE;
}

}  // namespace qlat

EXPORT(mk_sfw, {
  using namespace qlat;
  PyObject* p_path = NULL;
  PyObject* p_new_size_node = NULL;
  bool is_append = false;
  if (!PyArg_ParseTuple(args, "OO|b", &p_path, &p_new_size_node, &is_append)) {
    return NULL;
  }
  std::string path;
  py_convert(path, p_path);
  Coordinate new_size_node;
  py_convert(new_size_node, p_new_size_node);
  ShuffledFieldsWriter* psfw =
      new ShuffledFieldsWriter(path, new_size_node, is_append);
  return py_convert((void*)psfw);
});

EXPORT(free_sfw, {
  using namespace qlat;
  return free_obj<ShuffledFieldsWriter>(args);
});

EXPORT(get_new_size_node_sfw, {
  using namespace qlat;
  PyObject* p_obj = NULL;
  if (!PyArg_ParseTuple(args, "O", &p_obj)) {
    return NULL;
  }
  const ShuffledFieldsWriter& obj =
      py_convert_type<ShuffledFieldsWriter>(p_obj);
  return py_convert(obj.new_size_node);
});

EXPORT(mk_sfr, {
  using namespace qlat;
  PyObject* p_path = NULL;
  PyObject* p_new_size_node = NULL;
  if (!PyArg_ParseTuple(args, "O|O", &p_path, &p_new_size_node)) {
    return NULL;
  }
  std::string path;
  py_convert(path, p_path);
  Coordinate new_size_node;
  if (p_new_size_node != NULL) {
    py_convert(new_size_node, p_new_size_node);
  }
  ShuffledFieldsReader* psfr = new ShuffledFieldsReader(path, new_size_node);
  return py_convert((void*)psfr);
});

EXPORT(free_sfr, {
  using namespace qlat;
  return free_obj<ShuffledFieldsReader>(args);
});

EXPORT(get_new_size_node_sfr, {
  using namespace qlat;
  PyObject* p_obj = NULL;
  if (!PyArg_ParseTuple(args, "O", &p_obj)) {
    return NULL;
  }
  const ShuffledFieldsReader& obj =
      py_convert_type<ShuffledFieldsReader>(p_obj);
  return py_convert(obj.new_size_node);
});

EXPORT(mk_sbs, {
  using namespace qlat;
  PyObject* p_fsel = NULL;
  PyObject* p_new_size_node = NULL;
  if (!PyArg_ParseTuple(args, "OO", &p_fsel, &p_new_size_node)) {
    return NULL;
  }
  const FieldSelection& fsel = py_convert_type<FieldSelection>(p_fsel);
  Coordinate new_size_node;
  py_convert(new_size_node, p_new_size_node);
  ShuffledBitSet* psbs = new ShuffledBitSet();
  *psbs = mk_shuffled_bitset(fsel, new_size_node);
  return py_convert((void*)psbs);
});

EXPORT(free_sbs, {
  using namespace qlat;
  return free_obj<ShuffledBitSet>(args);
});

EXPORT(write_sfw_field, {
  using namespace qlat;
  PyObject* p_sfw = NULL;
  PyObject* p_fn = NULL;
  PyObject* p_field = NULL;
  if (!PyArg_ParseTuple(args, "OOO", &p_sfw, &p_fn, &p_field)) {
    return NULL;
  }
  ShuffledFieldsWriter& sfw = py_convert_type<ShuffledFieldsWriter>(p_sfw);
  PyField pf = py_convert_field(p_field);
  std::string fn;
  py_convert(fn, p_fn);
  PyObject* p_ret = NULL;
  FIELD_DISPATCH(p_ret, write_sfw_field_ctype, pf.ctype, sfw, fn, pf);
  return p_ret;
});

EXPORT(read_sfr_field, {
  using namespace qlat;
  PyObject* p_sfr = NULL;
  PyObject* p_fn = NULL;
  PyObject* p_field = NULL;
  if (!PyArg_ParseTuple(args, "OOO", &p_sfr, &p_fn, &p_field)) {
    return NULL;
  }
  ShuffledFieldsReader& sfr = py_convert_type<ShuffledFieldsReader>(p_sfr);
  PyField pf = py_convert_field(p_field);
  std::string fn;
  py_convert(fn, p_fn);
  PyObject* p_ret = NULL;
  FIELD_DISPATCH(p_ret, read_sfr_field_ctype, pf.ctype, sfr, fn, pf);
  return p_ret;
});

EXPORT(write_sfw_sfield, {
  using namespace qlat;
  PyObject* p_sfw = NULL;
  PyObject* p_fn = NULL;
  PyObject* p_field = NULL;
  PyObject* p_sbs = NULL;
  if (!PyArg_ParseTuple(args, "OOOO", &p_sfw, &p_fn, &p_field, &p_sbs)) {
    return NULL;
  }
  ShuffledFieldsWriter& sfw = py_convert_type<ShuffledFieldsWriter>(p_sfw);
  std::string fn;
  py_convert(fn, p_fn);
  PyField pf = py_convert_field(p_field);
  const ShuffledBitSet& sbs = py_convert_type<ShuffledBitSet>(p_sbs);
  PyObject* p_ret = NULL;
  FIELD_DISPATCH(p_ret, write_sfw_sfield_ctype, pf.ctype, sfw, fn, pf, sbs);
  return p_ret;
});

EXPORT(read_sfr_sfield, {
  using namespace qlat;
  PyObject* p_sfr = NULL;
  PyObject* p_fn = NULL;
  PyObject* p_sbs = NULL;
  PyObject* p_sfield = NULL;
  PyObject* p_fsel = NULL;
  if (!PyArg_ParseTuple(args, "OOOO|O", &p_sfr, &p_fn, &p_sbs, &p_sfield,
                        &p_fsel)) {
    return NULL;
  }
  ShuffledFieldsReader& sfr = py_convert_type<ShuffledFieldsReader>(p_sfr);
  const std::string fn = py_convert_data<std::string>(p_fn);
  const std::string ctype = py_get_ctype(p_sfield);
  PyObject* p_ret = NULL;
  FIELD_DISPATCH(p_ret, read_sfr_sfield_ctype, ctype, sfr, fn, p_sbs, p_sfield,
                 p_fsel);
  return p_ret;
});

EXPORT(list_sfr, {
  using namespace qlat;
  PyObject* p_sfr = NULL;
  if (!PyArg_ParseTuple(args, "O", &p_sfr)) {
    return NULL;
  }
  ShuffledFieldsReader& sfr = py_convert_type<ShuffledFieldsReader>(p_sfr);
  return py_convert(list_fields(sfr));
});

EXPORT(does_file_exist_sync_node_sfr, {
  using namespace qlat;
  PyObject* p_sfr = NULL;
  PyObject* p_fn = NULL;
  if (!PyArg_ParseTuple(args, "OO", &p_sfr, &p_fn)) {
    return NULL;
  }
  ShuffledFieldsReader& sfr = py_convert_type<ShuffledFieldsReader>(p_sfr);
  const std::string fn = py_convert_data<std::string>(p_fn);
  return py_convert(does_file_exist_sync_node(sfr, fn));
});

EXPORT(properly_truncate_fields_sync_node, {
  using namespace qlat;
  PyObject* p_path = NULL;
  bool is_check_all = false;
  bool is_only_check = false;
  PyObject* p_new_size_node = NULL;
  if (!PyArg_ParseTuple(args, "O|bbO", &p_path, &is_check_all, &is_only_check,
                        &p_new_size_node)) {
    return NULL;
  }
  std::string path;
  py_convert(path, p_path);
  Coordinate new_size_node;
  if (p_new_size_node != NULL) {
    py_convert(new_size_node, p_new_size_node);
  }
  return py_convert(
      properly_truncate_fields_sync_node(path, is_check_all, is_only_check, new_size_node));
});

EXPORT(truncate_fields_sync_node, {
  using namespace qlat;
  PyObject* p_path = NULL;
  PyObject* p_fns_keep = NULL;
  PyObject* p_new_size_node = NULL;
  if (!PyArg_ParseTuple(args, "OO|O", &p_path, &p_fns_keep, &p_new_size_node)) {
    return NULL;
  }
  std::string path;
  py_convert(path, p_path);
  std::vector<std::string> fns_keep;
  py_convert(fns_keep, p_fns_keep);
  Coordinate new_size_node;
  if (p_new_size_node != NULL) {
    py_convert(new_size_node, p_new_size_node);
  }
  return py_convert(truncate_fields_sync_node(path, fns_keep, new_size_node));
});

EXPORT(flush_sfw, {
  using namespace qlat;
  PyObject* p_sfw = NULL;
  if (!PyArg_ParseTuple(args, "O", &p_sfw)) {
    return NULL;
  }
  ShuffledFieldsWriter& sfw = py_convert_type<ShuffledFieldsWriter>(p_sfw);
  return py_convert(flush(sfw));
});

EXPORT(check_compressed_eigen_vectors, {
  using namespace qlat;
  PyObject* p_path = NULL;
  if (!PyArg_ParseTuple(args, "O", &p_path)) {
    return NULL;
  }
  std::string path;
  py_convert(path, p_path);
  return py_convert(qlat::check_compressed_eigen_vectors(path));
});

EXPORT(eigen_system_repartition, {
  using namespace qlat;
  PyObject* p_new_size_node = NULL;
  PyObject* p_path = NULL;
  PyObject* p_path_new = NULL;
  if (!PyArg_ParseTuple(args, "OOO", &p_new_size_node, &p_path, &p_path_new)) {
    return NULL;
  }
  const Coordinate new_size_node = py_convert_data<Coordinate>(p_new_size_node);
  const std::string path = py_convert_data<std::string>(p_path);
  const std::string path_new = py_convert_data<std::string>(p_path_new);
  return py_convert(eigen_system_repartition(new_size_node, path, path_new));
});
