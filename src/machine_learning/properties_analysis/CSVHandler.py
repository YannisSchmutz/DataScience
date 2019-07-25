
import csv
from collections import defaultdict
from pprint import pprint


def write_csv(file_name, data_set, data_description):
    """

    :param file_name:
    :param data_set:
    :return:
    """
    with open(file_name, mode='w') as fh:
        csv_writer = csv.writer(fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(data_description)
        for data_entry in data_set:
            csv_writer.writerow(data_entry)


def validate_csv(file_name, types):
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        validation_errors = defaultdict(dict)
        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                for i, (value, validation_type) in enumerate(zip(row, types)):
                    try:
                        if validation_type is int or validation_type is float:
                            validation_type(value)
                        # TODO: Check string and others...
                    except ValueError as err:
                        validation_errors[line_count][i] = err
                        continue

    print(f'Processed {line_count} lines.')
    if validation_errors:
        print(f'Found the following error(s):')
        pprint(dict(validation_errors))
        return False
    else:
        print(f"The given file {file_name} passed the validation!")
