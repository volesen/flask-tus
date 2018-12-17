# HANDLE PIP
pip install --upgrade pip
pip install -r requirements.txt

python setup.py install

# START PYTHON
python demo/app.py
# gunicorn demo/app:app -b 0.0.0.0:80
