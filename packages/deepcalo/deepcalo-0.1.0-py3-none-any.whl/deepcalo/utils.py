import os
import sys
import copy
import numpy as np
import itertools
from datetime import datetime
import h5py
import pickle
import argparse
import pprint
from sklearn.preprocessing import StandardScaler, RobustScaler


def load_data(path, n_points={'train':None, 'val':None, 'test':None},
              cnn_output=None, img_names=None, scalar_names=None,
              eval_scalar_names=None, load_sample_weights=False,
              load_time_imgs=False, load_tracks=False, verbose=True):
    """
    Args:
    -----
        path : *str*
            Path to the data to be loaded.

        n_points : *dict*
            This dictionary defines the names of the subsets of the data loaded
            (by way of the keys of `n_points`), as well as how many datapoints
            should be loaded for each set (by way of the values of `n_points`).
            This information is passed to `load_data` in `utils.py` through
            `main.py`.

            Its *keys* should be either `'train'` and `'val'`, or `'train'`,
            `'val'` and `'test'`. This means that while both training and
            validation data are required, test data can be left out. If test
            data is left out, no evaluation will be carried out at the end of
            training. It is important that the naming conventions of `'train'`,
            `'val'` and `'test'` are kept, as this is the only way the
            subsequent handling of the data knows which sets are meant to be
            used for what.

            The *values* of `n_points` dictate how many points of each set will
            be loaded. If `None`, all datapoints in the set corresponding to
            the key will be loaded. If instead a number n (*int* or *float*,
            where the latter will be converted into an *int*), only the first n
            datapoints of that set will be loaded. If a *list* of *int*s, this
            will be interpreted as indices, and only datapoints with these
            indices will be loaded (primarily used in conjunction with data
            generators).

        cnn_output : *str or None*
            The path of a file containing the outputs of a previously trained
            CNN. If not None, CNN outputs will be loaded instead of any images.

        img_names : *list of strs or None*
            List of image names to be loaded. Each image name will have its own
            entry in the returned data dict (acccessed by its name).
            If None (default), no images will be loaded and no CNN will be
            constructed.

        scalar_names : *list of strs or None*
            List of scalar variable names (meant to be used in training) to be
            loaded into the 'scalars' entry of the returned data dict.
            If None, no scalar variables will be loaded.

        eval_scalar_names : *list of strs or None*
            List of scalar variable names (meant to be used in evaluation) to be
            loaded into the 'eval_scalars' entry of the returned data dict.
            If 'all', all scalars will be loaded.
            If None, no evaluation scalar variables will be loaded.

        load_sample_weights : *bool*
            Whether to load sample weights to be used in training. Useful if
            classes are unbalanced or if certain marginal signal/background
            distributions do not follow each other nicely.

        load_time_imgs : *bool*
            Whether to load time images.

        load_tracks : *bool*
            Whether to load tracks.

        verbose : *bool*
            Verbose output.

    Returns:
    --------
        data : *dict*
            Dictionary of data. This dictionary (in its first level) will
            contain the same keys as those in n_points. Each of these keys point
            to another dict containing the different datasets (such as images
            and scalars).
            For example, if
            n_points = {'train':None, 'val':2000, 'test':1e3} and if
            scalar_names is not None, then we would access our training set
            scalars (which, like all the other datasets, should be a numpy
            array) like so: data['train']['scalars']. If we instead want
            to access the test set images, and img_names is ['img'], we do
            data['test']['img'].
            The target (or label in the case of classification) datasets are
            named 'targets'.
    """

    if verbose:
        print('Loading data.')

    # Prepare loading only the wanted data points
    # Make copy of n_points to use for loading (changes to n_points will persist
    # outside of this function)
    load_n_points = copy.deepcopy(n_points)

    for set_name in load_n_points:
        # If a list (of specific indices) is not given
        if not hasattr(load_n_points[set_name], '__iter__'):
            # If all data points should be loaded
            if load_n_points[set_name] is None:
                load_n_points[set_name] = slice(None)
            # If only the first int(load_n_points[set_name]) data points should be loaded
            else:
                load_n_points[set_name] = int(load_n_points[set_name])
                n_samples = load_n_points[set_name]
                load_n_points[set_name] = slice(None,load_n_points[set_name])
                if verbose:
                    print(f'Loading only the {n_samples} first data points of the {set_name} set.')
        else:
            load_n_points[set_name] = list(np.sort(load_n_points[set_name]))

    # Load the data
    with h5py.File(path, 'r') as hf:

        # Function for loading and organizing images
        def load_img(img_name, set_name, lrs, samples):
            return np.moveaxis(np.concatenate(tuple(hf[f'{img_name}_Lr{lr}_{set_name}'][samples] for lr in lrs),
                                              axis=1), source=1, destination=3)

        data = {set_name:{'images':{},
                          'scalars':{},
                          'tracks':{},
                          'targets':{},
                          'sample_weights':{}} for set_name in load_n_points}

        # Add targets to data
        for set_name in load_n_points:
            data[set_name]['targets'] = hf[f'y_{set_name}'][load_n_points[set_name]]

        # Add all scalars
        for set_name in load_n_points:
            data[set_name]['eval_scalars'] = hf[f'all_scalar_{set_name}'][load_n_points[set_name]]

        # Only load images if cnn_output is not already given
        if cnn_output is None and img_names is not None:
            # Add cell images to data
            # Different parts of the detector have a different number of layers
            layers_to_include = {}
            for img_name in img_names:
                if img_name == 'em_barrel':
                    lrs = [0,1,2,3]
                elif img_name == 'em_endcap':
                    lrs = [0,1,2,3]
                elif img_name == 'lAr_endcap':
                    lrs = [0,1,2,3]
                elif img_name == 'had_barrel':
                    lrs = [1,2]
                elif img_name == 'tile_ext_barrel':
                    lrs = [0,1,2,3]
                elif img_name == 'tile_gap':
                    lrs = [0,1,2,3]
                layers_to_include[img_name] = lrs

            for set_name in load_n_points:
                for img_name in img_names:
                    data[set_name]['images'][img_name] = load_img(img_name, set_name, layers_to_include[img_name], load_n_points[set_name])

            # Add time images to data
            # Note the division of 50 - this is actually preprocessing, but is easier to do here
            if load_time_imgs:
                for set_name in load_n_points:
                    for img_name in img_names:
                        data[set_name]['images'][f'time_{img_name}'] = load_img('time', set_name, layers_to_include[img_name], load_n_points[set_name]) / 50

        # Load the cnn_output, if given
        elif cnn_output is not None:
            with h5py.File(cnn_output,'r') as hf:
                for set_name in load_n_points:
                    data[set_name]['cnn_output'] = hf[f'cnn_ouputs_{set_name}'][load_n_points[set_name]]

        # Add scalars to data
        if scalar_names is not None:
            for set_name in load_n_points:
                data[set_name]['scalars'] = data[set_name]['eval_scalars'][scalar_names]

        # Reduce to only the variables that are actually needed (e.g. for plotting and evaluation)
        if eval_scalar_names is not None and eval_scalar_names!='all':
            for set_name in load_n_points:
                data[set_name]['eval_scalars'] = data[set_name]['eval_scalars'][eval_scalar_names]

        # Add sample weights (from reweighting)
        if load_sample_weights:
            for set_name in load_n_points:
                data[set_name]['sample_weights'] = data[set_name]['eval_scalars']['total_weight']

        # Add tracks
        if load_tracks:
            for set_name in load_n_points:
                data[set_name]['tracks'] = hf[f'track_{set_name}'][load_n_points[set_name]]

    # Convert scalar variables to normal numpy arrays (without names)
    # This can be done more elegantly!
    if scalar_names is not None:
        import pandas as pd
        for set_name in load_n_points:
            data[set_name]['scalars'] = pd.DataFrame(data[set_name]['scalars']).values

    if verbose:
        print('Data loaded.')

    return data


