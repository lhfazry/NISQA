import pandas as pd
import numpy as np
import scipy.stats
from argparse import ArgumentParser

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, h

def main(args):
    mos = []

    df = pd.read_csv(args.csv)
    mos_preds = df['mos_pred'].to_numpy()
    m_mos = mean_confidence_interval(mos_preds)

    print(f"MOS: {m_mos[0]} \u00b1 {m_mos[1]}")

if __name__ == '__main__':
    parser = ArgumentParser(description='Calculate MOS')
    parser.add_argument('--csv', help='CSV')
    
    main(parser.parse_args())
