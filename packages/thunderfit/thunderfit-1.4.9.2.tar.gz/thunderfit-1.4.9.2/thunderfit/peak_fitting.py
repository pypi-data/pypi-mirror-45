import logging

from lmfit import models
from numpy import nan

from . import utilities as utils
from . import model_creation

def get_tols(method, tol):
    if method in ['leastsq', 'least_squares']:
        tols = {'ftol': tol, 'xtol': tol}  # warning: need to experiment with these/allow control maybe?
    else:
        tols = {'ftol': tol}
    return tols

def prep_algo(method, tols, all_bounds):
    if method == 'basinhopping' or method == 'ampgo':
        print('Warning: This is a very slow but thorough algorithm')
    if method == 'differential_evolution':
        all_bounds = True

    if method in ['leastsq', 'least_squares', 'nelder', 'cobyla']:
        tols  = get_tols(method, tols)

    return tols, all_bounds


def fit_peaks(x_data, y_data, peak_types, peak_centres, peak_amps, peak_widths, bounds, method='leastsq', tol=0.0000001,
              all_bounds=False):
    impl_methods = ['leastsq', 'least_squares', 'nelder', 'lbfgsb', 'powell', 'cg', 'cobyla', 'bfgsb',
                    'differential_evolution', 'basinhopping', 'ampgo']
    if not method in impl_methods:
        raise ValueError(f"The method supplied is not supported. Available methods: {impl_methods}")
    logging.debug(f'fitting peaks:  peak_centres:{peak_centres}, peak_amps:{peak_amps}, peak_widths:{peak_widths}, '
                  f'peak_types:{peak_types}, bounds:{bounds}')

    tols, all_bounds = prep_algo(method, tol, all_bounds)
    model_specs = build_specs(peak_types, peak_centres, peak_amps, peak_widths, bounds)
    model, peak_params = generate_model(model_specs, all_bounds)

    if method in ['leastsq', 'least_squares', 'nelder', 'cobyla']:
        peaks = model.fit(y_data, peak_params, x=x_data, method=method, fit_kws=tols)
        if not peaks.success:
            print('peaks failed to fit, raising tolerance by one order magnitude and trying again')
            tols = {key:value*10 for key, value in tols.items()} # try raising the tolerance if it fails by one order
            peaks = model.fit(y_data, peak_params, x=x_data, method=method, fit_kws=tols)
    else:
        peaks = model.fit(y_data, peak_params, x=x_data, method=method)

    peak_params = peaks.best_values
    if not peaks.success:
        print('peaks failed to fit')
        peak_params = {key: nan for key in peak_params}
    return model_specs, model, peak_params, peaks

def safe_list_get (l, idx, default):
    """fetch items safely from a list, if it isn't long enough return a default value"""
    try:
        return l[idx]
    except IndexError:
        return default

