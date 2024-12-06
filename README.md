# Atomic Generator

A Python-based tool for generating YAML files for atomic tests for Atomic Red Team.

## Features
- This is a tool inspired by [atomic test generator](atomicgen.io). I wanted to create a python based tool to do essentially the same thing.
- Generate atomic test YAML files with required and optional fields.
- Supports dependencies and input arguments.
- Validates user input to ensure correct data format.

## Requirements
- Python 3.7+
- `pyyaml` package

## Installation
1. Clone the repository:

    ```bash
    git clone https://github.com/threatHNTR/atomic-generator.git
    cd atomic-generator
    ```

2. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```
## Usage

Run the script:

```bash
python generate_atomic_tests.py
```

Follow the prompts to generate the YAML files. The generated files will be saved in the atomic_red_team/atomics/ directory.

## Contributing

Feel free to open issues or submit pull requests for enhancements or bug fixes.

## To Do

- Add multiline option for attack commands
