Weekly calendar creation
========================

# Requirements

- Inkscape
- With conda

    1. Install [conda](https://docs.conda.io/en/latest/miniconda.html)
    2. Create conda environment with all the requirements

        ```
        $ conda env create -f environment.yml
        ```

    3. Activate conda environment

        ```
        $ conda activate calendar
        ```

- Without conda

    - Python >3
    - pandas
    - pikepdf

# Generate the calendar

1. Create a SVG template for a week.

    It must contain text with
    - `%month%"` for the month placeholder
    - `%week%` for the week number placeholder
    - `%mon%` for Monday number placeholder
    - `%tue%` for Tuesday number placeholder
    - `%wed%` for Wednesday number placeholder
    - `%thu%` for Thursday number placeholder
    - `%fri%` for Friday number placeholder
    - `%sat%` for Saturday number placeholder
    - `%sun%` for Sunday number placeholder

2. Create an output folder
3. Run the script

    ```
    $ python bin/generate_calendar.py \
        -s <start date in format Y-M-D> \
        -e <end date in format Y-M-D> \
        -t <path to template file> \
        -o <path to output directory>
    ```

