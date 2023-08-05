import numpy
cimport numpy
cdef extern from "worker_code.h":
    pass
cdef extern from "stopcond.h":
    pass

cimport mpi4py.MPI
cdef extern from "mpi.h":
    pass
cdef extern from "amuse_mpi.h":
    int c_set_comm_world "set_comm_world" (mpi4py.MPI.MPI_Comm world)

def set_comm_world(mpi4py.MPI.Comm comm not None):
    return c_set_comm_world(comm.ob_mpi)

cdef extern from "worker_code.h":
  
  
  int c_get_mass "get_mass" (int, double *);
  
  
  int c_commit_particles "commit_particles" ();
  
  
  int c_set_stopping_condition_timeout_parameter "set_stopping_condition_timeout_parameter" (double);
  
  
  int c_get_time "get_time" (double *);
  
  
  int c_get_children_of_binary "get_children_of_binary" (int, int *, int *);
  
  
  int c_get_stopping_condition_maximum_density_parameter "get_stopping_condition_maximum_density_parameter" (double *);
  
  
  int c_merge_with_other_star "merge_with_other_star" (int, int);
  
  
  int c_set_stopping_condition_out_of_box_use_center_of_mass_parameter "set_stopping_condition_out_of_box_use_center_of_mass_parameter" (int);
  
  
  int c_get_stopping_condition_out_of_box_use_center_of_mass_parameter "get_stopping_condition_out_of_box_use_center_of_mass_parameter" (int *);
  
  
  int c_enable_stopping_condition "enable_stopping_condition" (int);
  
  
  int c_set_supernova_kick_velocity "set_supernova_kick_velocity" (double);
  
  
  int c_get_stopping_condition_maximum_internal_energy_parameter "get_stopping_condition_maximum_internal_energy_parameter" (double *);
  
  
  int c_get_number_of_stopping_conditions_set "get_number_of_stopping_conditions_set" (int *);
  
  
  int c_change_mass "change_mass" (int, double, double);
  
  
  int c_is_stopping_condition_set "is_stopping_condition_set" (int, int *);
  
  
  int c_get_stellar_type "get_stellar_type" (int, int *);
  
  
  int c_new_particle "new_particle" (int *, double);
  
  
  int c_recall_memory_one_step "recall_memory_one_step" (int);
  
  
  int c_get_temperature "get_temperature" (int, double *);
  
  
  int c_get_is_logging_of_evolve_enabled "get_is_logging_of_evolve_enabled" (int *);
  
  
  int c_get_effective_radius "get_effective_radius" (int, double *);
  
  
  int c_evolve_for "evolve_for" (int, double);
  
  
  int c_set_stopping_condition_out_of_box_parameter "set_stopping_condition_out_of_box_parameter" (double);
  
  
  int c_set_eccentricity "set_eccentricity" (int, double);
  
  
  int c_refresh_memory "refresh_memory" (int);
  
  
  int c_set_stopping_condition_number_of_steps_parameter "set_stopping_condition_number_of_steps_parameter" (int);
  
  
  int c_get_stopping_condition_timeout_parameter "get_stopping_condition_timeout_parameter" (double *);
  
  
  int c_get_envelope_mass "get_envelope_mass" (int, double *);
  
  
  int c_get_stopping_condition_minimum_internal_energy_parameter "get_stopping_condition_minimum_internal_energy_parameter" (double *);
  
  
  int c_is_stopping_condition_enabled "is_stopping_condition_enabled" (int, int *);
  
  
  int c_get_eccentricity "get_eccentricity" (int, double *);
  
  
  int c_evolve_star "evolve_star" (double, double, double, double *, double *, double *, double *, double *, double *, int *);
  
  
  int c_get_convective_envelope_mass "get_convective_envelope_mass" (int, double *);
  
  
  int c_get_supernova_kick_velocity "get_supernova_kick_velocity" (double *);
  
  
  int c_get_stopping_condition_minimum_density_parameter "get_stopping_condition_minimum_density_parameter" (double *);
  
  
  int c_get_time_step "get_time_step" (int, double *);
  
  
  int c_get_core_radius "get_core_radius" (int, double *);
  
  
  int c_new_binary "new_binary" (int *, double, double, int, int);
  
  
  int c_recommit_particles "recommit_particles" ();
  
  
  int c_get_number_of_particles "get_number_of_particles" (int *);
  
  
  int c_get_stopping_condition_number_of_steps_parameter "get_stopping_condition_number_of_steps_parameter" (int *);
  
  
  int c_disable_stopping_condition "disable_stopping_condition" (int);
  
  
  int c_get_luminosity "get_luminosity" (int, double *);
  
  
  int c_get_age "get_age" (int, double *);
  
  
  int c_set_metallicity "set_metallicity" (double);
  
  
  int c_get_radius "get_radius" (int, double *);
  
  
  int c_set_semi_major_axis "set_semi_major_axis" (int, double);
  
  
  int c_get_natal_kick_velocity "get_natal_kick_velocity" (int, double *, double *, double *);
  
  
  int c_set_stopping_condition_minimum_internal_energy_parameter "set_stopping_condition_minimum_internal_energy_parameter" (double);
  
  
  int c_merge_the_binary "merge_the_binary" (int, int, int);
  
  
  int c_get_COcore_mass "get_COcore_mass" (int, double *);
  
  
  int c_get_semi_major_axis "get_semi_major_axis" (int, double *);
  
  
  int c_get_gyration_radius_sq "get_gyration_radius_sq" (int, double *);
  
  
  int c_set_stopping_condition_minimum_density_parameter "set_stopping_condition_minimum_density_parameter" (double);
  
  
  int c_has_stopping_condition "has_stopping_condition" (int, int *);
  
  
  int c_cleanup_code "cleanup_code" ();
  
  
  int c_set_stopping_condition_maximum_density_parameter "set_stopping_condition_maximum_density_parameter" (double);
  
  
  int c_get_relative_age "get_relative_age" (int, double *);
  
  
  int c_recommit_parameters "recommit_parameters" ();
  
  
  int c_get_relative_mass "get_relative_mass" (int, double *);
  
  
  int c_initialize_code "initialize_code" ();
  
  
  int c_evolve_system "evolve_system" (double);
  
  
  int c_evolve_one_step "evolve_one_step" (int);
  
  
  int c_get_core_mass "get_core_mass" (int, double *);
  
  
  int c_delete_star "delete_star" (int);
  
  
  int c_get_stopping_condition_out_of_box_parameter "get_stopping_condition_out_of_box_parameter" (double *);
  
  
  int c_delete_binary "delete_binary" (int);
  
  
  int c_set_is_logging_of_evolve_enabled "set_is_logging_of_evolve_enabled" (int);
  
  
  int c_set_stopping_condition_maximum_internal_energy_parameter "set_stopping_condition_maximum_internal_energy_parameter" (double);
  
  
  int c_get_stopping_condition_info "get_stopping_condition_info" (int, int *, int *);
  
  
  int c_get_metallicity "get_metallicity" (double *);
  
  
  int c_commit_parameters "commit_parameters" ();
  
  
  int c_get_wind_mass_loss_rate "get_wind_mass_loss_rate" (int, double *);
  
  
  int c_get_convective_envelope_radius "get_convective_envelope_radius" (int, double *);
  
  
  int c_get_stopping_condition_particle_index "get_stopping_condition_particle_index" (int, int, int *);
  
  
