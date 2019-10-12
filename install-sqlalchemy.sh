#!/bin/bash

wget "https://files.pythonhosted.org/packages/14/0e/487f7fc1e432cec50d2678f94e4133f2b9e9356e35bacc30d73e8cb831fc/SQLAlchemy-1.3.10.tar.gz"
tar -xf SQLAlchemy-1.3.10.tar.gz
cd SQLAlchemy-1.3.10
python setup.py install
cd ..
rm -rf SQLAlchemy-1.3.10
rm SQLAlchemy-1.3.10.tar.gz
