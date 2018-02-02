import pandas as pd


# brands data
input_data = pd.read_csv('data_before_removal_of_other/brands_(400)_1221734/source1221734.csv')
input_data = input_data[input_data['label_gold'].isnull()]
answered = pd.read_csv('data_before_removal_of_other/brands_(400)_1221734/a1221734.csv')

assert len(answered)  == 650
assert len(input_data)  == 2401

unanswered = pd.concat([input_data,answered]).drop_duplicates(keep=False,subset='id')
assert len(unanswered) == len(input_data) - len(answered)
check = unanswered[['id']].isin(answered['id'].values)
assert len(check['id'].value_counts()) == 1
assert check['id'].value_counts()[0] == len(input_data) - len(answered)
assert check['id'].value_counts().get(True) is None

unanswered.to_csv('unanswered_brands.csv', index=False)