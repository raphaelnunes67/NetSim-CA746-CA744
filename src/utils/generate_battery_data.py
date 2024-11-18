import os
import pandas as pd
from pathlib import Path

if __name__ == '__main__':

    df = pd.read_csv(Path('../dss/CA746/ev_shapes.csv'))
    num_columns = df.shape[1]

    for i in range(num_columns):
        df = pd.read_csv(Path('../dss/CA746/ev_shapes.csv'))
        count = 0
        values = []

        if os.path.exists(Path('battery_shapes.csv')):
            df2 = pd.read_csv(Path('battery_shapes.csv'))

            for element in df.iloc[:, i]:
                if count < 180 and element == 1:
                    count = count + 1
                    values.append(0)
                elif element == 1 and count == 180:
                    values.append(0.95)
                else:
                    values.append(0)

            df2[i] = values
        else:
            df2 = pd.DataFrame({i: values})

        df2.to_csv(Path('battery_shapes.csv'), index=False)

    df = pd.read_csv(Path('battery_shapes.csv'))
    df = df.iloc[:, 1:]
    df.to_csv(Path('battery_shapes.csv'), header=False, index=False)