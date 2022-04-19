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
       dframes[fname] = np.genfromtxt(path + fname, delimiter='|', dtype='str')[1:]

    cache_array = np.array([['package', 'requirement']], dtype='str')

    for i, fname in enumerate(file_names):

        print(fname, f'{round(i/len(file_names)*100, 1)}%    {len(cache_array)}', sep='\t')

        if i == 0:
            all_before_data = dframes[fname]
        else:
            all_before_data = np.vstack([dframes[_] for _ in file_names[:i]])

        for j, (package, requirement) in enumerate(dframes[fname]):
            if requirement != '':
                if requirement not in all_before_data[:,0]:
                    cache_array = np.vstack([cache_array, [package, requirement]])
                    dframes[fname][:,1][j] = ''

            index_found = np.where(cache_array[:,1] == package)[0]
            if index_found.size != 0:
                for i_found in index_found:
                    found_package, found_requirement = cache_array[i_found]
                    dframes[fname] = np.vstack([dframes[fname], [found_package, found_requirement]])
                cache_array = np.delete(cache_array, index_found, axis=0)


        dframes[fname] = np.unique(dframes[fname], axis=0)
        pd.DataFrame(dframes[fname], columns=['package', 'requirement']).to_csv('./data_sorted/' + fname, sep='|', index=False)



if __name__ == '__main__':
    main()
