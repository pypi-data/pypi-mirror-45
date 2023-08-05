import numpy as np
import keras as ks
import keras.backend as K
from .utils import load_data, boolify


class DataGenerator(ks.utils.Sequence):
    '''Generates data for Keras.

    From https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly'''

    def __init__(self, set_name, data_snippet, load_params, n_samples, batch_size, predict=False, shuffle=True):
        'Initialization'
        self.set_name = set_name
        self.data_snippet = data_snippet
        self.load_params = load_params
        self.n_samples = n_samples
        self.batch_size = batch_size
        self.indices = np.arange(self.n_samples)
        self.predict = predict
        self.shuffle = shuffle
        self.on_epoch_end()


    def __len__(self):
        'Denotes the number of mini-batches per epoch'
        return int(np.ceil(self.n_samples / self.batch_size)) # NOTE: Was originally np.floor()


    def __getitem__(self, index):
        '''Generate one batch of data.

        index is the mini-batch index (the last index is self.__len__())
        '''

        # Generate indices of the batch
        batch_indices = self.indices[index*self.batch_size:(index+1)*self.batch_size]

        return self._generate_data(batch_indices)


    def on_epoch_end(self):
        'Updates indices after each epoch'
        if self.shuffle == True:
            np.random.shuffle(self.indices)


    def _generate_data(self, batch_indices):
        'Generates data containing batch_size samples'

        # Modify n_points to have the batch_indices
        n_points = {self.set_name:batch_indices}

        # Load the wanted the data
        data = load_data(**self.load_params, verbose=False)

        # Organize the data into lists of the form that the Keras model expects
        return self._organize_data(data, self.set_name)


    def _organize_data(self, data, set_name):
        '''Data should be added in the same order as inputs.'''

        x = []

        if 'images' in self.data_snippet['train'] and boolify(self.data_snippet[set_name]['images']):
            # Images
            for img_name in self.data_snippet[set_name]['images']:
                x.append(self.data_snippet[set_name]['images'][img_name])

        # Scalars
        if 'scalars' in self.data_snippet['train'] and boolify(self.data_snippet[set_name]['scalars']):
            x.append(self.data_snippet[set_name]['scalars'])

        # Tracks
        if 'tracks' in self.data_snippet['train'] and boolify(self.data_snippet[set_name]['tracks']):
            x.append(self.data_snippet[set_name]['tracks'])

        # Targets
        y = self.data_snippet[set_name]['targets']

        if self.predict:
            return x
        else:
            if 'sample_weights' in self.data_snippet['train'] and boolify(self.data_snippet[set_name]['sample_weights']):
                sample_weights = data[set_name]['sample_weights']
                return x, y, sample_weights
            else:
                return x, y
