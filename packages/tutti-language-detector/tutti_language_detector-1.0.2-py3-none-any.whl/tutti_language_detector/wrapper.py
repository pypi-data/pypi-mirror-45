import pkg_resources
import re
import subprocess
import string
import unicodedata
from typing import List

import pandas as pd
import numpy as np

from sklearn.metrics import log_loss, accuracy_score

from logging import getLogger


logger = getLogger('VWMultiClassifier')


def remove_bad_chars(text: str) -> str:
    """
    Remove control characters from input string
    :param text: input string
    :type text: str
    :return: input text without control characters
    :rtype: str
    """
    text = text.replace('\n', ' ').translate(str.maketrans('', '', string.punctuation))
    return ''.join(ch for ch in text if unicodedata.category(ch) != 'Cc')


class VWMultiClassifier:
    """
    This class acts as a non-generic classifier for Vowpal Wabbit. It is non generic as it is specialised
    for the task of detecting tutti.ch ads language
    """
    params = dict()

    def __init__(self, random_seed: int = 42, ngram_size: int = 0, passes: int = 20, bit_precision: int = 25,
                 l2: float = 0, model: str = None, loss_function: str = 'logistic', multiclass: bool = False,
                 oaa: int = 0):
        """
        Constructor for the Vowpal Wabbit wrapper class that has methods for training/testing language datasets
        :param random_seed: random seed
        :param ngram_size: size of the N grams, if ngram_size=0 no N grams used
        :param passes: number of passes over the train set
        :param bit_precision: bit precision used by VW
        :param l2: L2 constraint to the model, if l2=0 the model is not regularized
        :param model: name of a model to load (NOTE: if model is loaded and no train is performed, the object will use
        this model to make predictions regardless of the rest of arguments in this constructor.)
        :param multiclass: flag that tells the model if there are more than 2 classes
        :param oaa: One Against All: number of classes to predict from (only relevant for multiclass=True)
        :param loss_function: loss function to use, the available values are the ones available to the vw binary
        """
        # Reset params
        self.params = {'quiet': True}

        # Params checks
        if ngram_size == 1:
            ngram_size = 0
        if multiclass:
            if oaa < 3:
                raise ValueError('If multiclass=True, oaa must be at least 3.')

        args = dict(locals())
        for k, v in args.items():
            if k != 'self' and k != '__class__' and v is not None:
                self.params[k] = v

    @staticmethod
    def get_pretrained_versions() -> List[str]:
        model_versions = ['0.0.1', '0.0.2']
        return model_versions

    @staticmethod
    def to_vw(df: pd.DataFrame, filepath: str = 'out.vw', columns: List[str] = None, target: str = None,
              tag: str = None) -> None:
        """
        Generic function to convert a pandas DataFrame into a Vowpal Wabbit formatted file. This function accepts
        features such as tags, string features and numeric features.
        NOTE:
         - This function supports only a single (optionally named) namespace.
         - This function expects the target to consist of integer labels (1, 2, ...), or (-1, 1) in case of binary
         classification. Otherwise VW won't work with the generated vw file
        Source: modified version of https://gist.github.com/maxpagels/6685efe304180e5a499540c85158b287
        :param df: input dataframe
        :param filepath: path to output file in Vowpal Wabbit format
        :param columns: list of columns to include into the output file (list of features, can include tag and
        target here too)
        :param target: name of the target column (if exists)
        :param tag: name of the tag column (if exists)
        :return: Nothing
        """
        if columns is None:
            columns = df.columns.tolist()
        if target in columns:
            columns.remove(target)
        if tag:
            columns.remove(tag)

        with open(filepath, 'w') as f:
            for _, row in df.iterrows():
                if target:
                    f.write('{target} '.format(target=row[target]))
                if tag:
                    f.write('\'{tag} '.format(tag=row[tag]))
                f.write('| ')
                last_feature = columns[-1]
                for idx, val in row.iteritems():
                    if idx not in columns:
                        continue
                    if isinstance(val, str):
                        f.write(remove_bad_chars(val))
                    elif isinstance(val, float) or isinstance(val, int):
                        if not np.isnan(val):
                            f.write('{name}:{value}'.format(name=idx.replace(' ', '_').replace(':', '_'),
                                                            value=val))
                        else:
                            continue
                    else:
                        f.write(val)
                    if idx != last_feature:
                        f.write(' ')
                f.write('\n')

    def fit(self, train_file: str, output_model: str = 'detect_oaa.model'):
        """
        Train a Vowpal Wabbit logistic One Against All classifier for 3 classes (languages) with settings
        :param train_file: train dataset in Vowpal Wabbit format
        :param output_model: name of output model file
        :return:
        """
        # Construction of fit command
        command = ['vw']
        if self.params['multiclass']:
            command.append('--oaa={}'.format(self.params['oaa']))
        if self.params['ngram_size'] > 1:
            command.append('--ngram={}'.format(self.params['ngram_size']))
        command = command + [
            '--data={}'.format(train_file),
            '--loss_function={}'.format(self.params['loss_function']),
            '--final_regressor={}'.format(output_model),
            '--cache',
            '--passes={}'.format(self.params['passes']),
            '--bit_precision={}'.format(self.params['bit_precision'])
        ]
        if self.params['l2'] != 0:
            command.append('--l2={}'.format(self.params['l2']))
        command.append('--random_seed={}'.format(self.params['random_seed']))

        # Run fit command
        out = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', check=True)
        logger.debug(out.stdout)

        # Store model in class
        self.params['model'] = output_model

    def load_model(self, model_name: str, loss_function: str = None) -> None:
        """
        Load a model file into the class to use for predictions
        :param model_name: name of the file that contains the VW model
        :param loss_function: loss_function used in the loaded model
        :return: nothing
        """
        self.params['model'] = model_name
        if loss_function:
            self.params['loss_function'] = loss_function

    @classmethod
    def test_model(cls, model: str, predictions_file: str, test_file: str, probabilities: bool = True):
        """
        Test given model against a test file and return a performance metric
        :param model: Vowpal Wabbit model to test
        :param predictions_file: name of the file to output the resulting predictions/probabilities
        :param test_file: path to test file in Vowpal Wabbit format
        :param probabilities: whether the model has to return probabilities for each class or just prediction (NOTE:
        probability output needs loss_function=logistic. If the model was not trained with this parameter the behaviour
        of this option could be unexpected).
        :return: cross entropy score for probabilities=True or accuracy score for probabilities=False
        """
        # Set command
        command = [
            'vw',
            '--initial_regressor={}'.format(model),
            '--testonly',
            '--data={}'.format(test_file)
        ]
        if probabilities:
            command = command + [
                '--loss_function=logistic',
                '--probabilities'
            ]
        command = command + [
            '--predictions={}'.format(predictions_file),
            '--quiet'
        ]
        # Run command
        subprocess.run(command, check=True, stdout=subprocess.PIPE)

        # Compute metric from output
        y_true = cls.read_labels_from_vw_file(test_file)
        class_labels = np.unique(y_true)
        logger.debug('Detected classes: {}'.format(class_labels))
        if probabilities:
            y_pred = cls.read_vw_probabilities(filename=predictions_file, labels=class_labels)
            logger.debug('Model predictions: \n{}'.format(y_pred))
            return log_loss(y_true=y_true, y_pred=y_pred, labels=class_labels)
        else:
            y_pred = cls.read_vw_predictions(filename=predictions_file)
            return accuracy_score(y_true=y_true, y_pred=y_pred)

    @staticmethod
    def read_labels_from_vw_file(filename: str) -> np.array:
        """
        Read labels from a test file
        :return: array of labels in file
        """
        with open(filename, 'r') as fd:
            labels = []
            for line in fd.readlines():
                labels.append(int(line[0]))
        return np.array(labels).reshape(-1, 1).astype(int)

    @staticmethod
    def read_vw_predictions(filename: str) -> np.array:
        """
        Read class predictions from result file (generated by test_model with probabilities=False)
        :return: array of predictions
        """
        with open(filename, 'r') as fd:
            predictions = [int(label) for label in fd.readlines()]
        return np.array(predictions).reshape(-1, 1).astype(int)

    @staticmethod
    def read_vw_probabilities(filename: str, labels) -> np.array:
        """
        Read probabilities from Vowpal Wabbit for N classes and create a DataFrame containing the values
        :param filename: name of the file to read predictions from
        :param labels: (array or list-like) with labels
        :returns: array of probabilities
        """
        with open(filename, 'r') as fd:
            rows = []
            for line in fd.readlines():
                probs = [float(x) for x in re.findall(r'\d+\.\d+', line)]
                rows.append(dict(zip(labels, probs)))
        logger.debug('Returned values: \n{}'.format(pd.DataFrame(rows).values))
        return pd.DataFrame(rows).values

    def predict(self, nclasses: int, input_data: str = None, batch: bool = False):
        """
        Use the loaded model to detect the language of a string or to batch predict an input file
        :param nclasses: number of possible different classes expected in the prediction
        :param input_data: either a string (in Vowpal Wabbit format) for the example (i.e. a phrase in German,
        Italian or French) or a file name (for batch mode)
        :param batch: flag to indicate if we are doing single example detection or batch detection from file
        :return: prediction(s) for the input value(s)
        """
        if 'model' not in self.params.keys():
            raise AttributeError('{} object needs to have a loaded model to predict.'
                                 'Call load_model method'.format(self))

        model = self.params['model']
        logger.debug('Model is {}'.format(model))
        if batch:
            output_file = '/tmp/vw-language-model-output.vw'
            command = [
                'vw',
                '--initial_regressor={}'.format(model),
                '--testonly',
                '--data={}'.format(input_data),
                '--loss_function=logistic',
                '--probabilities',
                '--predictions={}'.format(output_file),
                '--quiet'
            ]
            subprocess.run(command, check=True)
            logger.debug('VW command: {}'.format(' '.join(command)))
            probs_df = self.read_vw_probabilities(filename=output_file, labels=np.arange(nclasses))
        else:
            # Create stdin process to act as input file
            tmp_input = subprocess.Popen(('echo', '{}'.format('| ' + remove_bad_chars(input_data))),
                                         stdout=subprocess.PIPE)
            # Generate command
            command = [
                'vw',
                '--initial_regressor={}'.format(model),
                '--testonly',
                '--data=/dev/stdin',
                '--loss_function=logistic',
                '--probabilities',
                '--predictions=/dev/stdout',
                '--quiet'
            ]
            logger.debug('VW command: {}'.format(' '.join(command)))
            # Run command
            output = subprocess.run(command, check=True, stdin=tmp_input.stdout, stdout=subprocess.PIPE)
            # Read output of command
            line = output.stdout.decode('utf-8')
            # Get prediction and probability from command output
            probs = [float(x) for x in re.findall(r'\d+\.\d+', line)]
            rows = [dict(zip(np.arange(len(probs)), probs))]
            probs_df = pd.DataFrame(rows).values

            logger.debug('rows = {}'.format(rows))

        # TODO: fix me
        probability_df = pd.DataFrame(probs_df)
        logger.debug('probability_df = \n{}'.format(probability_df.to_string()))
        predicted_language_idx = probability_df.idxmax(axis=1).values + 1
        predicted_language_prob = probability_df.max(axis=1).values
        df = pd.DataFrame({'predicted_language': predicted_language_idx, 'probability': predicted_language_prob})
        logger.debug('df = \n{}'.format(df.to_string()))
        return df


