# claude-powered-gui-interaction

assuming unix environment:

run on a terminal window:
```commandline
conda create -n g python=3.11
conda activate g
conda install -c conda-forge --file requirements.txt
python3 app.py
# This will open a browser up

```

run on another terminal window:
```commandline
conda activate g
python3 mouse_demo.py
```