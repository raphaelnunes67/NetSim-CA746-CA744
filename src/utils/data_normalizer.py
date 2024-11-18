import numpy as np


def normalize_data(file_path):
    with open(file_path, 'r') as file:
        data = [float(line.strip()) for line in file.readlines()]

    data_array = np.array(data)

    min_val = np.min(data_array)
    max_val = np.max(data_array)

    normalized_data = (data_array - min_val) / (max_val - min_val)

    with open(file_path , 'w') as file:
        for value in normalized_data:
            file.write(f"{value}\n")

    print(f"Data saved: {file_path}")


if __name__ == '__main__':
    normalize_data('../data/irradiation_curves/pv_varied.txt')
