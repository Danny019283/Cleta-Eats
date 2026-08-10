# CletaEats

Este es el prototipo para el sistema de pedidos y gestión de repartidores "CletaEats". El proyecto está construido bajo una arquitectura limpia (Vista, Controlador, Servicio, Entidades) utilizando Python y Streamlit.

## Requisitos Previos

Para ejecutar la aplicación, es recomendable utilizar el gestor de entornos **Anaconda (o Miniconda)** para aislar las dependencias del proyecto.

## Instrucciones de Instalación y Ejecución

Sigue estos pasos desde tu terminal, asegurándote de estar ubicado en la carpeta raíz del proyecto (`/home/danny/Proyectos/prototipo_lab1`):

### 1. Crear el entorno virtual (solo la primera vez)

Utiliza el archivo `environment.yml` incluido para que Conda descargue automáticamente la versión correcta de Python y las librerías necesarias (como `streamlit` y `pytest`).

```bash
conda env create -f environment.yml
```
*(Conda empezará a descargar e instalar los paquetes. Esto puede tomar uno o dos minutos).*

### 2. Activar el entorno

Cada vez que vayas a trabajar en el proyecto o a ejecutarlo, debes "encender" este entorno para que el sistema utilice las librerías correctas:

```bash
conda activate cleta-eats-env
```
*(Al hacerlo, notarás que en tu terminal aparecerá el nombre `(cleta-eats-env)` al inicio de la línea).*

### 3. Correr la aplicación

Con el entorno ya activado, simplemente ejecuta el comando normal de Streamlit para abrir la aplicación web en tu navegador:

```bash
streamlit run app.py
```

---

## Ejecución de Pruebas Unitarias (Testing)

El sistema cuenta con un suite de pruebas automatizadas (con `pytest`) para validar las reglas de negocio en la capa de servicios (ej. validaciones de repartidores, cálculo de facturas, transiciones de estados, etc.).

Para correr las pruebas unitarias, ejecuta en la misma terminal (con el entorno activado):

```bash
pytest tests/ -v
```
