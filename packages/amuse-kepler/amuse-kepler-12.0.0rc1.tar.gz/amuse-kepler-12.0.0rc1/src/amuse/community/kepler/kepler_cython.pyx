import numpy
cimport numpy
cdef extern from "interface.h":
    pass

cimport mpi4py.MPI
cdef extern from "mpi.h":
    pass
cdef extern from "amuse_mpi.h":
    int c_set_comm_world "set_comm_world" (mpi4py.MPI.MPI_Comm world)

def set_comm_world(mpi4py.MPI.Comm comm not None):
    return c_set_comm_world(comm.ob_mpi)

cdef extern from "interface.h":
  
  
  int c_transform_to_time "transform_to_time" (double);
  
  
  int c_get_time "get_time" (double *);
  
  
  int c_set_periastron "set_periastron" (double);
  
  
  int c_get_separation_vector "get_separation_vector" (double *, double *, double *);
  
  
  int c_return_to_apastron "return_to_apastron" ();
  
  
  int c_get_total_mass "get_total_mass" (double *);
  
  
  int c_get_angles "get_angles" (double *, double *);
  
  
  int c_return_to_radius "return_to_radius" (double);
  
  
  int c_get_integrals "get_integrals" (double *, double *);
  
  
  int c_get_apastron "get_apastron" (double *);
  
  
  int c_advance_to_radius "advance_to_radius" (double);
  
  
  int c_return_to_periastron "return_to_periastron" ();
  
  
  int c_get_velocity_vector "get_velocity_vector" (double *, double *, double *);
  
  
  int c_get_transverse_unit_vector "get_transverse_unit_vector" (double *, double *, double *);
  
  
  int c_set_transverse_unit_vector "set_transverse_unit_vector" (double, double, double);
  
  
  int c_set_random "set_random" (int);
  
  
  int c_advance_to_periastron "advance_to_periastron" ();
  
  
  int c_initialize_from_elements "initialize_from_elements" (double, double, double, double, double, double, int);
  
  
  int c_get_period "get_period" (double *);
  
  
  int c_make_binary_scattering "make_binary_scattering" (double, double, double, double, double, double, int, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *, double *);
  
  
  int c_cleanup_code "cleanup_code" ();
  
  
  int c_get_random "get_random" (int *);
  
  
  int c_get_separation "get_separation" (double *);
  
  
  int c_get_longitudinal_unit_vector "get_longitudinal_unit_vector" (double *, double *, double *);
  
  
  int c_recommit_parameters "recommit_parameters" ();
  
  
  int c_advance_to_apastron "advance_to_apastron" ();
  
  
  int c_initialize_code "initialize_code" ();
  
  
  int c_print_all "print_all" ();
  
  
  int c_get_periastron "get_periastron" (double *);
  
  
  int c_get_elements "get_elements" (double *, double *);
  
  
  int c_set_normal_unit_vector "set_normal_unit_vector" (double, double, double);
  
  
  int c_initialize_from_dyn "initialize_from_dyn" (double, double, double, double, double, double, double, double);
  
  
  int c_commit_parameters "commit_parameters" ();
  
  
  int c_set_longitudinal_unit_vector "set_longitudinal_unit_vector" (double, double, double);
  
  
  int c_get_normal_unit_vector "get_normal_unit_vector" (double *, double *, double *);
  
  
def transform_to_time(time):
  
  cdef int __result__ = c_transform_to_time(time);
  return __result__


def get_time(time):
  
  cdef double output_time
  cdef int __result__ = c_get_time(&output_time);
  time.value = output_time
  return __result__


def set_periastron(peri):
  
  cdef int __result__ = c_set_periastron(peri);
  return __result__


def get_separation_vector(x, y, z):
  
  cdef double output_x
  cdef double output_y
  cdef double output_z
  cdef int __result__ = c_get_separation_vector(&output_x, &output_y, &output_z);
  x.value = output_x
  y.value = output_y
  z.value = output_z
  return __result__


def return_to_apastron():
  
  cdef int __result__ = c_return_to_apastron();
  return __result__


def get_total_mass(mass):
  
  cdef double output_mass
  cdef int __result__ = c_get_total_mass(&output_mass);
  mass.value = output_mass
  return __result__


def get_angles(true_anomaly, mean_anomaly):
  
  cdef double output_true_anomaly
  cdef double output_mean_anomaly
  cdef int __result__ = c_get_angles(&output_true_anomaly, &output_mean_anomaly);
  true_anomaly.value = output_true_anomaly
  mean_anomaly.value = output_mean_anomaly
  return __result__


def return_to_radius(radius):
  
  cdef int __result__ = c_return_to_radius(radius);
  return __result__


def get_integrals(energy, angular_momentum):
  
  cdef double output_energy
  cdef double output_angular_momentum
  cdef int __result__ = c_get_integrals(&output_energy, &output_angular_momentum);
  energy.value = output_energy
  angular_momentum.value = output_angular_momentum
  return __result__


def get_apastron(apo):
  
  cdef double output_apo
  cdef int __result__ = c_get_apastron(&output_apo);
  apo.value = output_apo
  return __result__


def advance_to_radius(radius):
  
  cdef int __result__ = c_advance_to_radius(radius);
  return __result__


def return_to_periastron():
  
  cdef int __result__ = c_return_to_periastron();
  return __result__


def get_velocity_vector(vx, vy, vz):
  
  cdef double output_vx
  cdef double output_vy
  cdef double output_vz
  cdef int __result__ = c_get_velocity_vector(&output_vx, &output_vy, &output_vz);
  vx.value = output_vx
  vy.value = output_vy
  vz.value = output_vz
  return __result__