def apply_preprocessing(data, standardize=True, robust_scaler=True,
                        pull_in_outliers=False, rm_outliers=False, rm_bad_reco=False,
                        medium_only=False, only_unconv_photon=False, verbose=True):

    # data is structured with keys 'train', 'val', possibly 'test', where each corresponding item
    # is structured into datasets (img_name, scalars, eval_scalars, time_img_name, etc.)
    # See load_data above for details.

    # Remember number of given data points
    n_points = {set_name:next(len(data[set_name][dataset]) for dataset in data[set_name]) for set_name in data}

    # Should we bother about preprocessing scalars?
    scalars_in_data = any(dataset=='scalars' for dataset in data['train'])

    if scalars_in_data:
        n_vars = data['train']['scalars'].shape[1]

    # Remove all events which the current E calib. reconstructs badly
    if rm_bad_reco:

        masks = {set_name:np.abs(data[set_name]['all_scalars']['p_e'] / data[set_name]['all_scalars']['p_truth_E'] - 1) <= 0.5 for set_name in data}

        for set_name in data:
            for dataset in data[set_name]:
                data[set_name][dataset] = data[set_name][dataset][masks[set_name]]
            if verbose:
                print(f'Removed {np.sum(np.logical_not(masks[set_name]))} badly reconstructed data points (out of {len(masks[set_name])}) from the {set_name} set.')

    # Let only unconverted photons through
    if only_unconv_photon:
        masks = {set_name:np.isclose(data[set_name]['all_scalars']['p_photonConversionType'],0) for set_name in data}

        for set_name in data:
            for dataset in data[set_name]:
                data[set_name][dataset] = data[set_name][dataset][masks[set_name]]
            if verbose:
                print(f'Removed {np.sum(np.logical_not(masks[set_name]))} converted photons (out of {len(masks[set_name])} photons) from the {set_name} set.')

    # Remove all but medium electrons. For prediction on real data test set.
    if medium_only:

        mask = np.isclose(data['test']['all_scalars']['pX_LHMedium'],1)

        for dataset in data['test']:
            data['test'][dataset] = data['test'][dataset][mask]
        if verbose:
            print('Only removing non-medium electrons from the test set!')
            print(f'Removed {np.sum(np.logical_not(mask))} non-medium cut data points (out of {len(mask)}) from the test set.')

    # Pull all outliers (like -999) towards the median
    if pull_in_outliers and scalars_in_data:

        def abs_dev(a, c=0.67448975, axis=0, center=np.median):
            # From https://www.statsmodels.org/dev/generated/statsmodels.robust.scale.mad.html
            """
            The Absolute Deviation along given axis of an array

            Parameters
            ----------
            a : array-like
                Input array.
            c : float, optional
                The normalization constant.  Defined as scipy.stats.norm.ppf(3/4.),
                which is approximately .6745.
            axis : int, optional
                The default is 0. Can also be None.
            center : callable or float
                If a callable is provided, such as the default `np.median` then it
                is expected to be called center(a). The axis argument will be applied
                via np.apply_over_axes. Otherwise, provide a float.

            Returns
            -------
            Absolute deviation : float
                abs(`a` - center))/`c`
            """
            a = np.asarray(a)
            if callable(center):
                center = np.apply_over_axes(center, a, axis)
            return np.fabs(a-center)/c

        # Outlier criterion (number of robust standard deviations)
        crit_outlier = 5e2

        # Remember variables with too many outliers to treat normally
        var_i_many_outliers = []

        # Fraction of outliers allowed to treat normally
        tol_outliers = 0.0001

        # How many robust standard deviations away to nudge the outliers,
        # after they have been pulled in
        nudge_outliers = 3

        # Find outliers

        for var_i in range(n_vars):
            if verbose:
                    print(f'\n### Variable {var_i} ###')
            for set_name in data:
                var = data[set_name]['scalars'][:,var_i]
                center = np.median(var)
                ad = abs_dev(var, center=center)
                mad = np.median(ad)
                outliers = ad/mad > crit_outlier
                if not np.any(outliers):
                    if verbose:
                        print(f'Variable {var_i} had no outliers in {set_name} set.')
                    continue
                outlier_inds = np.array(np.nonzero(outliers)[0])
                frac_outliers = outlier_inds.shape[0]/var.shape[0]
                if verbose:
                    print(f'Variable {var_i} had {frac_outliers*100:.4f}% outliers in {set_name} set.')
                if frac_outliers > tol_outliers:
                    var_i_many_outliers.append(var_i)
                    if verbose:
                        print(f'This is above the tolerated {tol_outliers*100:.4f}%.')
                else:
                    var_nout = var[~outliers]
                    var_nout_min, var_nout_max = var_nout.min(), var_nout.max()
                    if verbose:
                        print(f'Min,max values of non-outliers: {var_nout_min:.4f}, {var_nout_max:.4f}')
                    for out_ind in outlier_inds:
                        # Determine on which side of the median the outlier is
                        above = var[out_ind] > center
                        if verbose:
                            print(f'Converted {data[set_name]["scalars"][out_ind,var_i]:.5f} to ', end='')
                        if above:
                            pulled_in_and_nudged_out = var_nout_max + nudge_outliers * mad
                        else:
                            pulled_in_and_nudged_out = var_nout_min - nudge_outliers * mad
                        # Convert
                        data[set_name]['scalars'][out_ind,var_i] = pulled_in_and_nudged_out
                        if verbose:
                            print(f'{data[set_name]["scalars"][out_ind,var_i]:.5f}')


        # If there are too many, scale with StandardScaler (and divide by 10)
        var_i_many_outliers = np.unique(var_i_many_outliers)
        if standardize and robust_scaler and len(var_i_many_outliers) > 0:
            # Use the first set_name (typically train) to fit the scaler
            scaler = StandardScaler(copy=False).fit(data['train']['scalars'][:,var_i_many_outliers])

            # Apply the scaler
            for set_name in data:
                data[set_name]['scalars'][:,var_i_many_outliers] = scaler.transform(data[set_name]['scalars'][:,var_i_many_outliers]) / 10

            if verbose:
                print(f'Transformed variables {var_i_many_outliers} using StandardScaler.')

    # Remove all outliers in scalars # DEPRECATED
    if rm_outliers and scalars_in_data:

        print('WARNING: rm_outliers is deprecated and not recommended!')

        for set_name in data:

            mask = 1
            for var_i in range(n_vars):
                mask_var = np.abs(data[set_name]['scalars'][:,var_i]) <= 20
                if verbose:
                    print(f'{np.sum(np.logical_not(mask_var)) / len(mask_var) * 100:.3f}% of data points of variable number {var_i} in the {set_name} set are outliers.')
                mask *= mask_var
            mask = mask.astype(bool)

            for dataset in data[set_name]:
                data[set_name][dataset] = data[set_name][dataset][mask]

            if verbose:
                print(f'Removed {np.sum(np.logical_not(mask))} outliers (out of {len(mask)}) from the {set_name} set.')

    # Standardize
    if standardize and scalars_in_data:
        if robust_scaler:
            # Only transform variables not in var_i_many_outliers
            if pull_in_outliers:
                var_i_not_many_outliers = [var_i for var_i in range(n_vars) if var_i not in var_i_many_outliers]

            # Use the 'train' set to fit the scaler
            scaler = RobustScaler(copy=False).fit(data['train']['scalars'][:,var_i_not_many_outliers])
        else:
            # Use the 'train' set to fit the scaler
            scaler = StandardScaler(copy=False).fit(data['train']['scalars'])

        # Apply the scaler
        for set_name in data:
            if robust_scaler and pull_in_outliers:
                data[set_name]['scalars'][:,var_i_not_many_outliers] = scaler.transform(data[set_name]['scalars'][:,var_i_not_many_outliers])
            else:
                data[set_name]['scalars'] = scaler.transform(data[set_name]['scalars'])

        if verbose:
            if robust_scaler:
                trans_str = 'Robust'
            else:
                trans_str = 'Standard'
            print(f'Transformed datasets using {trans_str}Scaler.')

    return data


