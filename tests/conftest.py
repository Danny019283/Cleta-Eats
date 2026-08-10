import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'Modelo', 'Entidades'))
sys.path.insert(0, os.path.join(project_root, 'Modelo', 'Servicios'))
sys.path.insert(0, os.path.join(project_root, 'Acceso a Datos'))
sys.path.insert(0, os.path.join(project_root, 'Modelo'))