##### Call this with correct arguments, should always call with all the arguments!
def build_specs(peak_types, peak_centres, peak_amps, peak_widths, bounds,
                sigma_rs=(), gammas=(), fractions=(), betas=(), exponents=(), qs=(), cs=(), intercepts=(), slopes=(),
                _as=(), bs=(), degrees=(), poly_consts=(), forms=(), center1s=(), center2s=(), sigma1s=(), sigma2s=(),
                decays=()):
    """Build a specs list, which has the peak specification details for each element corresponding to a peak to fit.
    Note that each element is a dictionary containing either None, or a value for that peak i.e. the parameter guess,
    or the bounds for that value. Only some will be valid for each peak type, which will be handled elsewhere"""
    logging.debug('building specs')
    specs = [
        {
            'type': peak_types[i],
            'params': {'center': utils.safe_list_get(peak_centres, i, None),
                       'amplitude': utils.safe_list_get(peak_amps, i, None),
                       'sigma': utils.safe_list_get(peak_widths, i, None),
                       'sigma_r': utils.safe_list_get(sigma_rs, i, None),
                       'gamma': utils.safe_list_get(gammas, i, None),
                       'fraction': utils.safe_list_get(fractions, i, None),
                       'beta': utils.safe_list_get(betas, i, None),
                       'exponent': utils.safe_list_get(exponents, i, None),
                       'q': utils.safe_list_get(qs, i, None),
                       'c': utils.safe_list_get(cs, i, None),
                       'intercept': utils.safe_list_get(intercepts, i, None),
                       'slope': utils.safe_list_get(slopes, i, None),
                       'a': utils.safe_list_get(_as, i, None),
                       'b': utils.safe_list_get(bs, i, None),
                       'degree': utils.safe_list_get(degrees, i, None),
                       'poly_consts': utils.safe_list_get(poly_consts, i, [None, ]),
                       'form': utils.safe_list_get(forms, i, None),
                       'center1': utils.safe_list_get(center1s, i, None),
                       'center2': utils.safe_list_get(center2s, i, None),
                       'sigma1': utils.safe_list_get(sigma1s, i, None),
                       'sigma2': utils.safe_list_get(sigma2s, i, None),
                       'decay': utils.safe_list_get(decays, i, None)
                       },
            'bounds': {'center': utils.safe_list_get(bounds['centers'], i,(None, None)),
                       'amplitude': utils.safe_list_get(bounds['amps'], i, (None, None)),
                       'sigma': utils.safe_list_get(bounds['widths'], i, (None, None)),
                       'sigma_r': utils.safe_list_get(sigma_rs, i, (None, None)),
                       'gamma': utils.safe_list_get(gammas, i, (None, None)),
                       'fraction': utils.safe_list_get(fractions, i, (None, None)),
                       'beta': utils.safe_list_get(betas, i, (None, None)),
                       'exponent': utils.safe_list_get(exponents, i, (None, None)),
                       'q': utils.safe_list_get(qs, i, (None, None)),
                       'c': utils.safe_list_get(cs, i, (None, None)),
                       'intercept': utils.safe_list_get(intercepts, i, (None, None)),
                       'slope': utils.safe_list_get(slopes, i, (None, None)),
                       'a': utils.safe_list_get(_as, i, (None, None)),
                       'b': utils.safe_list_get(bs, i, (None, None)),
                       'degree': utils.safe_list_get(degrees, i, (None, None)),
                       'poly_consts': utils.safe_list_get(poly_consts, i, [(None, None),]),
                       'form': utils.safe_list_get(forms, i, (None, None)),
                       'center1': utils.safe_list_get(center1s, i, (None, None)),
                       'center2': utils.safe_list_get(center2s, i, (None, None)),
                       'sigma1': utils.safe_list_get(sigma1s, i, (None, None)),
                       'sigma2': utils.safe_list_get(sigma2s, i, (None, None)),
                       'decay': utils.safe_list_get(decays, i, (None, None))
                       }
        }
        for i, _ in range(peak_types)
    ]

    return specs

def generate_model(model_specs, all_bounds=False):
    """
    https://chrisostrouchov.com/post/peak_fit_xrd_python/
    :param model_specs:
    :return:
    """
    logging.debug('generating model specs')
    composite_model = None
    params = None
    for i, spec in enumerate(model_specs):
        prefix = f'm{i}_'
        model = getattr(models, spec['type'])(prefix=prefix) # generate the lmfit model based on the type specified

        model = decide_model_actions(spec, model, all_bounds) # call another function to decide what to do
        model_params = model.make_params() # make the params object

        if params is None: # first loop
            params = model_params
            composite_model = model
        else: # subsequent loops
            params.update(model_params)
            composite_model = composite_model + model

    return composite_model, params

def decide_model_actions(spec, model, all_bounds):
    if spec['type'] in ['GaussianModel', 'LorentzianModel']:
        model = model_creation.make_gauss_or_lor(model, spec, all_bounds)
    elif spec['type'] == 'SplitLorentzianModel':
        model = model_creation.make_split_lor(model, spec, all_bounds)
    else:
        raise NotImplemented(f'model {spec["type"]} not implemented yet')
    return model

