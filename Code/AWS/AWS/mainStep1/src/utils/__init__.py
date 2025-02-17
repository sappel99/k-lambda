def display_table(table):
    print('\n====================')
    print('anonymized table:\n', table)
    print('====================\n')


default_data_config = {
    'path': 's3://samarati/data/10k_3QI_output_1.csv',
    # QI for samarati
    'samarati_quasi_id': ['AGE', 'BIRTHDATE', 'GENDER'],
    'sensitive': 'DESCRIPTION',    
    'columns': ['ID', 'BIRTHDATE', 'AGE', 'SSN', 'DRIVERS', 'PASSPORT',	'PREFIX', 'SUFFIX', 'MAIDEN', 'MARITAL', 'GENDER', 'ADDRESS', 'DESCRIPTION'],
    'samarati_generalization_type': {
        'AGE': 'range',
        'BIRTHDATE': 'range',
        'GENDER': 'categorical',
    },
    'hierarchies': {
        'AGE': None,  # range type generalization
        'BIRTHDATE': None,  # range type generalization
#        'BIRTHDATE': 'data/my_adult_birthdate.txt',
        'GENDER': 's3://samarati/data/my_adult_gender.txt',
    },
}

#default_data_config = {
#    'path': 's3://samarati/data/10k_6QI_output_1.csv',
#    # QI for samarati
#    'samarati_quasi_id': ['BIRTHDATE', 'AGE', 'RACE', 'ETHNICITY', 'GENDER', 'BIRTHPLACE'],
#    'sensitive': 'DESCRIPTION',    
#    'columns': ['ID', 'BIRTHDATE', 'AGE', 'SSN', 'DRIVERS', 'PASSPORT', 'PREFIX', 'SUFFIX', 'MAIDEN', 'MARITAL', 'RACE', 'ETHNICITY', 'GENDER', 'BIRTHPLACE', 'ADDRESS', 'DESCRIPTION'],
#    'samarati_generalization_type': {
#        'AGE': 'range',
#        'BIRTHDATE': 'range',
#        'RACE': 'categorical',
#        'ETHNICITY': 'categorical',
#        'GENDER': 'categorical',
#        'BIRTHPLACE': 'categorical',
#    },
#    'hierarchies': {
#        'AGE': None,  # range type generalization
#        'BIRTHDATE': None,  # range type generalization
##        'BIRTHDATE': 's3://samarati/data/my_adult_birthdate.txt',
#        'RACE': 's3://samarati/data/my_adult_race.txt',
#        'ETHNICITY': 's3://samarati/data/my_adult_ethnicity.txt',
#        'GENDER': 's3://samarati/data/my_adult_gender.txt',
#        'BIRTHPLACE': 's3://samarati/data/my_adult_birthplace.txt',
#    },
#}

#default_data_config = {
#    'path': 's3://samarati/data/10k_9QI_output_1.csv',
#    # QI for samarati
#    'samarati_quasi_id': ['BIRTHDATE', 'DEATHDATE', 'AGE', 'FIRST', 'LAST', 'RACE', 'ETHNICITY', 'GENDER', 'BIRTHPLACE'],
#    'sensitive': 'DESCRIPTION',    
#   'columns': ['ID', 'BIRTHDATE', 'DEATHDATE', 'AGE', 'SSN', 'DRIVERS', 'PASSPORT', 'PREFIX', 'FIRST', 'LAST', 'SUFFIX', 'MAIDEN', 'MARITAL', 'RACE', 'ETHNICITY', 'GENDER', 'BIRTHPLACE', 'ADDRESS', 'DESCRIPTION'],
#   'samarati_generalization_type': {
#        'AGE': 'range',
#        'BIRTHDATE': 'range',
#        'DEATHDATE': 'range',
#        'FIRST': 'categorical',
#        'LAST': 'categorical',
#        'RACE': 'categorical',
#        'ETHNICITY': 'categorical',
#        'GENDER': 'categorical',
#        'BIRTHPLACE': 'categorical',
#    },
#    'hierarchies': {
#        'AGE': None,  # range type generalization
#        'BIRTHDATE': None,  # range type generalization
#        'DEATHDATE': None,  # range type generalization
#        'FIRST': 's3://samarati/data/my_adult_first.txt',
#        'LAST': 's3://samarati/data/my_adult_last.txt',
#        'RACE': 's3://samarati/data/my_adult_race.txt',
#        'ETHNICITY': 's3://samarati/data/my_adult_ethnicity.txt',
#        'GENDER': 's3://samarati/data/my_adult_gender.txt',
#        'BIRTHPLACE': 's3://samarati/data/my_adult_birthplace.txt',
#    },
#}