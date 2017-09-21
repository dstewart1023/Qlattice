#pragma once

QLAT_START_NAMESPACE

struct FermionAction
{
  bool initialized;
  double mass;
  int ls;
  double m5;
  double mobius_scale; // b+c, b-c=1.0
  bool is_multiplying_dminus;
  //
  void init()
  {
    initialized = false;
    mass = 0.01;
    ls = 16;
    m5 = 1.8;
    mobius_scale = 1.0; // b+c, b-c=1.0
    is_multiplying_dminus = true;
  }
  //
  FermionAction()
  {
    init();
  }
  FermionAction(const double mass_, const int ls_, const double m5_,
      const double mobius_scale = 1.0, bool is_multiplying_dminus = true)
  {
    init();
    initialized = true;
    mass = mass_;
    ls = ls_;
    m5 = m5_;
  }
};

struct LancArg
{
  bool initialized;
  double ch_alpha, ch_beta;
  long ch_ord;
  long n_use, n_get, n_true_get;
  //
  void init()
  {
    initialized = false;
    ch_alpha = 2.5;
    ch_beta = 0.022;
    ch_ord = 200;
    n_use = 2600;
    n_get = 2100;
    n_true_get = 2000;
  }
  //
  LancArg()
  {
    init();
  }
  LancArg(double ch_alpha_, double ch_beta_, long ch_ord_, long n_use_, long n_get_, long n_true_get_)
  {
    init();
    initialized = true;
    ch_alpha = ch_alpha_;
    ch_beta = ch_beta_;
    ch_ord = ch_ord_;
    n_use = n_use_;
    n_get = n_get_;
    n_true_get = n_true_get_;
  }
};


QLAT_END_NAMESPACE
