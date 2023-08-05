import numpy as np
from scipy import sparse
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from mpl_toolkits.axes_grid1 import make_axes_locatable

from . import utilities as utili


##### funcs for plotting
def shift_map_matr(coordinates_array):
    coordinates_array[:, 0] = coordinates_array[:, 0] - min(coordinates_array[:, 0])
    coordinates_array[:, 1] = coordinates_array[:, 1] - min(coordinates_array[:, 1])
    return coordinates_array

def map_scan_plot(coordinates, values):
    no_fits = len(list(values.values())[0])
    figs = []
    data = []
    for i in range(no_fits):
        X = []
        Y = []
        Z = []
        for key in values.keys():
            x, y = coordinates[key]
            z = values[key][i]
            X.append(x)
            Y.append(y)
            Z.append(z)
        x_step = np.unique(X)[1] - np.unique(X)[0]
        xx = (np.round(X / x_step)).astype(int)
        y_step = np.unique(Y)[1] - np.unique(Y)[0]
        yy = np.round((Y / y_step)).astype(int)
        data_ = sparse.coo_matrix((Z, (xx, yy))).toarray()
        data.append(data_)
        f = plt.figure()
        ax = plt.gca()
        im = plt.imshow(data_, cmap='magma', extent=[min(X), max(X), max(Y), min(Y)], vmin=data_.min(),
                        vmax=data_.max())
        plt.xlabel('x coordinates')
        plt.ylabel('y coordinates')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        # f.tight_layout()
        figs.append(f)
    return figs

def plot_map_scan(bag, fit_params, dirname):
    coordinates_array = np.array(list(bag.coordinates.values()))  # convert coordinates for each point into an array
    coordinates_array = shift_map_matr(
        coordinates_array)  # shift so that each coordinate starts at 0, not normalised
    for i, key in enumerate(bag.coordinates):
        bag.coordinates[key] = coordinates_array.tolist()[i]  # reassign in the correct format
    while True:
        ans = input("making map scans, please input which property you would like to scan. options are:"
                    f"\n {[p_ for p_ in fit_params.keys()]}. or type e to exit")
        if ans == 'e':
            break
        else:
            try:
                p = ans
                plot = map_scan_plot(bag.coordinates, fit_params[p])
                for i, pt in enumerate(plot):
                    try:
                        cents = next(iter(fit_params['center'].values()))
                        pt.suptitle(f'{p}_{i}_heatmap. peak {i} is centered at: {cents[i]}')
                    except KeyError:
                        print("tried to add label for peak centers onto graph, but couldn't fetch the right variable")
                        pt.suptitle(f'{p}_{i}_heatmap')
            except KeyError:
                p = ''
                plot = None
                print('wrong answer entered, trying again!')
            try:
                for i, pt in enumerate(plot):
                    utili.save_plot(pt, path=dirname, figname=f"{p}_{i}.svg")
                pt.close()
            except AttributeError:
                print("Tried to save plot but there is no plot yet! Somethuing wen't wrong in making the plot")
#####