from ab_rmsd import calc_ab_rmsd
import os
import pandas as pd
import argparse

def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native_dir', type=str, default='/share/pengzhangzhi/ab_result/benchmark_data/pdbs/')
    parser.add_argument('--pred_dir', type=str, default='/share/pengzhangzhi/ab_result/esmfold/benchmark_149_73/nano/')
    parser.add_argument('--out_path', type=str, default='./igfold_benchmark_pair.csv')
    args = parser.parse_args()
    return args


def run(
    native_dir = '',
    pred_dir = '',
    out_path = './result.csv',
):
    res = {}
    errors = []
    for pdb_file in os.listdir(pred_dir):
        try:
            id = pdb_file.split('.')[0]
            native_path = os.path.join(native_dir, pdb_file)
            pred_path = os.path.join(pred_dir, pdb_file)
            rmsd = calc_ab_rmsd(pred_path,native_path)
            res[id] = {k:v.item() for k, v in rmsd.items()}
        except Exception as e:
            error_msg = f"[Error] {e}. \n native path: {native_path} \n pred path: {pred_path}"
            print(error_msg)
            errors.append(error_msg)
            
    # save error massage
    out_dir = os.path.dirname(out_path)
    with open(os.path.join(out_dir, 'errors.log'), 'w') as f:
        f.write('\n'.join(errors))
        
    # save rmsd statistics
    df = pd.DataFrame(res).T
    df.loc['mean'] = df.mean()
    df.to_csv(out_path)
    print(df)
    
if __name__ == '__main__':
    args = parse_arg()
    run(args.native_dir, args.pred_dir, args.out_path)
   