def create_directories(base_dir, epochs, log_prefix=''):

    current_time = datetime.utcnow().isoformat()

    if log_prefix != '':
        log_prefix = log_prefix.replace(',','_')
        log_dir = base_dir + f'logs/{log_prefix}/{current_time}_{epochs}_epochs/'
    else:
        log_dir = base_dir + f'logs/{current_time}_{epochs}_epochs/'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    fig_dir = log_dir + 'figures/'
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)

    saved_models_dir = log_dir + 'saved_models/'
    if not os.path.exists(saved_models_dir):
        os.makedirs(saved_models_dir)

    lr_finder_dir = log_dir + 'lr_finder/'
    if not os.path.exists(lr_finder_dir):
        os.makedirs(lr_finder_dir)

    dirs = {'log'           : log_dir,
            'fig'           : fig_dir,
            'saved_models'  : saved_models_dir,
            'lr_finder'     : lr_finder_dir}

    return dirs


def merge_dicts(base_dict, subset_dict=None, in_depth=False):
    """
    For every key in the dictionary subset_dict that is also a key in the
    base_dict dictionary, overwrite the value of that key in base_dict with the
    one from subset_dict, and return the resulting (partially overwritten)
    version of base_dict.
    """

    if subset_dict is None:
        return base_dict

    merged_dict = copy.deepcopy(base_dict)

    for key in subset_dict:
        if not isinstance(subset_dict[key], dict):
            merged_dict[key] = subset_dict[key]
        else:
            if not isinstance(merged_dict[key], dict) or not in_depth:
                merged_dict[key] = subset_dict[key]
            else:
                merged_dict[key] = merge_dicts(merged_dict[key], subset_dict[key], in_depth=True)

    return merged_dict


