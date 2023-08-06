import pandas as pd
import numpy as np


pd.set_option("display.max_columns", 100)
pd.set_option("display.max_rows", 100)


# def prepare_data(file, model):
#     df = pd.read_csv(file)
#     df = df.set_index("OPTUM_LAB_ID")
#     print("Getting propensity scores ...", end = " ")
#     propensity_scores = get_propensity_scores(model = model, data = df, verbose = False)
#     print("DONE!")
#     df["PROPENSITY"] = propensity_scores
#     return df


# def get_propensity_scores(model, data, verbose = False):
#     import statsmodels.api as sm
#     glm_binom = sm.formula.glm(formula = model, data = data, family = sm.families.Binomial())
#     result = glm_binom.fit()
#     if verbose:
#         print(result.summary)
#     return result.fittedvalues


def match(groups, propensity, k):
    groups = groups == groups.unique()[1]
    n = len(groups)
    n1 = groups[groups==1].sum()
    n2 = n-n1
    g1, g2 = propensity[groups==1], propensity[groups==0]

    if n1 > n2:
        n1, n2, g1, g2 = n2, n1, g2, g1

    m_order = list(np.random.permutation(groups[groups==1].index))
    matches = {}

    for m in m_order:
        dist = abs(g1[m]-g2)
        array = np.array(dist)
        k_smallest = np.partition(array, k)[:k].tolist()
        keep = np.array(dist[dist.isin(k_smallest)].index)

        if len(keep):
            matches[m] = list(np.random.choice(keep, k, replace=False))
        else:
            matches[m] = [dist.idxmin()]

        g2 = g2.drop(matches[m])

    matches = pd.DataFrame.from_dict(matches, orient="index")
    matches = matches.reset_index()
    column_names = {}
    column_names["index"] = "CASE_ID"
    for i in range(k):
        column_names[i] = str("CONTROL_MATCH_" + str(i+1))
    matches = matches.rename(columns = column_names)
    return matches


# def make_crosstable(df, var):
#     crosstable = pd.crosstab(df["CASE"], df[var])
#     return crosstable


# def calc_chi2_2x2(crosstable):
#     from scipy.stats import chi2_contingency
#     f_obs = np.array([crosstable.iloc[0][0:2].values,
#                       crosstable.iloc[1][0:2].values])
#     result = chi2_contingency(f_obs)[0:3]
#     round_result = (round(i,4) for i in result)
#     return list(round_result)


# def calc_chi2_2xC(crosstable):
#     from scipy.stats import chi2_contingency
#     C = crosstable.shape[1]
#     f_obs = np.array([crosstable.iloc[0][0:C].values,
#                       crosstable.iloc[1][0:C].values])
#     result = chi2_contingency(f_obs)[0:3]
#     round_result = (round(i,4) for i in result)
#     return list(round_result)


# def flatten_match_ids(df):
#     master_list = []
#     master_list.append(df[df.columns[0]].tolist())
#     for i in range(1, df.shape[1]):
#         master_list.append(df[df.columns[i]].tolist())
#     master_list = [item for sublist in master_list for item in sublist]
#     return master_list


def get_matched_data(match_ids, raw_data):
    match_ids = flatten_match_ids(match_ids)
    matched_data = raw_data[raw_data.index.isin(match_ids)]
    return matched_data


def evaluate_match(match_ids, raw_data):
    matched_data = get_matched_data(match_ids, raw_data)
    variables = matched_data.columns.tolist()[0:-2]
    results = {}

    for var in variables:
        crosstable = make_crosstable(matched_data, var)
        p_val = calc_chi2_2x2(crosstable)[1]
        results[var] = p_val
        print("\t" + var, end = "")
        if p_val < 0.05:
            print(": FAILED!")
        else:
            print(": PASSED!")

    if True in [i < 0.05 for i in results.values()]:
        return "At least one variable failed to match!"
    return "All variables were successfully matched!"


def run(file, model, k):
    print("\nReading data: " + file)
    df = prepare_data(file, model)
    print("Matching controls to cases ...", end = " ")
    matched_df = match(df.CASE, df.PROPENSITY, k=int(k))
    print("DONE!")
    print("Evaluating matches ...")
    print(evaluate_match(matched_df, df))
    print("Writing data to file ...")
    save_file = file.split(".")[0] + "_matched_ps.csv"
    matched_df.to_csv(save_file, index=False)
    print()