def get_mass(index_of_the_star, mass):
  
  cdef double output_mass
  cdef int __result__ = c_get_mass(index_of_the_star, &output_mass);
  mass.value = output_mass
  return __result__


def commit_particles():
  
  cdef int __result__ = c_commit_particles();
  return __result__


def set_stopping_condition_timeout_parameter(value):
  
  cdef int __result__ = c_set_stopping_condition_timeout_parameter(value);
  return __result__


def get_time(time):
  
  cdef double output_time
  cdef int __result__ = c_get_time(&output_time);
  time.value = output_time
  return __result__


def get_children_of_binary(index_of_the_star, child1, child2):
  
  cdef int output_child1
  cdef int output_child2
  cdef int __result__ = c_get_children_of_binary(index_of_the_star, &output_child1, &output_child2);
  child1.value = output_child1
  child2.value = output_child2
  return __result__


def get_stopping_condition_maximum_density_parameter(value):
  
  cdef double output_value
  cdef int __result__ = c_get_stopping_condition_maximum_density_parameter(&output_value);
  value.value = output_value
  return __result__


def merge_with_other_star(child1, child2):
  
  cdef int __result__ = c_merge_with_other_star(child1, child2);
  return __result__


def set_stopping_condition_out_of_box_use_center_of_mass_parameter(value):
  
  cdef int __result__ = c_set_stopping_condition_out_of_box_use_center_of_mass_parameter(value);
  return __result__


def get_stopping_condition_out_of_box_use_center_of_mass_parameter(value):
  
  cdef int output_value
  cdef int __result__ = c_get_stopping_condition_out_of_box_use_center_of_mass_parameter(&output_value);
  value.value = output_value
  return __result__


def enable_stopping_condition(type):
  
  cdef int __result__ = c_enable_stopping_condition(type);
  return __result__


