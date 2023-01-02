### -------------------------------------------------------------------

cdef class FieldTYPENAME(FieldBase):

    ctype = ElemTypeTYPENAME

    def __cinit__(self, Geometry geo = None, int multiplicity = 0):
        self.cdata = <long>&(self.xx)
        if geo is None:
            return
        self.xx.init(geo.xx, multiplicity)

    def __getbuffer__(self, Py_buffer *buffer, int flags):
        cdef const cc.Geometry* p_geo = &self.xx.get_geo()
        cdef cc.Coordinate local_site = p_geo[0].local_site()
        cdef int multiplicity = p_geo[0].multiplicity
        cdef cc.Vector[cc.TYPENAME] fvec = cc.get_data(self.xx)
        cdef int ndim = 5 + ElemTypeTYPENAME.ndim()
        cdef char* fmt = ElemTypeTYPENAME.format()
        cdef Buffer buf = Buffer(self, ndim, ElemTypeTYPENAME.itemsize())
        cdef cc.std_vector[Py_ssize_t] vec = ElemTypeTYPENAME.shape()
        cdef Py_ssize_t* shape = &buf.shape_strides[0]
        cdef Py_ssize_t* strides = &buf.shape_strides[buf.ndim]
        cdef int i
        for i in range(4):
            shape[i] = local_site[i]
        shape[4] = multiplicity
        for i in range(buf.ndim):
            shape[5 + i] = vec[i]
        buf.set_strides()
        buffer.buf = <char*>(fvec.data())
        if flags & PyBUF_FORMAT:
            buffer.format = fmt
        else:
            buffer.format = NULL
        buffer.internal = NULL
        buffer.itemsize = buf.itemsize
        buffer.len = buf.get_len()
        buffer.ndim = buf.ndim
        buffer.obj = buf
        buffer.readonly = 0
        buffer.shape = shape
        buffer.strides = strides
        buffer.suboffsets = NULL
        assert buffer.len == fvec.size()

    def __imatmul__(self, f1):
        # f1 can be Field, SelectedField, SelectedPoints
        # field geo does not change if already initialized
        if isinstance(f1, FieldTYPENAME):
            self.xx = (<FieldTYPENAME>f1).xx
        else:
            assert f1.ctype is self.ctype
            from qlat.selected_field import SelectedField
            from qlat.selected_points import SelectedPoints
            if isinstance(f1, SelectedField):
                c.set_field_sfield(self, f1)
            elif isinstance(f1, SelectedPoints):
                c.set_field_spfield(self, f1)
            else:
                raise Exception(f"Field @= type mismatch {type(self)} {type(f1)}")
        return self

    def copy(self, is_copying_data = True):
        f = FieldTYPENAME()
        if is_copying_data:
            f @= self
        return f

    def swap(self, FieldTYPENAME f1):
        cc.qswap(f1.xx, self.xx)

### -------------------------------------------------------------------

cdef class SelectedFieldTYPENAME(SelectedFieldBase):

    ctype = ElemTypeTYPENAME

    def __cinit__(self, FieldSelection fsel, int multiplicity):
        self.cdata = <long>&(self.xx)
        self.fsel = fsel
        if multiplicity > 0:
            self.xx.init(self.fsel.xx, multiplicity)

### -------------------------------------------------------------------

cdef class SelectedPointsTYPENAME(SelectedPointsBase):

    ctype = ElemTypeTYPENAME

    def __cinit__(self, PointSelection psel, int multiplicity = 0):
        self.cdata = <long>&(self.xx)
        self.psel = psel
        if multiplicity > 0:
            self.xx.init(self.psel.xx, multiplicity)

### -------------------------------------------------------------------

field_type_dict[ElemTypeTYPENAME] = FieldTYPENAME

selected_field_type_dict[ElemTypeTYPENAME] = SelectedFieldTYPENAME

selected_points_type_dict[ElemTypeTYPENAME] = SelectedPointsTYPENAME

### -------------------------------------------------------------------
