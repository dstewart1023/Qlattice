#define QLAT_INSTANTIATE_FIELD

#include <qlat/field.h>

namespace qlat
{  //

void set_mom_phase_field(FieldM<Complex, 1>& f, const CoordinateD& mom)
// mom is in lattice unit (1/a)
// exp(i * mom \cdot xg )
{
  TIMER("set_mom_phase_field");
  const Geometry& geo = f.geo();
  qacc_for(index, geo.local_volume(), {
    const Geometry& geo = f.geo();
    const Coordinate xl = geo.coordinate_from_index(index);
    const Coordinate xg = geo.coordinate_g_from_l(xl);
    double phase = 0;
    for (int k = 0; k < DIMN; ++k) {
      phase += mom[k] * xg[k];
    }
    f.get_elem(xl) = qpolar(1.0, phase);
  });
}

void set_phase_field(FieldM<Complex, 1>& f, const CoordinateD& lmom)
// lmom is in lattice momentum unit
// exp(i * 2*pi/L * lmom \cdot xg )
{
  TIMER("set_phase_field");
  const CoordinateD mom = lmom * lattice_mom_mult(f.geo());
  set_mom_phase_field(f, mom);
}

void set_xg_field(Field<Int>& f, const Geometry& geo_)
{
  TIMER("set_xg_field(f,geo)");
  const Geometry geo = geo_reform(geo_, DIMN);
  f.init(geo);
  qacc_for(index, geo.local_volume(), {
    const Coordinate xl = geo.coordinate_from_index(index);
    const Coordinate xg = geo.coordinate_g_from_l(xl);
    Vector<Int> fv = f.get_elems(xl);
    for (int mu = 0; mu < DIMN; ++mu) {
      fv[mu] = xg[mu];
    }
  });
}

}  // namespace qlat
