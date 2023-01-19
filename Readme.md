# Generate CSV 
This is a simple script to generate a CSV file with a specific size.

## How run it

Run the script
```bash
python csv_generator.py
```

## Usage

- This example will generate a CSV file with 1GB of size and 200 columns.

    ```python
    CsvGenerator("1GB.csv", 1*CsvGenerator.GB, n_columns=200).generate()
    ```

- This example will generate a CSV file with 1MB of size and 200 columns.

    ```python
    CsvGenerator("1MB.csv", 1*CsvGenerator.MB, n_columns=200).generate()
    ```

- This example will generate a CSV file with 2GB reusing the 1GB file.

    ```python
    CsvGenerator("2GB.csv", 2*CsvGenerator.GB, reuse_file="1GB.csv").generate()
    ```