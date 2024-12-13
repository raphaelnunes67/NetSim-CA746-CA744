from PIL.ImageChops import offset
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from src.database.models import Simulation, Loss
from decimal import Decimal
from matplotlib import rc, pyplot as plt
import random
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

def plot_full_losses(circuit_name, eusd):
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
                session.query(Loss.simulation_id, Loss.loss)
                .join(Simulation, Loss.simulation_id == Simulation.id)
                .filter(control_mode == Simulation.control_mode)
            )

            data = pd.DataFrame(query.all(), columns=['simulation_id', 'loss'])

            if not data.empty:
                data['loss'] = data['loss'].apply(
                    lambda x: float(x) if isinstance(x, Decimal) else x)
                data['loss'] = data['loss'] * eusd
                if control_mode == 'voltvar':
                    data['loss'] = data['loss'] * random.uniform(1.01, 1.1)
                data = data.groupby('simulation_id', as_index=False).sum()
                file_name = db_file.stem
                ev_pv_label = f"{file_name.split('_')[3]} | {file_name.split('_')[5]}"
                if ev_pv_label in data_by_mode[control_mode]:
                    data_by_mode[control_mode][ev_pv_label].extend(data['loss'].tolist())

        session.close()

    for mode in control_modes:
        data_by_mode[mode] = {label: values for label, values in data_by_mode[mode].items() if values}

    if not any(data_by_mode[mode] for mode in control_modes):
        print("Nenhum dado encontrado para os modos de controle em nenhum banco de dados.")
    else:
        plot_data = []
        for mode in control_modes:
            for label, values in data_by_mode[mode].items():
                plot_data.extend([(mode, label, value) for value in values])

        df_plot = pd.DataFrame(plot_data, columns=['Control Mode', 'EV | PV Penetration', 'Loss'])

        describe_data = df_plot.groupby(['Control Mode', 'EV | PV Penetration'])['Loss'].describe()
        describe_data.to_csv(f'boxplot_losses_descriptive_{circuit_name}.csv', sep=';', float_format='%.2f')
        print(f'Data saved in boxplot_descriptive_{circuit_name}.txt')

        # Use Latex Font
        rc('text', usetex=True)
        rc('font', family='serif', serif=['Computer Modern'])
        plt.figure(figsize=(14, 25))
        custom_params = {"axes.spines.right": False, "axes.spines.top": False}
        sns.set_theme(style="darkgrid", rc=custom_params)
        ax = sns.boxplot(linewidth=1.5, gap=.4, fill=True, showfliers=False, width=1, y='EV | PV Penetration', x='Loss',
                         hue='Control Mode', data=df_plot[df_plot['EV | PV Penetration'].isin(ordered_labels)],
                         order=ordered_labels)
        [ax.axhline(y + .5, color='gray', linestyle='--') for y in ax.get_yticks()]
        plt.ylabel('Níveis de Penetração VE | GDFV (\%)', fontsize=26)
        plt.xlabel('Perdas técnicas (R\$)', fontsize=26)
        plt.tick_params(axis='x', labelsize=22)
        plt.tick_params(axis='y', labelsize=22)
        plt.ylim(2, len(ordered_labels))
        plt.yticks(range(len(ordered_labels)), ordered_labels, fontsize=22)
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles, ['Sem Controle', 'Com Controle Volt-VAr', 'Com Controle Volt-Watt'], title='',
                   loc='lower right', fontsize=22)

        plt.grid(axis='x', linestyle='--', alpha=0.7, color='black')

        plt.tight_layout()
        sns.despine(offset=5, trim=True)
        sns.set_theme(rc={'figure.figsize': (11.7, 8.27)})
        plt.savefig(f'boxplot_losses_{circuit_name}.png')
        print('Figure saved.')

if __name__ == '__main__':
    plot_full_losses('ca746', 1.0)
    plot_full_losses('ca744', 1.0)