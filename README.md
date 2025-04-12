# claude-powered-gui-interaction

assuming unix environment:

run:
```commandline
conda create -n g python=3.10
conda activate g
conda install -c conda-forge anthropic flask
python3 app.py
# This will open a browser up

```

On another terminal
```commandline
conda activate g
python3 mouse_demo.py
```