import os
import pandas as pd

def run():
    file_paths = get_data_path()
    export_data(file_path=file_paths)
    return

def export_data(file_path=list):
    for p in file_path:
        print(f'Now processing: {os.path.basename(p)}')
        df = pd.read_csv(p, encoding='utf-8-sig')
        df_export  = data_process(df=df)
        path_export= os.path.abspath(os.path.join('data','export', os.path.basename(p)))
        df_export.to_csv(path_export, encoding='utf-8-sig')
        print(f'File exported to: {path_export}\n')
    
    return


def get_data_path():
    path_in = os.path.abspath(os.path.join('data', 'raw'))
    path_ex = os.path.abspath(os.path.join('data', 'export'))

    file_path = []
    for name in os.listdir(path_in):
        f_p = os.path.abspath(os.path.join(path_in, name))
        e_p = os.path.abspath(os.path.join(path_ex, name))
        if os.path.isfile(f_p) and not os.path.exists(e_p):
            file_path.append(f_p)
        elif os.path.exists(e_p):
            print(f'File already exists: {e_p}')
            print('Move to the next.')

    return file_path


def data_process(df = pd.DataFrame):
    # Filter on estop
    df = df[df['estop'] == True]
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    # datetime
    df['local_time'] = pd.to_datetime(df['local_time'])
    df['时间间隔'] = (df['local_time'] - df['local_time'].shift(1)).dt.total_seconds().fillna(3)

    # get estop times
    df['estop_times'] = None
    ind = df[(df['时间间隔'] < 0) | (df['时间间隔']>=300)].index
    for i in range(1, len(ind)+1):
        df.loc[ind[i-1], 'estop_times'] = i
    df['estop_times'] = df['estop_times'].ffill().fillna(0)

    return df