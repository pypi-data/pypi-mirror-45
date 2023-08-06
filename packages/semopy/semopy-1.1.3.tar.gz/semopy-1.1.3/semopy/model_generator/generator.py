from .structgenerator import generate_measurement_part,\
                             generate_structural_part, create_model_description
from .datagenerator import generate_data
from .paramgenerator import generate_parameters, params_set_to_dataframe
from scipy.stats import uniform
from numpy.random import choice
from functools import partial


def param_gen(scale, shift):
    v = scale * uniform.rvs(0.1, 1.1)
    if choice([True, False]):
        return v + shift
    else:
        return -v + shift

def generate_model(n_obs: int, n_lat: int, n_manif: tuple, p_manif: float,
                   n_cycles: int, scale: float, n_size: int):
    """Generates a measurement, structural parts, parameters and data. Bear in
    mind that this method is a wrapper around generatte_measurement_part,
    generated_structura_part, generate_parameters and generate_data. The
    functionality embodied in those methods is much broader than in this one.
    If one wishes to approach the generation process with a greater
    versatility, consider using those methods instead (see their __doc__
    strings). This methods exists solely for simplicity purposes.
    Keyword arguments:
        n_obs    -- A number of observed variables in structural part.
        n_lat    -- A number of latent variables in structural part.
        n_manif  -- A range from which a number of manifest variables will be
                    chosen for each latent variable.
        p_manif  -- A percentage of manifest variables that will be merged
                    together.
        n_cycles -- A number of cycles to be present in the model.
        scale    -- All parameters sampled from uniform distribution on interval
                    [-1, -0.1]u[0.1, 1] are multiplied by this value.
        n_size   -- A number of data samples.
    Returns:
        Model description, DataFrame with parameters values, data.
    """
    f_gen = partial(param_gen, scale, 0)
    mpart = generate_measurement_part(n_lat, n_manif, p_manif)
    spart, tm = generate_structural_part(mpart, n_obs, num_cycles=n_cycles)
    params_mpart, params_spart = generate_parameters(mpart, spart,
                                                     mpart_generator=f_gen,
                                                     spart_generator=f_gen)
    data = generate_data(mpart, spart, params_mpart, params_spart,
                         n_size, tm)
    params_df = params_set_to_dataframe(params_mpart, params_spart, False)
    model = create_model_description(mpart, spart)
    return model, params_df, data