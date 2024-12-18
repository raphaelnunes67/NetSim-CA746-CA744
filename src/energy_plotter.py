from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from src.database.models import Simulation, EnergyMeter
from decimal import Decimal
from matplotlib import rc, pyplot as plt
import pandas as pd
import seaborn as sns

# Parâmetros
ordered_labels = [" ",
                  "0 | 20", "0 | 40", "0 | 60", "0 | 80", "0 | 100",
                  "20 | 0", "20 | 20", "20 | 40", "20 | 60", "20 | 80", "20 | 100",
                  "40 | 0", "40 | 20", "40 | 40", "40 | 60", "40 | 80", "40 | 100",
                  "60 | 0", "60 | 20", "60 | 40", "60 | 60", "60 | 80", "60 | 100",
                  "80 | 0", "80 | 20", "80 | 40", "80 | 60", "80 | 80", "80 | 100",
                  "100 | 0", "100 | 20", "100 | 40", "100 | 60", "100 | 80", "100 | 100"]

control_modes = ['no_control', 'voltvar', 'voltwatt']


def plot_energy_boxplots(circuit_name, bus_type):
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
                session.query(Simulation.loop_simulation_id, EnergyMeter.energy)
                .join(Simulation, EnergyMeter.simulation_id == Simulation.id)
                .filter(control_mode == Simulation.control_mode)
                .filter(EnergyMeter.bus.like(f"%{bus_type}%"))
            )
            data = pd.DataFrame(query.all(), columns=['loop_simulation_id', 'energy'])

            if not data.empty:
                data['energy'] = data['energy'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

                if bus_type == 'PV':
                    data['energy'] = data['energy'] * -1

                grouped_data = data.groupby('loop_simulation_id', as_index=False)['energy'].sum()

                file_name = db_file.stem
                ev_pv_label = f"{file_name.split('_')[3]} | {file_name.split('_')[5]}"

                if ev_pv_label in data_by_mode[control_mode]:
                    data_by_mode[control_mode][ev_pv_label].extend(grouped_data['energy'].tolist())

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

        df_plot = pd.DataFrame(plot_data, columns=['Control Mode', 'EV | PV Penetration', 'Energy'])

        describe_data = df_plot.groupby(['Control Mode', 'EV | PV Penetration'])['Energy'].describe()
        describe_data.to_csv(f'boxplot_energy_descriptive_{circuit_name}_{bus_type}.csv', sep=';', float_format='%.2f')
        print(f'Data saved in boxplot_energy_descriptive_{circuit_name}_{bus_type}.csv')

        color_palette = {
            'no_control': '#C0504D',
            'voltwatt': '#9BBB59',
            'voltvar': '#4F81BD'
        }

        plt.figure(figsize=(20, 24))
        custom_params = {"axes.spines.right": False, "axes.spines.top": False}
        sns.set_theme(style="whitegrid", rc=custom_params)
        ax = sns.boxplot(
            gap=.4, fill=True, showfliers=False, width=1, y='EV | PV Penetration', x='Energy',
            hue='Control Mode', data=df_plot[df_plot['EV | PV Penetration'].isin(ordered_labels)],
            order=ordered_labels, orient="h", linewidth=1.5, palette=color_palette)

        [ax.axhline(y + .5, color='gray', linestyle='--') for y in ax.get_yticks()]
        plt.ylabel('Níveis de Penetração VE | GDFV (%)', fontsize=34)
        plt.xlabel('Energia (kWh)', fontsize=34)
        plt.tick_params(axis='x', labelsize=34)
        plt.ylim(2, len(ordered_labels))
        plt.yticks(range(len(ordered_labels)), ordered_labels, fontsize=30)
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles, ['Sem Controle', 'Com Controle Volt-VAr', 'Com Controle Volt-Watt'], title='',
                   loc='lower right', fontsize=26)

        plt.grid(axis='x', linestyle='--', alpha=0.7, color='black')
        plt.tight_layout()
        plt.savefig(f'boxplot_energy_{circuit_name}_{bus_type}.eps', format='eps')
        print('Figure saved.')


if __name__ == '__main__':
    # plot_energy_boxplots('ca746', 'PV')
    plot_energy_boxplots('ca746', 'EV')
    # plot_energy_boxplots('ca744', 'PV')
    plot_energy_boxplots('ca744', 'EV')
