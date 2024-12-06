import os
import yaml

logo = '''

  __ _____ __  __ __ _  ___   __ ___ __  _ ___ ___  __ _____ __  ___  
 /  \_   _/__\|  V  | |/ _/  / _] __|  \| | __| _ \/  \_   _/__\| _ \ 
| /\ || || \/ | \_/ | | \__ | [/\ _|| | ' | _|| v / /\ || || \/ | v / 
|_||_||_| \__/|_| |_|_|\__/  \__/___|_|\__|___|_|_\_||_||_| \__/|_|_\ 

'''
print(logo + "by threatHNTR\n")

class CustomDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow, False)

def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())

yaml.add_representer(dict, dict_representer, Dumper=CustomDumper)

def validate_choice(prompt, choices):
    """Ensure user input is one of the valid choices."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in choices:
            return choice
        print(f"Invalid choice. Please select from: {', '.join(choices)}")

def validate_non_empty(prompt):
    """Ensure the user input is not empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required. Please enter a value.")

def main():

    atomic_tests = []

    add_test = validate_choice("Would you like to create a new Atomic Test? (yes or no): ", ["yes", "no"])

    while add_test == "yes":
        print("\nCreating a New Atomic Test...")
        atomic_name = validate_non_empty("Enter Atomic Test Name: ")
        atomic_description = validate_non_empty("Provide a Description for the Atomic Test: ")

        platforms = []
        while not platforms:
            platform_input = input(
                "Supported Platforms (comma-separated, e.g., windows, macos, linux): "
            ).strip()
            platforms = [p.strip() for p in platform_input.split(",") if p.strip()]
            valid_platforms = {
                "windows", "macos", "linux", "office-365", "azure-ad", "google-workspace",
                "saas", "iaas", "containers", "iaas:gcp", "iaas:azure", "iaas:aws"
            }
            if not set(platforms).issubset(valid_platforms):
                print("Invalid platform(s) provided. Please re-enter.")
                platforms = []

        executor_name = validate_choice("Select Attack Executor (none, powershell, command prompt, bash, sh): ",
                                        ["none", "powershell", "command prompt", "bash", "sh"])
        elevation_required = validate_choice("Does this require elevated privileges? (yes or no): ", ["yes", "no"]) == "yes"
        attack_command = validate_non_empty("Enter the primary command to execute the attack: ")
        cleanup_command = input("Enter a cleanup command (optional): ").strip()

        atomic_test = {
            "name": atomic_name,
            "description": atomic_description,
            "supported_platforms": platforms,
            "executor": {
                "name": executor_name,
                "command": attack_command,
                "elevation_required": elevation_required,
            },
        }

        if cleanup_command:
            atomic_test["executor"]["cleanup_command"] = cleanup_command

        if validate_choice("Would you like to add input arguments? (yes or no): ", ["yes", "no"]) == "yes":
            print("\nDefining Input Arguments (leave argument name empty to stop):")
            input_arguments = {}
            while True:
                arg_name = input("  Argument Name: ").strip()
                if not arg_name:
                    break
                arg_desc = validate_non_empty("  Argument Description: ")
                arg_default = validate_non_empty("  Default Value: ")
                arg_type = validate_choice("  Input Type (string, url, path, integer): ", ["string", "url", "path", "integer"])

                input_arguments[arg_name] = {
                    "type": arg_type,
                    "default": arg_default,
                    "description": arg_desc,
                }
            if input_arguments:
                atomic_test["input_arguments"] = input_arguments

        if validate_choice("Would you like to add dependencies? (yes or no): ", ["yes", "no"]) == "yes":
            print("\nDefining Dependencies (leave dependency description empty to stop):")
            dependencies = []
            while True:
                dep_description = input("  Dependency Description: ").strip()
                if not dep_description:
                    break
                dep_executor = validate_choice("  Dependency Executor (none, powershell, command prompt, bash, sh): ",
                                               ["none", "powershell", "command prompt", "bash", "sh"])
                prereq_command = validate_non_empty("  Prerequisite Command (command to check dependency): ")
                get_prereq_command = validate_non_empty("  Get Prerequisite Command (command to install dependency): ")

                dependencies.append({
                    "description": dep_description,
                    "prereq_command": prereq_command,
                    "get_prereq_command": get_prereq_command,
                })
            if dependencies:
                atomic_test["dependencies"] = dependencies
                atomic_test["dependency_executor_name"] = dep_executor

        atomic_tests.append(atomic_test)

        add_test = validate_choice("\nWould you like to create another Atomic Test? (yes or no): ", ["yes", "no"])

    for test in atomic_tests:
        atomic_name = test["name"]
        yaml_structure = {
            "atomic_tests": [test]
        }

        sanitized_name = atomic_name.lower().replace(" ", "_")
        directory = "atomic_red_team/atomics"
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, f"{sanitized_name}.yaml")

        with open(filepath, "w") as file:
            yaml.dump(yaml_structure, file, default_flow_style=False, Dumper=CustomDumper)

        print(f"\nYAML file successfully created: {filepath}")

if __name__ == "__main__":
    main()
