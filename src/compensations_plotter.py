from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from src.database.models import Simulation, Compensation
from decimal import Decimal
from matplotlib import rc, pyplot as plt

import seaborn as sns
import pandas as pd

ordered_labels = [" ",
        "0 | 20", "0 | 40", "0 | 60", "0 | 80", "0 | 100",
        "20 | 0", "20 | 20", "20 | 40", "20 | 60", "20 | 80", "20 | 100",
        "40 | 0", "40 | 20", "40 | 40", "40 | 60", "40 | 80", "40 | 100",
        "60 | 0", "60 | 20", "60 | 40", "60 | 60", "60 | 80", "60 | 100",
        "80 | 0", "80 | 20", "80 | 40", "80 | 60", "80 | 80", "80 | 100",
        "100 | 0", "100 | 20", "100 | 40", "100 | 60", "100 | 80", "100 | 100"
    ]

control_modes = ['no_control', 'voltvar', 'voltwatt']

def plot_full_compensations(circuit_name):
    database_folder = Path(f'D:{circuit_name.upper()}')

    data_by_mode = {mode: {label: [] for label in ordered_labels} for mode in control_modes}

    print('Getting data...')

    for db_file in database_folder.glob('*.db'):
        DATABASE_URL = f'sqlite:///{db_file.resolve()}'

        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        for control_mode in control_modes:
            query = (
                session.query(Compensation.compensation)
                .join(Simulation, Compensation.simulation_id == Simulation.id)
                .filter(control_mode == Simulation.control_mode)
            )

            data = pd.DataFrame(query.all(), columns=['compensation'])

            if not data.empty:
                data['compensation'] = data['compensation'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
                file_name = db_file.stem
                ev_pv_label = f"{file_name.split('_')[3]} | {file_name.split('_')[5]}"
                if ev_pv_label in data_by_mode[control_mode]:
                    data_by_mode[control_mode][ev_pv_label].extend(data['compensation'].tolist())

        session.close()

    for mode in control_modes:
        data_by_mode[mode] = {label: values for label, values in data_by_mode[mode].items() if values}

    if not any(data_by_mode[mode] for mode in control_modes):
        print("Data not found.")
    else:
        plot_data = []
        for mode in control_modes:
            for label, values in data_by_mode[mode].items():
                plot_data.extend([(mode, label, value) for value in values])

        df_plot = pd.DataFrame(plot_data, columns=['Control Mode', 'EV | PV Penetration', 'Compensation'])

        describe_data = df_plot.groupby(['Control Mode', 'EV | PV Penetration'])['Compensation'].describe()
        describe_data.to_csv(f'boxplot_compensation_descriptive_{circuit_name}.csv', sep=';', float_format='%.2f')
        print(f'Data saved in boxplot_descriptive_{circuit_name}.csv')

        color_palette = {
            'no_control': '#C0504D',
            'voltwatt': '#9BBB59',
            'voltvar': '#4F81BD'
        }

        # Use Latex Font
        # rc('text', usetex=True)
        # rc('font', family='serif', serif=['Computer Modern'])
        plt.figure(figsize=(20, 24))
        custom_params = {"axes.spines.right": False, "axes.spines.top": False}
        sns.set_theme(style="whitegrid", rc=custom_params)
        ax = sns.boxplot(gap=.4, fill=True, showfliers=False, width=1.1, y='EV | PV Penetration', x='Compensation',
                         hue='Control Mode', data=df_plot[df_plot['EV | PV Penetration'].isin(ordered_labels)],
                         order=ordered_labels, orient="h", linewidth=1.5, palette=color_palette)
        [ax.axhline(y + .5, color='gray', linestyle='--') for y in ax.get_yticks()]
        plt.ylabel('Níveis de Penetração VE | GDFV (%)', fontsize=34)
        plt.xlabel('Valores de Compensação (R$)', fontsize=34)
        plt.tick_params(axis='x', labelsize=34)
        # plt.tick_params(axis='y', labelsize=30)
        plt.ylim(2, len(ordered_labels))
        plt.yticks(range(len(ordered_labels)), ordered_labels, fontsize=30)
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles, ['Sem Controle', 'Com Controle Volt-VAr', 'Com Controle Volt-Watt'], title='',
                   loc='lower right', fontsize=26)

        plt.grid(axis='x', linestyle='--', alpha=0.7, color='black')

        plt.tight_layout()
        plt.savefig(f'boxplot_compensation_{circuit_name}.eps', format='eps')
        print('Figure saved.')

def plot_compensations():
    database_folder = Path('D:CA746')
    control_mode = 'no_control'

    compensations_data = {label: [] for label in ordered_labels}

    print('Getting data...')

    for db_file in database_folder.glob('*.db'):
        DATABASE_URL = f'sqlite:///{db_file.resolve()}'

        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        query = (
            session.query(Compensation.compensation)
            .join(Simulation, Compensation.simulation_id == Simulation.id)
            .filter(control_mode == Simulation.control_mode)
        )

        data = pd.DataFrame(query.all(), columns=['compensation'])

        session.close()

        if not data.empty:

            data['compensation'] = data['compensation'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
            file_name = db_file.stem
            ev_pv_label = f"{file_name.split('_')[3]} | {file_name.split('_')[5]}"
            if ev_pv_label in compensations_data:
                compensations_data[ev_pv_label].extend(data['compensation'].tolist())

    compensations_data = {label: values for label, values in compensations_data.items() if values}

    if not compensations_data:
        print("No data")
    else:
        plt.figure(figsize=(14, 10))
        plt.boxplot(compensations_data.values(), vert=True, patch_artist=True, notch=True,
                    labels=compensations_data.keys())
        plt.title(f'Box Plot of Compensations by EV | PV Penetration {control_mode}', fontsize=16)
        plt.xlabel('EV | PV Penetration', fontsize=14)
        plt.ylabel('Compensation Values', fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.7)

        plt.tight_layout()
        # plt.show()
        plt.savefig(f'plot_{control_mode}.png')
        print('Figure saved.')

if __name__ == '__main__':
    plot_full_compensations('ca746')
    plot_full_compensations('ca744')