class VWPretrainedModel(VWMultiClassifier):
    """
    This is a class derived from VWMultiClassifier that loads one of the pretrained models that come with the package
    """
    lang_codes = {1: 'de', 2: 'it', 3: 'fr'}

    def __init__(self, version: str = None):
        """
        Create a VWMultiClassifier object with a preloaded model using one of the pre-trained models included in the
        python package. The version of the model can be specified in the constructor.
        This pre-trained model works with German, Italian and French, and uses the labels
            { 'german': 1, 'italian': 2, 'french': 3 }
        :param version: version of the model to load. Must be in the list of versions provided by
        get_pretrained_versions()
        """
        if version:
            if version not in self.get_pretrained_versions():
                raise ValueError('The specified model version does not exist')
        else:
            version = self.get_pretrained_versions()[0]

        resource_package = __name__
        resource_path = '/'.join(('models', 'vw-{}.model'.format(version)))
        filepath = pkg_resources.resource_filename(resource_package, resource_path)
        pretrained_model_path = filepath
        super().__init__(model=pretrained_model_path, random_seed=42)

    def to_lang_code(self, lang_index: int) -> str:
        return self.lang_codes[lang_index]

    def predict(self, nclasses: int = 3, input_data: str = None, batch: bool = False):
        result = super().predict(nclasses=nclasses, input_data=input_data, batch=batch)
        # TODO: apply transformation to language code to the whole result (and make it work for both single and batch)
        result['predicted_language'] = result['predicted_language'].apply(lambda x: self.to_lang_code(x))
        return result
