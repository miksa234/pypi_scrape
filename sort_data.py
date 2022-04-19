#/usr/bin/env python3.6

import os
import pandas as pd
import numpy as np
from datetime import datetime

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def main():

    path = './data/'
    file_names =  sorted(os.listdir(path), key=lambda x: datetime.strptime(x, '%Y-%m.csv'))
    dframes = {}

    for fname in file_names:
       dframes[fname] = pd.read_csv(path + fname, sep='|', keep_default_na=False)
    cache_list = [['package', 'requirement']]

    for i, fname in enumerate(file_names[:10]):

        print(fname, f'{round(i/len(file_names)*100, 1)}%', sep='\t')

        if i == 0:
            all_before_pd = dframes[fname]
        else:
            all_before_pd = pd.concat([dframes[_] for _ in file_names[:i]])

        for j, (package, requirement) in enumerate(dframes[fname].to_numpy()):
            if requirement != '':
                if requirement not in all_before_pd['package'].to_list():
                    cache_list.append([package, requirement])
                    dframes[fname]['requirement'].iloc[j] = ''

            if (index_found := np.where(np.array(cache_list, dtype='object')[:,1] == package)[0]).size != 0:
                for i_found in index_found:
                    found_package, found_requirement = cache_list[i_found]
                    dframes[fname].append({'package': found_package, 'requirement': found_requirement},\
                                      ignore_index=True)
                    del cache_list[i_found]


        dframes[fname] = dframes[fname].drop_duplicates()
        dframes[fname].to_csv('./data_sorted/' + fname, sep='|', index=False)


if __name__ == '__main__':
    main()
