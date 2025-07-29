import importlib.util
import inspect
import os
import sys
import textwrap

def get_user_file():
    path = input("Enter the Python file to test (e.g., kn_sock/udp.py): ").strip()
    if not os.path.isfile(path):
        print("❌ File does not exist.")
        sys.exit(1)
    return path

def load_module_from_path(filepath):
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None:
        print("❌ Could not load module.")
        sys.exit(1)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def check_docstring(func):
    doc = inspect.getdoc(func)
    if not doc:
        return "❌ Missing docstring"

    signature = inspect.signature(func)
    missing_params = []
    for param in signature.parameters:
        if param not in doc:
            missing_params.append(param)

    missing_returns = "Returns:" not in doc and "return:" not in doc.lower()
    
    issues = []
    if missing_params:
        issues.append(f"Missing parameter docs: {', '.join(missing_params)}")
    if missing_returns:
        issues.append("Missing 'Returns' section")
    
    return "✅ OK" if not issues else "⚠️ " + "; ".join(issues)

def main():
    filepath = get_user_file()
    module = load_module_from_path(filepath)

    print(f"\n🔍 Checking functions in {filepath}...\n")

    public_functions = [
        (name, func)
        for name, func in inspect.getmembers(module, inspect.isfunction)
        if not name.startswith("_") and func.__module__ == module.__name__
    ]

    if not public_functions:
        print("No public functions found.")
        return

    for name, func in public_functions:
        status = check_docstring(func)
        print(f"{name} → {status}")

if __name__ == "__main__":
    main()