def save_dict(dict, path, overwrite=False, save_pkl=False):
    """
    Args :
        dict :
            *dict*

            Dictionary to be saved.
        path :
            *str*

            Path to which the dictionary should be saved. The path must have a
            file ending (i.e. '.*') to work properly with the 'save_pkl' option.
            If the path already exists, the given dict will be appended
            to what is already in the file.
        overwrite :
            *bool*

            Whether to overwrite an already existing text file in the same path.
            Picled files are always overwritten, if they exist.
        save_pkl :
            *bool*

            Saves dict as a pickled file, in addition to the text file.
    """

    if os.path.exists(path):
        mod = 'a'
        if overwrite:
            mod = 'w+'
    else:
        mod = 'w+'

    with open(path, mod) as f:
        pprint.sorted = lambda x, key=None: x # disables sorting
        f.write(pprint.pformat(dict))

    if save_pkl:
        path_for_pkl = path.rsplit('.', 1)[0] + '.pkl'
        with open(path_for_pkl, 'wb+') as f:
            pickle.dump(dict,f)


def drop_key(dict, key_to_be_dropped):
    """Returns the input dictionary without the key_to_be_dropped, out of place."""

    if type(key_to_be_dropped)==str:
        if key_to_be_dropped in dict:
            return {key:dict[key] for key in dict if key!=key_to_be_dropped}
        else:
            return dict
    else: # List of keys to be dropped
        for key_in_list in key_to_be_dropped:
            dict = drop_key(dict, key_in_list)
        return dict


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def point_asdict(search_space_as_dict, point_as_list):

    return {key:val for key,val in zip(search_space_as_dict,point_as_list)}