def set_supernova_kick_velocity(v_disp):
  
  cdef int __result__ = c_set_supernova_kick_velocity(v_disp);
  return __result__


def get_stopping_condition_maximum_internal_energy_parameter(value):
  
  cdef double output_value
  cdef int __result__ = c_get_stopping_condition_maximum_internal_energy_parameter(&output_value);
  value.value = output_value
  return __result__


def get_number_of_stopping_conditions_set(result):
  
  cdef int output_result
  cdef int __result__ = c_get_number_of_stopping_conditions_set(&output_result);
  result.value = output_result
  return __result__


def change_mass(index_of_the_star, value, dt):
  
  cdef int __result__ = c_change_mass(index_of_the_star, value, dt);
  return __result__


def is_stopping_condition_set(type, result):
  
  cdef int output_result
  cdef int __result__ = c_is_stopping_condition_set(type, &output_result);
  result.value = output_result
  return __result__


def get_stellar_type(index_of_the_star, stellar_type):
  
  cdef int output_stellar_type
  cdef int __result__ = c_get_stellar_type(index_of_the_star, &output_stellar_type);
  stellar_type.value = output_stellar_type
  return __result__


def new_particle(index_of_the_star, mass):
  
  cdef int output_index_of_the_star
  cdef int __result__ = c_new_particle(&output_index_of_the_star, mass);
  index_of_the_star.value = output_index_of_the_star
  return __result__


def recall_memory_one_step(index_of_the_star):
  
  cdef int __result__ = c_recall_memory_one_step(index_of_the_star);
  return __result__


def get_temperature(index_of_the_star, temperature):
  
  cdef double output_temperature
  cdef int __result__ = c_get_temperature(index_of_the_star, &output_temperature);
  temperature.value = output_temperature
  return __result__


def get_is_logging_of_evolve_enabled(value):
  
  cdef int output_value
  cdef int __result__ = c_get_is_logging_of_evolve_enabled(&output_value);
  value.value = output_value
  return __result__


def get_effective_radius(index_of_the_star, effective_radius):
  
  cdef double output_effective_radius
  cdef int __result__ = c_get_effective_radius(index_of_the_star, &output_effective_radius);
  effective_radius.value = output_effective_radius
  return __result__


def evolve_for(index_of_the_star, delta_t):
  
  cdef int __result__ = c_evolve_for(index_of_the_star, delta_t);
  return __result__


def set_stopping_condition_out_of_box_parameter(value):
  
  cdef int __result__ = c_set_stopping_condition_out_of_box_parameter(value);
  return __result__


def set_eccentricity(index_of_the_star, value):
  
  cdef int __result__ = c_set_eccentricity(index_of_the_star, value);
  return __result__


def refresh_memory(index_of_the_star):
  
  cdef int __result__ = c_refresh_memory(index_of_the_star);
  return __result__


def set_stopping_condition_number_of_steps_parameter(value):
  
  cdef int __result__ = c_set_stopping_condition_number_of_steps_parameter(value);
  return __result__


def get_stopping_condition_timeout_parameter(value):
  
  cdef double output_value
  cdef int __result__ = c_get_stopping_condition_timeout_parameter(&output_value);
  value.value = output_value
  return __result__


def get_envelope_mass(index_of_the_star, value):
  
  cdef double output_value
  cdef int __result__ = c_get_envelope_mass(index_of_the_star, &output_value);
  value.value = output_value
  return __result__


def get_stopping_condition_minimum_internal_energy_parameter(value):
  
  cdef double output_value
  cdef int __result__ = c_get_stopping_condition_minimum_internal_energy_parameter(&output_value);
  value.value = output_value
  return __result__


def is_stopping_condition_enabled(type, result):
  
  cdef int output_result
  cdef int __result__ = c_is_stopping_condition_enabled(type, &output_result);
  result.value = output_result
  return __result__


def get_eccentricity(index_of_the_star, value):
  
  cdef double output_value
  cdef int __result__ = c_get_eccentricity(index_of_the_star, &output_value);
  value.value = output_value
  return __result__


def evolve_star(mass, endtime, metal, resulttime, end_mass, end_radius, end_luminosity, end_temperature, time_step, stellar_type):
  
  cdef double output_resulttime
  cdef double output_end_mass
  cdef double output_end_radius
  cdef double output_end_luminosity
  cdef double output_end_temperature
  cdef double output_time_step
  cdef int output_stellar_type
  cdef int __result__ = c_evolve_star(mass, endtime, metal, &output_resulttime, &output_end_mass, &output_end_radius, &output_end_luminosity, &output_end_temperature, &output_time_step, &output_stellar_type);
  resulttime.value = output_resulttime
  end_mass.value = output_end_mass
  end_radius.value = output_end_radius
  end_luminosity.value = output_end_luminosity
  end_temperature.value = output_end_temperature
  time_step.value = output_time_step
  stellar_type.value = output_stellar_type
  return __result__


