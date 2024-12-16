
import re
import requests
import subprocess
import os
import winreg
import zipfile

def get_chrome_version() -> str:
    """Devuelve la versión actual de Google Chrome instalada."""
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
        version, _ = winreg.QueryValueEx(key, 'version')
        print(f"Versión de Google Chrome instalada: {version}")
    
    except FileNotFoundError:
        print("Google Chrome no está instalado.")

    return version if 'version' in locals() else None

def update_chrome_driver(chrome_version:str) -> None:
    """Actualiza el chromedriver.exe a la última versión compatible con Google Chrome.
    chrome_version: Versión de Google Chrome en formato 'XXX.X.XXXX.XXX'.
    Si no existe version de chrome, no se actualiza chromedriver."""
    if chrome_version is None:
        print("No se pudo obtener la versión de Google Chrome.")
        return

    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')

    # Verificar versión actual de chromedriver
    chromedriver_version = None
    if os.path.exists(chromedriver_path):
        try:
            output = subprocess.check_output([chromedriver_path, '--version'], stderr=subprocess.STDOUT).decode()
            chromedriver_version = re.search(r'ChromeDriver (\d+\.\d+\.\d+\.\d+)', output).group(1)
        except Exception:
            pass
        print('Version de Chromedriver: ', chromedriver_version)

    chrome_version = chrome_version.split('.')[0] if chrome_version else None
    chromedriver_version = chromedriver_version.split('.')[0] if chromedriver_version else None

    if chrome_version == chromedriver_version:
        print("La versión de ChromeDriver coincide con la versión de Google Chrome.")
        return
    else:
        print("Actualizando ChromeDriver...")

        # Construir URL de descarga
        # Obtener la versión completa de Chrome
        chrome_version
        
        # Primero, solicitar el HTML de la página
        response = requests.get('https://googlechromelabs.github.io/chrome-for-testing/#stable')
        html_content = response.text

        # Segundo, encontrar el enlace de descarga que coincide con la versión de Chrome

        pattern = rf"https://storage\.googleapis\.com/chrome-for-testing-public/({chrome_version}\.\d+\.\d+\.\d+)/win64/chromedriver-win64\.zip"
        match = re.search(pattern, html_content)

        if match:
            download_url = match.group(0)
        else:
            print(f"No se encontró el ChromeDriver para la versión {chrome_version}")
            return
        
        # Descargar chromedriver
        zip_path = os.path.join(os.getcwd(), 'chromedriver.zip')
        try:
            response = requests.get(download_url)
            with open(zip_path, 'wb') as file:
                file.write(response.content)
        except Exception as e:
            print(f"Error al descargar ChromeDriver: {e}")
            return

        # Extraer chromedriver.exe
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())
            os.remove(zip_path)
            # Mover 'chromedriver.exe' desde 'chromedriver-win64' al directorio actual
            extracted_dir = os.path.join(os.getcwd(), 'chromedriver-win64')
            chromedriver_exe = os.path.join(extracted_dir, 'chromedriver.exe')
            os.replace(chromedriver_exe, os.path.join(os.getcwd(), 'chromedriver.exe'))
            for root, dirs, files in os.walk(extracted_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(extracted_dir)
            print("ChromeDriver actualizado correctamente.")
        except Exception as e:
            print(f"Error al extraer ChromeDriver: {e}")
            return

if __name__ == '__main__':
    chrome_version = get_chrome_version()
    update_chrome_driver(chrome_version)