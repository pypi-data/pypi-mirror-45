import os
import tempfile
from shutil import copyfile


def copy_pitch_data_to_temp(name='soccar'):
    pitch_data = os.path.join(os.path.dirname(os.path.realpath(__file__)), name + '.dat')
    destination = os.path.join(tempfile.gettempdir(), 'rlbot-pitch.dat')
    copyfile(pitch_data, destination)