def get_convective_envelope_mass(index_of_the_star, convective_envelope_mass):
  
  cdef double output_convective_envelope_mass
  cdef int __result__ = c_get_convective_envelope_mass(index_of_the_star, &output_convective_envelope_mass);
  convective_envelope_mass.value = output_convective_envelope_mass
  return __result__


def get_supernova_kick_velocity(v_disp):
  
  cdef double output_v_disp
  cdef int __result__ = c_get_supernova_kick_velocity(&output_v_disp);
  v_disp.value = output_v_disp
  return __result__


def get_stopping_condition_minimum_density_parameter(value):
  
  cdef double output_value
  cdef int __result__ = c_get_stopping_condition_minimum_density_parameter(&output_value);
  value.value = output_value
  return __result__


def get_time_step(index_of_the_star, time_step):
  
  cdef double output_time_step
  cdef int __result__ = c_get_time_step(index_of_the_star, &output_time_step);
  time_step.value = output_time_step
  return __result__


def get_core_radius(index_of_the_star, value):
  
  cdef double output_value
  cdef int __result__ = c_get_core_radius(index_of_the_star, &output_value);
  value.value = output_value
  return __result__


def new_binary(index_of_the_star, semi_major_axis, eccentricity, child1, child2):
  
  cdef int output_index_of_the_star
  cdef int __result__ = c_new_binary(&output_index_of_the_star, semi_major_axis, eccentricity, child1, child2);
  index_of_the_star.value = output_index_of_the_star
  return __result__


def recommit_particles():
  
  cdef int __result__ = c_recommit_particles();
  return __result__


def get_number_of_particles(number_of_particles):
  
  cdef int output_number_of_particles
  cdef int __result__ = c_get_number_of_particles(&output_number_of_particles);
  number_of_particles.value = output_number_of_particles
  return __result__


def get_stopping_condition_number_of_steps_parameter(value):
  
  cdef int output_value
  cdef int __result__ = c_get_stopping_condition_number_of_steps_parameter(&output_value);
  value.value = output_value
  return __result__


def disable_stopping_condition(type):
  
  cdef int __result__ = c_disable_stopping_condition(type);
  return __result__


def get_luminosity(index_of_the_star, luminosity):
  
  cdef double output_luminosity
  cdef int __result__ = c_get_luminosity(index_of_the_star, &output_luminosity);
  luminosity.value = output_luminosity
  return __result__


def get_age(index_of_the_star, age):
  
  cdef double output_age
  cdef int __result__ = c_get_age(index_of_the_star, &output_age);
  age.value = output_age
  return __result__


def set_metallicity(metallicity):
  
  cdef int __result__ = c_set_metallicity(metallicity);
  return __result__


def get_radius(index_of_the_star, radius):
  
  cdef double output_radius
  cdef int __result__ = c_get_radius(index_of_the_star, &output_radius);
  radius.value = output_radius
  return __result__


def set_semi_major_axis(index_of_the_star, value):
  
  cdef int __result__ = c_set_semi_major_axis(index_of_the_star, value);
  return __result__


def get_natal_kick_velocity(index_of_the_star, natal_kick_velocity_x, natal_kick_velocity_y, natal_kick_velocity_z):
  
  cdef double output_natal_kick_velocity_x
  cdef double output_natal_kick_velocity_y
  cdef double output_natal_kick_velocity_z
  cdef int __result__ = c_get_natal_kick_velocity(index_of_the_star, &output_natal_kick_velocity_x, &output_natal_kick_velocity_y, &output_natal_kick_velocity_z);
  natal_kick_velocity_x.value = output_natal_kick_velocity_x
  natal_kick_velocity_y.value = output_natal_kick_velocity_y
  natal_kick_velocity_z.value = output_natal_kick_velocity_z
  return __result__


def set_stopping_condition_minimum_internal_energy_parameter(value):
  
  cdef int __result__ = c_set_stopping_condition_minimum_internal_energy_parameter(value);
  return __result__


def merge_the_binary(index_of_the_binary, child1, child2):
  
  cdef int __result__ = c_merge_the_binary(index_of_the_binary, child1, child2);
  return __result__


def get_COcore_mass(index_of_the_star, value):
  
  cdef double output_value
  cdef int __result__ = c_get_COcore_mass(index_of_the_star, &output_value);
  value.value = output_value
  return __result__


