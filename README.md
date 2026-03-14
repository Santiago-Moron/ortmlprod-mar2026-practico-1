# Práctico 1

En este práctico se abordarán los conceptos básicos de Docker y se realizará un ejercicio práctico para descargar y trabajar con imágenes de Docker.

- Manejo de control de versiones con Git (repaso)
- Gestión de dependencias en Python (repaso)
- Fundamentos de Docker y contenedores (repaso)
- Ejemplo simple de descarga de imágenes de Docker


## Índice de Contenidos

1. [Creación de un Repositorio en GitHub](#1-creación-de-un-repositorio-en-github)
   
   1.1 [Seteo de SSH](#11-seteo-de-ssh)
   
   1.2 [Git Clone](#12-git-clone)
   
   1.3 [Git Init](#13-git-init)

2. [Dependencias de Python](#2-dependencias-de-python)

   2.1 [Instalación de virtualenv](#21-instalación-de-virtualenv)

   2.2 [Creación de un entorno virtual](#22-creación-de-un-entorno-virtual)

   2.3 [Activación del entorno virtual](#23-activación-del-entorno-virtual)

   2.4 [Gestión con pip y PyPI](#24-gestión-con-pip-y-pypi)

   2.5 [Gestión con pip-tools](#25-gestión-con-pip-tools)

   2.6 [Especificación de versiones en requirements.txt](#26-especificación-de-versiones-en-requirementstxt)

3. [Docker](#3-docker)

   3.1 [Instalación de Docker](#31-instalación-de-docker)

   3.2 [Creación de imágenes de Docker](#32-creación-de-imágenes-de-docker)

   3.3 [Empaquetado de una aplicación Python](#33-empaquetado-de-una-aplicación-python)


## 1. Creación de un Repositorio en GitHub

La forma más sencilla de crear un repositorio en GitHub es desde el siguiente enlace: https://github.com/new. Esto abrirá una nueva pestaña en el navegador con un formulario para crear un nuevo repositorio. 

Hay dos formas principales de comenzar a trabajar con un repositorio Git localmente:
- Usar `git clone` para clonar un repositorio existente.
- Usar `git init` para crear un repositorio nuevo desde cero.

### 1.1 Seteo de SSH

Para poder interactuar con GitHub, es necesario configurar una clave SSH. Los pasos para esto son los siguientes:

1. Generar una clave SSH
    Se debe seguir el [tutorial de GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) para generar una clave SSH.

2. Agregar la clave SSH al repositorio remoto
    Se debe seguir el [tutorial de GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) para agregar la clave SSH al repositorio remoto.

3. Probar la conexión
    Hay varias maneras de probar la conexión con GitHub. A continuación vamos a ver una de las formas, que requiere la instalación de `openssh-client`.

    La manera más sencilla es desactivar las claves SSH con el comando:
    ```bash
    ssh-add -D
    ```

    Luego, se debe activar la clave SSH que acabamos de generar con el comando:
    ```bash
    ssh-add ~/.ssh/<nombre-de-la-clave>
    ```

    Finalmente, se debe probar la conexión con GitHub usando el comando:
    ```bash
    ssh -T git@github.com
    ```

**Recomendación:**
Configurar el nombre y email del usuario con los comandos:

```bash
git config --global user.name "Nombre para los commits"
git config --global user.email "tu.email@example.com"
```

Se puede dejar configurado de manera global o por repositorio.

### 1.2 Git Clone
Se puede clonar un repositorio existente en GitHub usando el siguiente comando:
```bash
git clone <url-del-repositorio>
```

Usar `git clone` cuando:
- Se quiere trabajar sobre un repositorio que ya existe en GitHub u otro servidor remoto.
- Se quiere una copia completa del historial del proyecto.
- Se quiere comenzar a contribuir a un proyecto existente.

### 1.3 Git Init
Si se está comenzando un proyecto nuevo desde cero, debes pararte dentro del directorio del proyecto y usar el siguiente comando:
```bash
git init
```

Usar `git init` cuando:
- Se está comenzando un proyecto nuevo desde cero.
- Se quiere convertir un proyecto (carpetas, archivos, etc. pero no un repositorio Git) existente local en un repositorio Git.
- Se quiere crear un repositorio vacío que luego conectarás con un remoto.

Si usas `git init`, necesitarás configurar el remoto manualmente:
```bash
git remote add origin <url-del-repositorio>
git branch -M main
git push -u origin main
```


## 2. Dependencias de Python

Las dependencias de Python son módulos o bibliotecas que una aplicación de Python utiliza para su correcto funcionamiento. Existen diferentes herramientas para gestionar estas dependencias, siendo las más populares `pip`, `pip-tools`, `poetry`, `uv`, entre otras.

Vamos a trabajar con `pip` y `pip-tools` por simplicidad, pero pueden buscar documentación de otras herramientas en su web, como por ejemplo [poetry](https://python-poetry.org/docs/) o [uv](https://github.com/astral-sh/uv).

Para esto, vamos a trabajar utilizando entorno virtuales con la librería `virtualenv`.

### 2.1 Instalación de virtualenv

```bash
pip install virtualenv
```

### 2.2 Creación de un entorno virtual

En Linux/Mac:
```bash
virtualenv venv -p $(which python3.11)
```

En Windows:
```bash
python -m virtualenv venv -p python3.11
```

### 2.3 Activación del entorno virtual

En Linux/Mac:
```bash
source venv/bin/activate
```

En Windows:
```bash
.\venv\Scripts\activate
```


### 2.4 Gestión con pip y PyPI

Pip es la herramienta estándar de línea de comandos que se utiliza para descargar e instalar paquetes de Python desde el Python Package Index (PyPI), el repositorio oficial de paquetes de Python.

Para gestionar dependencias con pip:

1. Crear un archivo `requirements.txt` manualmente
2. Listar las dependencias y versiones deseadas
3. Instalar con `pip install -r requirements.txt`

Por ejemplo, un archivo `requirements.txt` puede tener el siguiente contenido:

```bash
requests>=2.26.0
beautifulsoup4>=4.10.0
```

Al ejecutar `pip install -r requirements.txt` se instalarán las dependencias en el entorno actual.

### 2.5 Gestión con pip-tools

Pip-tools es una herramienta que permite gestionar dependencias de Python de manera más eficiente. Sus principales ventajas son:

- **Bloqueo de versiones**: Genera un archivo requirements.txt con versiones exactas, garantizando entornos reproducibles
- **Gestión de dependencias transitivas**: Resuelve y bloquea automáticamente las dependencias de las dependencias
- **Separación de dependencias**: Permite mantener `requirements.in` con dependencias directas y `requirements.txt` con todas las dependencias resueltas
- **Actualización selectiva**: Facilita actualizar paquetes específicos y sus dependencias con `pip-compile --upgrade-package`
- **Sincronización del entorno**: El comando `pip-sync` instala/desinstala paquetes para que coincidan exactamente con requirements.txt

Para usar pip-tools:

1. Instala pip-tools con `pip install pip-tools`
2. Crea un archivo `requirements.in` con las dependencias deseadas
3. Ejecuta `pip-compile requirements.in` para generar `requirements.txt`
4. Instala las dependencias con `pip install -r requirements.txt`


### 2.6 Especificación de versiones en requirements.txt

Bibliotecas de Python: Se enumeran las bibliotecas de terceros que se utilizan en la aplicación, junto con sus versiones. Hay varios operadores para especificar versiones:

- `requests==2.26.0`: Instala exactamente la versión 2.26.0
- `requests>=2.26.0`: Instala la versión 2.26.0 o superior
- `requests~=2.26.0`: Instala la versión 2.26.x más reciente (compatible con 2.26.0)
- `requests`: Instala la última versión disponible
- `requests>=2.26.0,<3.0.0`: Instala una versión entre 2.26.0 y 3.0.0
- `requests!=2.26.0`: Instala cualquier versión excepto la 2.26.0

Se recomienda especificar versiones para garantizar la reproducibilidad del entorno.

## 3. Docker

Docker es una plataforma de virtualización de contenedores que permite crear, implementar y ejecutar aplicaciones de manera aislada en un entorno seguro y reproducible. Los contenedores son unidades de software ligeras y portátiles que empaquetan el código y todas sus dependencias para que la aplicación se ejecute de manera rápida y confiable en cualquier entorno informático.

Las principales ventajas de Docker incluyen:

- **Portabilidad:** Las aplicaciones pueden ejecutarse de manera consistente en distintos entornos
- **Aislamiento:** Cada contenedor funciona de forma independiente sin interferir con otros contendores
- **Eficiencia:** Los contenedores comparten recursos del sistema operativo, siendo más livianos que las máquinas virtuales
- **Escalabilidad:** Facilita el despliegue y la gestión de múltiples instancias
- **Versionado:** Permite rastrear cambios y rollbacks de manera sencilla

Docker utiliza una arquitectura cliente-servidor y aprovecha las características de aislamiento del kernel de Linux para proporcionar sus funcionalidades de contenedorización.


### 3.1 Instalación de Docker

Para instalar Docker:

1. Windows/Mac: Descarga Docker Desktop desde https://www.docker.com/products/docker-desktop
2. Linux: Sigue las instrucciones específicas para tu distribución en https://docs.docker.com/engine/install/

Para aprender los conceptos básicos de Docker (imágenes, contenedores, volúmenes), consulta la documentación oficial: https://docs.docker.com/get-started/

### 3.2 Creación de imágenes de Docker

1. Crea un archivo **Dockerfile** en el directorio raíz del proyecto que defina cómo construir la imagen. Este contiene una serie de instrucciones que Docker utiliza para construir la imagen. El mismo debe incluir:
   - Especificación de la imagen base a utilizar
   - Instalación de dependencias necesarias
   - Configuración del entorno

2. Construye la imagen con el comando **docker build**.
   ```bash
   docker build -t <nombre_imagen> .
   ```
   El comando construye una imagen de Docker a partir del Dockerfile en el directorio actual. Lee las instrucciones del Dockerfile y ejecuta cada paso secuencialmente para crear capas de la imagen. La opción `-t` permite asignar un nombre y etiqueta a la imagen resultante. El punto `.` al final indica que el Dockerfile está en el directorio actual.
   
3. Ejecuta el contenedor usando **docker run**:
   ```bash
   docker run --name <container_name> -v ./imagenes:/app/imagenes <image_name> <command>
   ```

   Los parámetros principales son:
   - `--name <container_name>`: Da un nombre descriptivo al contenedor
   - `-v ./imagenes:/app/imagenes`: Conecta una carpeta local con el contenedor para compartir archivos
   - `<image_name>`: Nombre de la imagen Docker a ejecutar
   - `<command>`: Comando que se ejecutará dentro del contenedor

También se pueden gestionar contenedores, imágenes y volúmenes desde el dashboard de Docker Desktop.

### 3.3 Empaquetado de una aplicación Python

Para ejecutar una aplicación Python en un contenedor Docker, necesitarás preparar los siguientes elementos:

1. **Código fuente de la aplicación**
   - Todo el código Python de tu aplicación (archivos .py)
   - Archivos de configuración y recursos necesarios
   - Estructura de directorios del proyecto
   - Tests y documentación relevante

2. **Gestión de dependencias**
   - Archivo `requirements.txt` con las dependencias exactas (librerías como `pip-tools`, `poetry` y `uv` pueden ser útiles)
   - Versiones específicas de las bibliotecas para reproducibilidad
   - Dependencias de desarrollo separadas (opcional)
   - Entorno virtual si es necesario (**recomendado**, librerías como `venv`, `pyenv`, `virtualenv` pueden ser útiles)

3. **Configuración del contenedor**
   - Comando de inicio definido en el Dockerfile (CMD o ENTRYPOINT)
   - Variables de entorno necesarias (ej: credenciales, configuración de la aplicación, etc.)
   - Argumentos de línea de comandos
   - Ejemplo: `CMD ["python", "app.py"]`

4. **Configuración de red**
   - Puertos expuestos en el Dockerfile (`EXPOSE`)
   - Mapeo de puertos al ejecutar (`-p host:container`)
   - Ejemplo: `docker run -p 8080:8080 mi-app`
   - Redes personalizadas si se requiere comunicación entre contenedores

5. **Volúmenes y persistencia**
   - Montaje de volúmenes para datos persistentes
   - Directorios compartidos entre host y contenedor
   - Ejemplo: `docker run -v ./data:/app/data mi-app`

6. **Monitoreo y logs**
   - Configuración de logging
   - Healthchecks
   - Métricas de la aplicación
