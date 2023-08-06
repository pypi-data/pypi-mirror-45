import matplotlib.pyplot as plt
from os.path import basename
from ast import literal_eval
import numpy as np

from . import utilities
from . import parsing
from . import multi_obj
from . import thundobj

def main():
    args = parsing.parse_user_args()

    arguments = parsing.using_user_args(args)

    if arguments['map']:
        try:  # a user can pass in a list of filenames or just one
            file_name = basename(literal_eval(arguments['datapath'])[0])
        except SyntaxError:  # assume its just a string and not a list passed
            file_name = None
            log_name = arguments['datapath']
            arguments['datapath'] = f"['{arguments['datapath']}',]"  # as this is what multiobj needs
        bag = multi_obj.main(arguments)  # create a Thunder object

        bag.choose_spectrum() # get the user to choose which spectrum to create params from
        thund = bag.thunder_bag[bag.first]
    else:
        thund = thundobj.main(arguments)  # create a Thunder object

    sharpening_factor = (0, 0)
    res_enhanced = thund.y_data
    while True:
        plt.plot(thund.x_data, res_enhanced)
        print(f"Do you want to sharpen the peaks to help find components? Note this will not edit the actual data. "
              f"Current sharpening factor is: {sharpening_factor}")
        plt.show()
        ans = input("Please enter the method (either 'power' or 'deriv'), then a comma, then a new sharpening factors "
                    "(comma seperated if mutliple i.e. for derivative), "
                    "or type y to continue with the current factor")
        if ans == 'y':
            break
        else:
            try:
                ans = ans.split(',')
                type = ans[0]
                ans = ans[1:]
                sharpening_factor = [float(fac) for fac in ans]
                if type == 'power':
                    res_enhanced = thund.y_data ** sharpening_factor[0] # raise to the power
                elif type == 'deriv':
                    y_double_prime = np.pad(np.diff(thund.y_data, n=2), (0, 2), 'constant')
                    y_4_prime = np.pad(np.diff(thund.y_data, n=4), (0, 4), 'constant')
                    res_enhanced = thund.y_data - sharpening_factor[0] * y_double_prime + sharpening_factor[
                        1] * y_4_prime  # this is the original data minus its
                    # derivative multiplied by some factor
                else:
                    raise ValueError("enter a correct type")
            except:
                print("You entered an incorrect answer! Trying again...")
    plt.close()


    cents = []
    while True:
        plt.plot(thund.x_data, thund.y_data)
        for xc in cents:
            plt.axvline(x=xc)
        print(f"First looking at peak center values, look at the following plot with centers at values:"
              f"{cents}")
        plt.show()
        ans = input("Please enter a list of values e.g. 1,2,3 etc. or type y if happy with these values")
        if ans == 'y':
            break
        else:
            try:
                cents = ans.split(',')
                cents = [float(i) for i in cents]
            except:
                print("You entered an incorrect answer! Trying again...")
    plt.close()

    amps = []
    while True:
        plt.plot(thund.x_data, thund.y_data)
        if len(amps) == len(cents):
            plt.plot(cents, amps, 'r*')
        else:
            for yc in amps:
                plt.axhline(y=yc)
        print(f"First looking at peak center values, look at the following plot with amps at values:"
              f"{amps}")
        plt.show()
        ans = input("Please enter a list of values e.g. [1,2,3] etc. or type y if happy with these values")
        if ans == 'y':
            break
        else:
            try:
                amps = ans.split(',')
                amps = [float(i) for i in amps]
            except:
                print("You entered an incorrect answer! Trying again...")
    plt.close()

    widths = []
    while True:
        plt.plot(thund.x_data, thund.y_data)
        if len(widths)%2:
            for width in widths:
                plt.axvline(x=width)
        else:
            for band in range(len(widths)//2):
                plt.axvspan(widths[2*band], widths[2*band + 1], alpha=0.1, color='red')
        print(f"First looking at peak center values, look at the following plot with widths at values:"
              f"{widths}")
        plt.show()
        ans = input("Please enter a list of values e.g. [1,2,3] etc. or type y if happy with these values")
        if ans == 'y':
            break
        else:
            try:
                widths = ans.split(',')
                widths = [float(i) for i in widths]
            except:
                print("You entered an incorrect answer! Trying again...")
    plt.close()
    widths = [abs(widths[2*i+1]-widths[2*i]) for i in range(len(widths)//2)]

    params = {"peak_centres":cents, "peak_amps":amps, "peak_widths":widths}
    utilities.save_fit_report(params, './', 'generated_params.txt')