def get_semi_major_axis(index_of_the_star, value):
  
  cdef double output_value
  cdef int __result__ = c_get_semi_major_axis(index_of_the_star, &output_value);
  value.value = output_value
  return __result__


def get_gyration_radius_sq(index_of_the_star, gyration_radius_sq):
  
  cdef double output_gyration_radius_sq
  cdef int __result__ = c_get_gyration_radius_sq(index_of_the_star, &output_gyration_radius_sq);
  gyration_radius_sq.value = output_gyration_radius_sq
  return __result__


def set_stopping_condition_minimum_density_parameter(value):
  
  cdef int __result__ = c_set_stopping_condition_minimum_density_parameter(value);
  return __result__


def has_stopping_condition(type, result):
  
  cdef int output_result
  cdef int __result__ = c_has_stopping_condition(type, &output_result);
  result.value = output_result
  return __result__


def cleanup_code():
  
  cdef int __result__ = c_cleanup_code();
  return __result__


def set_stopping_condition_maximum_density_parameter(value):
  
  cdef int __result__ = c_set_stopping_condition_maximum_density_parameter(value);
  return __result__


def get_relative_age(index_of_the_star, relative_age):
  
  cdef double output_relative_age
  cdef int __result__ = c_get_relative_age(index_of_the_star, &output_relative_age);
  relative_age.value = output_relative_age
  return __result__


def recommit_parameters():
  
  cdef int __result__ = c_recommit_parameters();
  return __result__


def get_relative_mass(index_of_the_star, relative_mass):
  
  cdef double output_relative_mass
  cdef int __result__ = c_get_relative_mass(index_of_the_star, &output_relative_mass);
  relative_mass.value = output_relative_mass
  return __result__


def initialize_code():
  
  cdef int __result__ = c_initialize_code();
  return __result__


def evolve_system(time):
  
  cdef int __result__ = c_evolve_system(time);
  return __result__


def evolve_one_step(index_of_the_star):
  
  cdef int __result__ = c_evolve_one_step(index_of_the_star);
  return __result__


def get_core_mass(index_of_the_star, value):
  
  cdef double output_value
  cdef int __result__ = c_get_core_mass(index_of_the_star, &output_value);
  value.value = output_value
  return __result__


def delete_star(index_of_the_star):
  
  cdef int __result__ = c_delete_star(index_of_the_star);
  return __result__


def get_stopping_condition_out_of_box_parameter(value):
  
  cdef double output_value
  cdef int __result__ = c_get_stopping_condition_out_of_box_parameter(&output_value);
  value.value = output_value
  return __result__


def delete_binary(index_of_the_particle):
  
  cdef int __result__ = c_delete_binary(index_of_the_particle);
  return __result__


def set_is_logging_of_evolve_enabled(value):
  
  cdef int __result__ = c_set_is_logging_of_evolve_enabled(value);
  return __result__


def set_stopping_condition_maximum_internal_energy_parameter(value):
  
  cdef int __result__ = c_set_stopping_condition_maximum_internal_energy_parameter(value);
  return __result__


def get_stopping_condition_info(index, type, number_of_particles):
  
  cdef int output_type
  cdef int output_number_of_particles
  cdef int __result__ = c_get_stopping_condition_info(index, &output_type, &output_number_of_particles);
  type.value = output_type
  number_of_particles.value = output_number_of_particles
  return __result__


def get_metallicity(metallicity):
  
  cdef double output_metallicity
  cdef int __result__ = c_get_metallicity(&output_metallicity);
  metallicity.value = output_metallicity
  return __result__


def commit_parameters():
  
  cdef int __result__ = c_commit_parameters();
  return __result__


def get_wind_mass_loss_rate(index_of_the_star, wind_mass_loss_rate):
  
  cdef double output_wind_mass_loss_rate
  cdef int __result__ = c_get_wind_mass_loss_rate(index_of_the_star, &output_wind_mass_loss_rate);
  wind_mass_loss_rate.value = output_wind_mass_loss_rate
  return __result__


def get_convective_envelope_radius(index_of_the_star, convective_envelope_radius):
  
  cdef double output_convective_envelope_radius
  cdef int __result__ = c_get_convective_envelope_radius(index_of_the_star, &output_convective_envelope_radius);
  convective_envelope_radius.value = output_convective_envelope_radius
  return __result__


def get_stopping_condition_particle_index(index, index_of_the_column, index_of_particle):
  
  cdef int output_index_of_particle
  cdef int __result__ = c_get_stopping_condition_particle_index(index, index_of_the_column, &output_index_of_particle);
  index_of_particle.value = output_index_of_particle
  return __result__

