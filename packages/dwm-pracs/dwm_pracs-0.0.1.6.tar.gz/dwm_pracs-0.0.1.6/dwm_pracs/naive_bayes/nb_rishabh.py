# coding=utf-8
from typing import Iterator
from csv import DictReader
from collections import Counter


def get_csv_data(file_name: str) -> Iterator[list]:
    """
    This returns the csv file data in dict format.
    file_name: str
    Assumptions:
          1) file is a csv
          2) file exists
          3) file has utf8 encoding.
    """
    with open(file_name) as f:
        # creating a reader instance that can iterate over rows of file.
        reader = DictReader(f)

        # iterating over rows:
        for row in reader:
            yield dict(row)  # returning the dicts for each row in the dataset.


def ld_to_dl(ld: list):
    """
    @ld: list of dictionaries
    This function converts the list of dicts to dict of list as values
    Basically, merges all the dict with same header in key:list(values) pairs.
    Assumptions:
        1) all the dicts in the list have same and all the keys.
    """
    return {key: [dic[key] for dic in ld] for key in ld[0]}


def get_probabilities(l) -> dict:
    """
    l: list of atomic countables arithmetic values.
    Returns probability of each unique element in the given list.
    Assumptions:
        1) No missig values in the passed vector/list/iterable.
        2) All the elements in the given iterable are real numbers.
    """
    freq = Counter(l)
    sum_all_elements = sum(freq.values())
    probs = {key: value / sum_all_elements for key, value in freq.items()}
    return probs


def prob_table(feat_list, target_list):
    """
    feat_list: list of values of feature whose freq table is to be created.
    target_list: list of values in target feature.
    Returns the frequencies of occurence of each element 
      in the list of features of getting a unique values from target_list.
    """

    feat_to_target = tuple(zip(feat_list, target_list))

    ''' Finding the frequency of all the unique class in feat that 
        maps to a specific value in target column.'''
    freq_tbl = dict(Counter(feat_to_target))

    # finding the probability of occurence of tar_val when feat_val is given
    # ∀(tar_val ∈ target_list)  and  ∀(feat_val ∈ feat_list)
    prob_tbl = {key: value / target_list.count(key[-1]) for key, value in freq_tbl.items()}

    return prob_tbl


class NaiveBayes(object):
    def __init__(self, dataset, target_name):
        # binding all the objects to the class instance(object).
        self.dataset = dataset
        self.target_name = target_name
        self.target_probabilities = None
        self.probabilities = None

    def fit(self, target_list=None):
        """
        dataset: dict of feature_name: [*feature_values]
        """
        # building the target list object if not provided.
        if target_list is None:
            target_list = self.dataset[self.target_name]

        # get and set probabilities for all the unique values in the target.
        target_probabilities = get_probabilities(target_list)
        self.target_probabilities = target_probabilities

        # making the frequency table for each feature in the dataset.
        probabilities = {feat_name: prob_table(self.dataset[feat_name], target_list) for feat_name in self.dataset if
                         feat_name != target_name}

        # setting the prob_table to class instance.
        self.probabilities = probabilities

    def predict(self, input_data: dict)-> str:
        """
        Returns the class of target with max probability wrt input_data
        input_data: dict of class:value
        """
        if self.probabilities is None or self.target_probabilities is None:
            raise ValueError('You need to fit the data first!!')

        # This will store target:probability for given dataset.
        all_probs = {}  # a dict.

        # iterating all the target classes to find probab.. of it's occurence.

        for uniq_target_name in set(self.dataset[self.target_name]):
            probability = 1
            for feat_name in input_data:
                probability *= self.probabilities[feat_name][(input_data[feat_name], uniq_target_name)]
            probability *= self.target_probabilities[uniq_target_name]

            all_probs[probability] = uniq_target_name
        return all_probs[max(all_probs)]


if __name__ == '__main__':
    file_name = 'dataset.csv'
    target_name = 'Stolen'

    # extracting data from csv file.
    data = list(get_csv_data(file_name))  # data is a list of dicts.

    # getting data in a dict.
    dict_data = ld_to_dl(data)

    # making a classifier object.
    nb = NaiveBayes(dict_data, target_name)

    # Fitting the data passed to classifier object.
    nb.fit()

    # a random example:
    unseen_sample = dict(Color='Red', Type='SUV', Origin='Domestic')
    prediction = nb.predict(unseen_sample)

    print('Unseen sample: {}'.format(unseen_sample))
    print('Predicted Value:{}'.format({target_name: prediction}))
