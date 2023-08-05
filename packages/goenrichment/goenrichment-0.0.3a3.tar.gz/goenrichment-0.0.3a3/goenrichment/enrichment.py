import pandas
import numpy as np

from scipy.stats import hypergeom
import statsmodels.stats.multitest as smm


def calculate(godb, query,
              alpha=0.05,
              min_category_depth=4,
              min_category_size=3,
              max_category_size=500):
    """
    Calculate the GO enrichment from a list of gene IDs
    :param df: Pandas dataframe with genes IDs
    :param gene_id_column: Gene ID column on the data frame
    :param geneGoDB: geneGoDB data structure
    :param name_space: GO name space
    :return: Pandas data frame
    """
    vals = []
    pvalues = []
    N = len(set(query))
    terms, nodes = zip(*godb['graph'].nodes(data=True))
    for node in nodes:
        category = node['genes']
        n = len(category)
        hits = query.intersection(category)
        k = len(hits)
        if k > 0 and node.get('depth', 0) >= min_category_depth \
                and min_category_size <= n <= max_category_size:
            p = hypergeom.sf(k - 1, godb['M'], n, N)
            pvalues.append(p)
            vals.append((node['id'], node['name'], p, k, n, node['depth']))
    correction = smm.multipletests(pvalues, alpha=alpha, method='fdr_bh')
    df = pandas.DataFrame(vals, columns=['term', 'name', 'p', 'k', 'n', 'depth'])
    df['acepted'] = correction[0]
    df['q'] = correction[1]
    df['-1.0log(q)'] = -1.0 * np.log10(correction[1])
    df = df[['term', 'name', 'depth', 'k', 'n', 'p', 'q', '-1.0log(q)', 'acepted']]
    df = df.sort_values('-1.0log(q)', ascending=False)
    return df
