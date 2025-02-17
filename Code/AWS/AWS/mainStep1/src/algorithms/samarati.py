from itertools import product
import pandas as pd
from utils.loss_metrics import categorical_loss_metric
from operator import itemgetter


class Lattice():
    def __init__(self, hierarchies, quasi_id, heights):
        self.hierarchies = hierarchies
        self.heights = heights
        self.total_height = sum(heights.values())
        self.attr_num = len(self.heights)
        self.quasi_id = quasi_id
        self.height_array = [list(range(h + 1)) for h in self.heights.values()]
        self.lattice_map = self.build_map()

    def build_map(self):
        lattice_map = {h: [] for h in range(self.total_height + 1)}
        all_combinations = [x for x in product(*self.height_array)]
        for dist in all_combinations:
            temp = sum(dist)
            if temp <= self.total_height:
                lattice_map[temp].append(dist)
        print('\nlattice_map:\n', lattice_map)
        return lattice_map
    
    def get_vectors(self, height):
        return self.lattice_map[height]

    def satisfies(self, vector, k, table, maxsup):
        # generalization
        anonymized_table = self.generalization(table, vector)        
        # suppression & validation
        valid, anonymized_table, sup = self.validation(anonymized_table, k, maxsup)
        return valid, sup, anonymized_table

    def generalization(self, table, vector):
        table = table.copy()
        for attribute, gen_level in zip(self.quasi_id, vector):
            col = [str(elem) for elem in list(table[attribute])]
            # find the ancestors for generalization
            ancestors = {k: k for k in [elem for elem in list(set(col))]}
            for k in ancestors.keys():
                for _ in range(gen_level):
                    ancestors[k] = self.hierarchies[attribute][ancestors[k]]
            # replace old values
            col = [ancestors[elem] for elem in col]
            table[attribute] = col

        return table

    def validation(self, table, k, maxsup):
        sup = 0
        table = table.copy()
        anonymized_table = pd.DataFrame(columns=table.columns)
        while sup <= maxsup and not table.empty:
            first_row = table.loc[table.index[0], self.quasi_id]
            row_counts = table.shape[0]
            # delete tuples with same qi values as the 1st row
            conditions = False
            for attr in self.quasi_id:  # at least 1 qi is different
                conditions |= (table[attr] != first_row[attr])
            # suppress unsatisfied tuples
            residual_table = table[~conditions]
            table = table[conditions]
            new_row_counts = table.shape[0]
            # judge maxsup
            delta = row_counts - new_row_counts
            if (delta < k):
                sup += delta
            else:
                anonymized_table = anonymized_table._append(residual_table)
        return sup <= maxsup, anonymized_table, sup