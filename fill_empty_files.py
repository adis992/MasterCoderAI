import os

# Define skeleton content for file types
SKELETONS = {
    '.py': '# Auto-generated placeholder for {filename}\n"""\nImplement module functionality here.\n"""\n',
    '.jsonl': '{{}}\n',
    '.yaml': '# TODO: Add configuration for {filename}\n',
    '.yml': '# TODO: Add configuration for {filename}\n',
    '.md': '# {filename}\n\nTODO: Document this file.\n',
    '.gitignore': '# Byte-compiled / optimized / DLL files\n__pycache__/\n*.py[cod]\n# Env\n.env\n',
    'docker-compose.yml': "version: '3.8'\nservices:\n  app:\n    build: .\n    command: echo 'Add your services'\n",
    'ci.yml': 'name: CI\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v2\n      - name: Setup Python\n        uses: actions/setup-python@v2\n        with:\n          python-version: "3.x"\n      - name: Install dependencies\n        run: pip install -r zahtjevi.txt\n      - name: Run tests\n        run: pytest\n',
    'cd.yml': 'name: CD\non: [push]\njobs:\n  deploy:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v2\n      - name: Deploy\n        run: echo "Deploy steps here"\n'
}

# Walk through workspace
root = os.getcwd()
for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        fpath = os.path.join(dirpath, fname)
        try:
            if os.path.getsize(fpath) == 0:
                # Determine skeleton key
                skeleton = None
                ext = os.path.splitext(fname)[1]
                if fname in SKELETONS:
                    skeleton = SKELETONS[fname]
                elif ext in SKELETONS:
                    skeleton = SKELETONS[ext]
                if skeleton:
                    content = skeleton.format(filename=fname)
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Popunjeno: {fpath}')
        except Exception as e:
            print(f'Error processing {fpath}: {e}')
print('Popunjavanje završeno.')
