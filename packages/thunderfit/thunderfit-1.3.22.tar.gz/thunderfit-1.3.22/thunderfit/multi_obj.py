import logging
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

from glob import glob
from copy import deepcopy
from pandas.errors import ParserError
from tqdm import tqdm
from ast import literal_eval


from .thundobj import Thunder
from . import utilities as utili

############## NOT IMPLEMENTED!
# TODO
# make option of passing in many params files - one for each data file

class ThunderBag():

    def __init__(self, input):
        # initialise everything first
        self.thunder_bag: {} = {}
        self.coordinates: {} = {}

        if isinstance(input, Thunder):  # if only pass one but its already a thunder object then just use that
            self.thunder_bag[0] = Thunder(input)  # add all the details in depending on args
        elif isinstance(input, dict):
            self.create_bag(input)  # add all the details in depending on args
        else:
            raise TypeError('Cannot convert input to ThunderBag object')

    def create_bag(self, inp):
        self.x_ind =  inp.get('x_ind', None)
        self. y_ind = inp.get('y_ind', None)
        self.e_ind = inp.get('e_ind', None)
        self.img_path = inp.get('imgpath', None)
        self.coordinates = inp.get('coords', {})

        self.map = inp.get('map', None) # if user passes map as True then the file will be treated as a map file

        data_paths = inp.get('datapath', None)
        self.datapath = literal_eval(data_paths) # this is a bit dangerous!!!!!

        for i, data in tqdm(enumerate(self.datapath)):
            if len(self.datapath):
                prefix = f'{i}_'  # if more than one datapath then we name them with i_j
            if isinstance(data, Thunder):
                self.thunder_bag[i] = data
            elif isinstance(data, str):
                # then read the data file
                if self.map == True:
                    prefix = ''
                    self.x_coord_ind, self.y_coord_ind = inp.get('x_coord_ind', 0), inp.get('y_coord_ind', 1)
                    map_path = glob(data)[0] # save the filepath to the mapscan as self.map for later
                    x_data, y_data, x_coords, y_coords = self.read_map(map_path, self.x_ind, self.y_ind, self.x_coord_ind, self.y_coord_ind)

                    for j in range(len(x_data)): # go through the list of x_data
                        x_data_, y_data_ = x_data[j], y_data[j] # the x and y data for each coordinate set
                        self.thunder_bag[f'{prefix}{j}'] = Thunder(inp, x_data=x_data_, y_data=y_data_) # make a thunder obj
                                                                                                    # with this data
                        x_coords_, y_coords_ = x_coords[j], y_coords[j]
                        self.coordinates[f'{prefix}{j}'] = (x_coords_, y_coords_)  # for each i we will have a list of tuples of x and y coords
                elif '*' in data:
                    filematches = glob(data)
                    for j, file in enumerate(filematches):
                        try:
                            self.thunder_bag[f'{prefix}{j}'] = self.create_thunder(file, inp) # make a thunder object for each file
                        except ParserError as e:
                            logging.warning(f"A Thunder object could not be created for the datafile: {file}, skipping")
                else:
                    try:
                        self.thunder_bag[str(i)] = self.create_thunder(data, inp)
                    except ParserError as e:
                        logging.warning(f"A Thunder object could not be created for the datafile: {file}, skipping")
            else:
                logging.warning(f"wrong format in data list detected for {i}th element: {data}. Skipping element")
                pass

    @staticmethod
    def create_thunder(file, inp):
        arguments = deepcopy(inp)
        arguments['datapath'] = file
        thund_obj = Thunder(arguments)
        return thund_obj

    @staticmethod
    def read_map(file_address, x_ind, y_ind, x_coord_ind, y_coord_ind):
        x_data, y_data, _ = utili.load_data(file_address, x_ind, y_ind)  # load the data. note these drop nan rows but
                                    # does that for the whole filepath so will be consistent for data and coordinates
        x_coords, y_coords, _ = utili.load_data(file_address, x_coord_ind, y_coord_ind)  # load the coordinates
        x_data, y_data, x_coords, y_coords = utili.map_unique_coords(x_data, y_data, x_coords, y_coords) #

        return x_data, y_data, x_coords, y_coords

    @staticmethod
    def bag_iterator(bag, func, input_args, sett_args):
        bagkeys = tqdm(bag.keys())
        bagkeys.set_description(f"Operating with: {func.__name__}, to find: {sett_args}")
        for key in bagkeys:
            thund = bag[key]
            kwargs_ = [getattr(thund, arg) for arg in input_args]
            _, val = utili.apply_func((key, kwargs_), func)
            for i, arg in enumerate(sett_args):
                try:
                    setattr(thund, arg, val[i])
                except KeyError as e:
                    if isinstance(val, dict):
                        setattr(thund, arg, val)
                    else:
                        print(f'Weird KeyError encountered: {e}')


def main(arguments):
    bag = ThunderBag(deepcopy(arguments)) # load object
    return bag
