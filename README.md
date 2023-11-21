# Arriendo-autos-Dataqu

## Ambiente Virtual

Es recomendable trabajar dentro de un ambiente virtual para mantener las dependencias requeridas por el proyecto separadas. Puedes crear un ambiente virtual en Python utilizando el siguiente comando:

``` bash
python -m venv nombre_del_ambiente
```
Para activar el ambiente virtual, usa:

- En Windows:

```bash
nombre_del_ambiente\Scripts\activate
```

- En Unix o MacOS:

```bash
source nombre_del_ambiente/bin/activate
```

## Requisitos

Una vez que el ambiente virtual esté activo, puedes instalar las librerías necesarias que se encuentran en el archivo requirements.txt utilizando el comando:

```bash
pip install -r requirements.txt
```

## Base de Datos

Puedes borrar la base de datos (db.sqlite3) para trabajar desde cero, ya que sólo contiene archivos de prueba.

## Carga de Datos

Los archivos que se pueden cargar se encuentran dentro de la carpeta fixtures de la aplicación RentAdmin. Estos archivos permiten cargar datos a las tablas Cliente, Empresa y Arriendo. Para cargar los datos, utiliza el siguiente comando:

```bash
python manage.py loaddata nombre_del_archivo
```
