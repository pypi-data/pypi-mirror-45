'''
Handling Drever testvector files module.
'''
import numpy as np


class FileHandler():
    '''
    classdocs
    '''

    @classmethod
    def get_ppm_info(cls, data):
        '''
        Extracts PPM image information from Numpy data array

        Parameters:
        data (ndarray): 2D array with single channel or data triplet (RGB)

        Return:
        dict: PPM image information
        '''

        ppm_info = dict()

        data_dim = len(data.shape)

        assert data_dim in (2, 3), "Wrong data dimension: " + str(data_dim)

        ppm_info['width'] = data.shape[1]
        ppm_info['height'] = data.shape[0]
        ppm_info['mode'] = "RGB" if data_dim == 3 else "GRAY"

        assert data.dtype in (np.uint8, np.uint16), \
            "Wrong unsigned integer type (neither uint8 or uint16)"

        if data.dtype == np.uint8:
            ppm_info['bitdepth'] = 8
        else:
            ppm_info['bitdepth'] = 16

        if ppm_info['bitdepth'] == 8:
            assert data.dtype == np.uint8, "Data is none 8bit type!"

        ppm_info['max_value'] = 2**ppm_info['bitdepth'] - 1

        return ppm_info

    @classmethod
    def create_ppm_header(cls, ppm_info):
        '''
        Create PPM header. currently only P2 and P3 are supported.

        Parameters:
        ppm_info (dict): PPM image information

        Return:
        str: String with header content
        '''

        if ppm_info['mode'] == "GRAY":
            header = "P2\n"
        else:
            header = "P3\n"

        header += str(ppm_info['width']) + " " + str(ppm_info['height']) + "\n"
        header += str(ppm_info['max_value']) + "\n"

        return header

    @classmethod
    def store_ppm_image(cls, data, path):
        '''
        Stores numpy arrays as ppm file. Elements are stored as 16 bit pixel
        data.

        Parameters:
        data (ndarray): 2D array with single channel or data triplet (RGB)
        path (str): Path of output file
        '''

        ppm_info = cls.get_ppm_info(data)
        ascii_size = 6 if (ppm_info['bitdepth'] == 16) else 4

        header = cls.create_ppm_header(ppm_info)

        ppm_file = open(path, "w")
        ppm_file.write(header)

        for row in range(0, ppm_info['height']):

            line = ""

            for col in range(0, ppm_info['width']):

                value = ""

                if ppm_info['mode'] == "GRAY":
                    value = str(data[row, col]).rjust(ascii_size, " ")
                else:
                    for rgb in range(0, 3):
                        data_str = str(data[row, col, rgb])
                        value += data_str.rjust(ascii_size, " ")

                line += value

            ppm_file.write(line + "\n")

        ppm_file.close()
