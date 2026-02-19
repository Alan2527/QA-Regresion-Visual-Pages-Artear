# 📊 QA-Regresion-Visual-Pages: Report Hosting

Este repositorio funciona como el **servidor estático** (vía GitHub Pages) para todos los resultados generados por el motor de regresión visual de Artear.

## 🌐 Acceso Directo
Todos los reportes están centralizados en el Dashboard principal:
🔗 **[https://artear.github.io/QA-Regresion-Visual-Pages/](https://artear.github.io/QA-Regresion-Visual-Pages/)**

## 🏗️ Organización de la Información
Los reportes se almacenan siguiendo una jerarquía estricta de directorios para facilitar la trazabilidad:
`[SITIO] / [DISPOSITIVO] / [AMBIENTE] / [VERSIÓN] / [FECHA_HORA]`

**Ejemplo de ruta:**
`tnpt1/desktop/dev/4033/09-01-2025_14-30/index.html`

## 📄 Anatomía del Reporte
Cada ejecución genera un set de archivos:
* **index.html:** Un reporte interactivo que resume la cantidad de elementos analizados, elementos OK y fallas detectadas.
* **Capturas de Pantalla (.png):** * `Base`: Captura del sitio estable.
    * `Nueva`: Captura del sitio con los cambios.
    * `Diferencias`: Imagen procesada que marca visualmente dónde están los errores.

## ⚙️ Proceso de Actualización Automática
Este repositorio recibe contenido mediante el `JamesIves/github-pages-deploy-action`. 
1. El repositorio de código (`QA-Regresion-Visual`) genera los archivos.
2. Se realiza un "push" automático a la rama `gh-pages` de este repositorio.
3. No se deben realizar cambios manuales en este repo, ya que podrían ser sobrescritos por el flujo automatizado.

## 🛠️ Mantenimiento
Si el Dashboard principal deja de mostrar reportes nuevos, verificar los permisos del `REPORTS_TOKEN` en los secretos de la organización y asegurar que la rama `gh-pages` esté configurada correctamente en los ajustes de GitHub Pages.