def get_transverse_unit_vector(vx, vy, vz):
  
  cdef double output_vx
  cdef double output_vy
  cdef double output_vz
  cdef int __result__ = c_get_transverse_unit_vector(&output_vx, &output_vy, &output_vz);
  vx.value = output_vx
  vy.value = output_vy
  vz.value = output_vz
  return __result__


def set_transverse_unit_vector(vx, vy, vz):
  
  cdef int __result__ = c_set_transverse_unit_vector(vx, vy, vz);
  return __result__


def set_random(seed):
  
  cdef int __result__ = c_set_random(seed);
  return __result__


def advance_to_periastron():
  
  cdef int __result__ = c_advance_to_periastron();
  return __result__


def initialize_from_elements(mass, semi, ecc, mean_anomaly, time, periastron, random_orientation):
  
  cdef int __result__ = c_initialize_from_elements(mass, semi, ecc, mean_anomaly, time, periastron, random_orientation);
  return __result__


def get_period(period):
  
  cdef double output_period
  cdef int __result__ = c_get_period(&output_period);
  period.value = output_period
  return __result__


def make_binary_scattering(m, ecc, M, v_inf, impact_parameter, gamma, planar, time, m1, m2, m3, x1, x2, x3, y1, y2, y3, z1, z2, z3, vx1, vx2, vx3, vy1, vy2, vy3, vz1, vz2, vz3):
  
  cdef double output_time
  cdef double output_m1
  cdef double output_m2
  cdef double output_m3
  cdef double output_x1
  cdef double output_x2
  cdef double output_x3
  cdef double output_y1
  cdef double output_y2
  cdef double output_y3
  cdef double output_z1
  cdef double output_z2
  cdef double output_z3
  cdef double output_vx1
  cdef double output_vx2
  cdef double output_vx3
  cdef double output_vy1
  cdef double output_vy2
  cdef double output_vy3
  cdef double output_vz1
  cdef double output_vz2
  cdef double output_vz3
  cdef int __result__ = c_make_binary_scattering(m, ecc, M, v_inf, impact_parameter, gamma, planar, &output_time, &output_m1, &output_m2, &output_m3, &output_x1, &output_x2, &output_x3, &output_y1, &output_y2, &output_y3, &output_z1, &output_z2, &output_z3, &output_vx1, &output_vx2, &output_vx3, &output_vy1, &output_vy2, &output_vy3, &output_vz1, &output_vz2, &output_vz3);
  time.value = output_time
  m1.value = output_m1
  m2.value = output_m2
  m3.value = output_m3
  x1.value = output_x1
  x2.value = output_x2
  x3.value = output_x3
  y1.value = output_y1
  y2.value = output_y2
  y3.value = output_y3
  z1.value = output_z1
  z2.value = output_z2
  z3.value = output_z3
  vx1.value = output_vx1
  vx2.value = output_vx2
  vx3.value = output_vx3
  vy1.value = output_vy1
  vy2.value = output_vy2
  vy3.value = output_vy3
  vz1.value = output_vz1
  vz2.value = output_vz2
  vz3.value = output_vz3
  return __result__


def cleanup_code():
  
  cdef int __result__ = c_cleanup_code();
  return __result__


def get_random(seed):
  
  cdef int output_seed
  cdef int __result__ = c_get_random(&output_seed);
  seed.value = output_seed
  return __result__


def get_separation(r):
  
  cdef double output_r
  cdef int __result__ = c_get_separation(&output_r);
  r.value = output_r
  return __result__


def get_longitudinal_unit_vector(vx, vy, vz):
  
  cdef double output_vx
  cdef double output_vy
  cdef double output_vz
  cdef int __result__ = c_get_longitudinal_unit_vector(&output_vx, &output_vy, &output_vz);
  vx.value = output_vx
  vy.value = output_vy
  vz.value = output_vz
  return __result__


def recommit_parameters():
  
  cdef int __result__ = c_recommit_parameters();
  return __result__


def advance_to_apastron():
  
  cdef int __result__ = c_advance_to_apastron();
  return __result__


def initialize_code():
  
  cdef int __result__ = c_initialize_code();
  return __result__


def print_all():
  
  cdef int __result__ = c_print_all();
  return __result__


def get_periastron(peri):
  
  cdef double output_peri
  cdef int __result__ = c_get_periastron(&output_peri);
  peri.value = output_peri
  return __result__


def get_elements(semi, ecc):
  
  cdef double output_semi
  cdef double output_ecc
  cdef int __result__ = c_get_elements(&output_semi, &output_ecc);
  semi.value = output_semi
  ecc.value = output_ecc
  return __result__


def set_normal_unit_vector(vx, vy, vz):
  
  cdef int __result__ = c_set_normal_unit_vector(vx, vy, vz);
  return __result__


def initialize_from_dyn(mass, x, y, z, vx, vy, vz, time):
  
  cdef int __result__ = c_initialize_from_dyn(mass, x, y, z, vx, vy, vz, time);
  return __result__


def commit_parameters():
  
  cdef int __result__ = c_commit_parameters();
  return __result__


def set_longitudinal_unit_vector(vx, vy, vz):
  
  cdef int __result__ = c_set_longitudinal_unit_vector(vx, vy, vz);
  return __result__


def get_normal_unit_vector(vx, vy, vz):
  
  cdef double output_vx
  cdef double output_vy
  cdef double output_vz
  cdef int __result__ = c_get_normal_unit_vector(&output_vx, &output_vy, &output_vz);
  vx.value = output_vx
  vy.value = output_vy
  vz.value = output_vz
  return __result__

