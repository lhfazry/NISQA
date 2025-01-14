# -*- coding: utf-8 -*-
"""
@author: Gabriel Mittag, TU-Berlin
"""
from nisqa.NISQA_model import nisqaModel
import argparse
import os
from calc_mci import mean_confidence_interval

parser = argparse.ArgumentParser()
parser.add_argument('--mode', required=True, type=str, help='either predict_file, predict_dir, or predict_csv')
parser.add_argument('--pretrained_model', required=True, type=str, help='file name of pretrained model (must be in current working folder)')
parser.add_argument('--deg', type=str, help='path to speech file')
parser.add_argument('--data_dir', type=str, help='folder with speech files')
parser.add_argument('--prefix', type=str, help='prefix')
parser.add_argument('--max_files', type=int, help='max_files')
parser.add_argument('--output_dir', type=str, help='folder to ouput results.csv')
parser.add_argument('--filename', type=str, help='filename to ouput results.csv')
parser.add_argument('--csv_file', type=str, help='file name of csv (must be in current working folder)')
parser.add_argument('--csv_deg', type=str, help='column in csv with files name/path')
parser.add_argument('--num_workers', type=int, default=0, help='number of workers for pytorchs dataloader')
parser.add_argument('--bs', type=int, default=1, help='batch size for predicting')
parser.add_argument('--ms_channel', type=int, help='audio channel in case of stereo file')

args = parser.parse_args()
args = vars(args)

if args['mode'] == 'predict_file':
    if args['deg'] is None:
        raise ValueError('--deg argument with path to input file needed')
elif args['mode'] == 'predict_dir':
    if args['data_dir'] is None:
        raise ValueError('--data_dir argument with folder with input files needed')
elif args['mode'] == 'predict_csv':
    if args['csv_file'] is None:
        raise ValueError('--csv_file argument with csv file name needed')
    if args['csv_deg'] is None:
        raise ValueError('--csv_deg argument with csv column name of the filenames needed')
    if args['data_dir'] is None:
        args['data_dir'] = ''
else:
        raise NotImplementedError('--mode given not available')
args['tr_bs_val'] = args['bs']
args['tr_num_workers'] = args['num_workers']
    
if __name__ == "__main__":
    nisqa = nisqaModel(args)
    df = nisqa.predict()

    mos_preds = df['mos_pred'].to_numpy()
    m_mos = mean_confidence_interval(mos_preds)

    print(f"\n\n{args['data_dir']} - {args['prefix']}")
    print(f"MOS: {m_mos[0]} \u00b1 {m_mos[1]}")

    df.to_csv(os.path.join(args['output_dir'], args['filename']), index=False)


































