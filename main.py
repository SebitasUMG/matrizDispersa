import csv
from scipy.sparse import lil_matrix
from graphviz import Digraph


def load_sparse_matrix_from_csv(csv_file):
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)

        max_row_index = 0
        num_columns = len(next(csvreader)) - 1

        for row in csvreader:
            max_row_index = max(max_row_index, int(row[0]))

        sparse_matrix = lil_matrix((max_row_index + 1, num_columns), dtype=int)

        csvfile.seek(0)
        next(csvreader)

        for row in csvreader:
            for j, value in enumerate(row[1:]):
                sparse_matrix[int(row[0]), j] = int(value)

    return sparse_matrix


def visualize_sparse_matrix(sparse_matrix, column_names):
    dot = Digraph()
    for j, column_name in enumerate(column_names):
        dot.node(str(j), label=column_name, shape='rectangle')

    for i in range(sparse_matrix.shape[0]):
        for j in range(sparse_matrix.shape[1]):
            if sparse_matrix[i, j] != 0:
                dot.node(str(i), shape='circle')
                dot.edge(str(i), str(j), label=str(sparse_matrix[i, j]))

    dot.render('sparse_matrix', format='png', cleanup=True)
    dot.view()


def main():
    csv_file = input("Enter the path to the CSV file: ")

    try:
        with open(csv_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            column_names = next(csvreader)[1:]
        sparse_matrix = load_sparse_matrix_from_csv(csv_file)
        visualize_sparse_matrix(sparse_matrix, column_names)
    except FileNotFoundError:
        print("File not found. Please make sure the path is correct.")


if __name__ == "__main__":
    main()