def point_aslist(search_space_as_dict, point_as_dict):

    return [point_as_dict[key] for key in search_space_as_dict]


def str2bool(v):
    if v.lower() in ('true', 't', 'yes', 'y', '1'):
        return True
    elif v.lower() in ('false', 'f', 'no', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_str_combs(base, extension):
    fix = [base, extension]
    return [''.join(name) for name in itertools.chain.from_iterable([itertools.product(fix[i], ['','_'], fix[i+1]) for i in [0,-1]])]


def boolify(obj):
    return bool(obj.size if isinstance(obj, np.ndarray) else obj)


def set_auto_lr(params):

    def _get_auto_lr(optimizer_name, batch_size, range_factor=3):

        # Set scaling of learning rate based on optimizer
        if optimizer_name.lower() in ['nadam']:
            optimum_lr = 2.5*1e-5 * np.sqrt(batch_size)

        elif optimizer_name.lower() in ['padam']:
            optimum_lr = 1e-3 * np.sqrt(batch_size)

        elif optimizer_name.lower() in ['yogi']:
            optimum_lr = 3*1e-5 * np.sqrt(batch_size)

        else:
            raise NotImplementedError(f'Optimizer {optimizer_name} not implemented in get_auto_lr.')

        # Adjust the cyclical learning rate schedule to vary around the set value
        range_factor = 3

        return optimum_lr, [optimum_lr * range_factor**(-0.5),
                            optimum_lr * range_factor**(0.5)]

    if isinstance(params['optimizer'], dict):
        optimizer_name = params['optimizer']['class_name']
    else:
        optimizer_name = params['optimizer']
    lr, lr_schedule_range = _get_auto_lr(optimizer_name, params['batch_size'])
    if params['lr_schedule']['name'] is not None:
        params['lr_schedule']['range'] = lr_schedule_range
        if verbose:
            print('Learning rate range for learning rate schedule '
                  f'{params["lr_schedule"]["name"]} set to '
                  f'({params["lr_schedule"]["range"][0]:.5e}, '
                  f'{params["lr_schedule"]["range"][1]:.5e}) '
                  'by auto_lr.')
    else:
        if isinstance(params['optimizer'], dict):
            params['optimizer']['config']['lr'] = lr
        else:
            params['optimizer'] = {'class_name':params['optimizer'],
                                   'config':{'lr':lr}}
        if verbose:
            print('Learning rate has been set to  '
                  f'{params["optimizer"]["config"]["lr"]:.5e} by auto_lr.')

    return params


def get_default_params():
    """
    Returns a dictionary containing default parameters to be passed to the model
    container.

    Please see the README for documentation.
    """

    params = {
          # Training
          'epochs'                     : 1,
          'batch_size'                 : 32,
          'loss'                       : 'mse',
          'metrics'                    : None,
          'optimizer'                  : 'Nadam',
          'lr_finder'                  : {'use':False,
                                          'scan_range':[1e-4, 1e-2],
                                          'epochs':1,
                                          'prompt_for_input':False},
          'lr_schedule'                : {'name':None,
                                          'range':[1e-3,5e-3],
                                          'step_size_factor':5},
          'auto_lr'                    : False,

          # Misc.
          'use_earlystopping'          : False,
          'restore_best_weights'       : False,
          'pretrained_model'           : {'use':False,
                                          'weights_path':'./weights.h5',
                                          'params_path':None,
                                          'layers_to_load':[],
                                          'freeze_loaded_layers':[]},
          'n_gpus'                     : 0,
          'data_generator'             : {'use':False,
                                          'n_workers':1,
                                          'max_queue_size':10,
                                          'path':'./data.h5',
                                          'n_points':{'train':None, 'val':None, 'test':None}},
          'upsampling'                 : {'use':False,
                                          'wanted_size':(100,100),
                                          'interpolation':'nearest'},

          # Submodels
          'top'                        : {'initialization':'orthogonal',
                                          'activation':None,
                                          'normalization':None,
                                          'layer_reg':{},
                                          'dropout':None,
                                          'units':[64,1],
                                          'final_activation':None},
          'cnn'                        : {'initialization':'orthogonal',
                                          'activation':None,
                                          'normalization':None,
                                          'layer_reg':{},
                                          'dropout':None,
                                          'cnn_type':'simple',
                                          'conv_dim':2,
                                          'block_depths':[1],
                                          'n_init_filters':4,
                                          'init_kernel_size':5,
                                          'rest_kernel_size':3,
                                          'cardinality':1,
                                          'use_squeeze_and_excite':False,
                                          'globalavgpool':False,
                                          'downsampling':None,
                                          'min_size_for_downsampling':2},
          'scalar_net'                 : {'initialization':'orthogonal',
                                          'activation':None,
                                          'normalization':None,
                                          'layer_reg':{},
                                          'dropout':None,
                                          'units':[],
                                          'connect_to':[]},
          'FiLM_gen'                   : {'initialization':'orthogonal',
                                          'activation':None,
                                          'normalization':None,
                                          'layer_reg':{},
                                          'dropout':None,
                                          'use':False,
                                          'units':[64]},
          'track_net'                  : {'initialization':'orthogonal',
                                          'activation':None,
                                          'normalization':None,
                                          'layer_reg':{},
                                          'dropout':None,
                                          'phi_units':[64],
                                          'rho_units':[64],
                                          'connect_to':[]},
          'time_net'                   : {'initialization':'orthogonal',
                                          'activation':None,
                                          'normalization':None,
                                          'layer_reg':{},
                                          'dropout':None,
                                          'units':[],
                                          'use_res':False,
                                          'final_activation':None,
                                          'final_activation_init':[1.0],
                                          'merge_method':'concatenate'}
          }

    return params
