import os
from datetime import datetime, timedelta
import pytz

def generate_dashboard():
    # 1. Configuración de hora de actualización (Argentina)
    try:
        timezone = pytz.timezone('America/Argentina/Buenos_Aires')
        now = datetime.now(timezone).strftime("%d-%m-%Y %H:%Mhs")
    except Exception:
        now = datetime.now().strftime("%d-%m-%Y %H:%Mhs")

    # --- CONFIGURACIÓN DE PRIORIDADES ---
    # Valores altos para que al usar reverse=True aparezcan arriba
    ENV_PRIORITY = {"PROD": 3, "SBX": 2, "DEV": 1}
    SITE_PRIORITY = {
        "TNPT1": 5, "TNPT2": 4, "ELTRECE": 3, 
        "ELDOCE": 2, "CIUDAD": 1
    }

    # 2. Estructura HTML inicial
    html_start = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard QA Artear</title>
        <style>
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #121212; color: #e0e0e0; padding: 20px; line-height: 1.6; }}
            .container {{ max-width: 1400px; margin: auto; }}
            header {{ border-bottom: 2px solid #4caf50; padding-bottom: 15px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }}
            h1 {{ margin: 0; color: #4caf50; font-size: 1.8em; }}
            .last-update {{ font-size: 0.85em; color: #888; }}
            
            .filters-section {{ background: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 20px; display: flex; gap: 15px; flex-wrap: wrap; align-items: center; border: 1px solid #333; }}
            .filter-group {{ display: flex; flex-direction: column; gap: 5px; }}
            .filter-group label {{ font-size: 0.75em; color: #4caf50; text-transform: uppercase; font-weight: bold; }}
            .filter-group select {{ background: #2c2c2c; color: white; border: 1px solid #444; padding: 8px; border-radius: 4px; min-width: 130px; cursor: pointer; }}
            
            table {{ width: 100%; border-collapse: collapse; background-color: #1e1e1e; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
            th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #333; font-size: 0.9em; }}
            th {{ background-color: #2c2c2c; color: #4caf50; text-transform: uppercase; font-size: 0.75em; letter-spacing: 1px; }}
            tr:hover {{ background-color: #2a2a2a; }}
            .btn-link {{ background-color: #4caf50; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 0.75em; display: inline-block; }}
            .env-tag {{ font-weight: bold; font-size: 0.8em; padding: 2px 6px; border-radius: 3px; background: #333; }}
            strong {{ color: #fff; }}
            .hidden {{ display: none !important; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div><h1>📊 Dashboard de Regresión Visual</h1></div>
                <div class="last-update">Última actualización: <strong>{now}</strong> (ART)</div>
            </header>
    """

    # 3. Escaneo de archivos
    root_dir = "." 
    reports = []
    unique_versions = set()
    unique_sites = set()
    unique_devices = set()
    unique_dates = set()
    
    excluded_dirs = {'gh-pages-branch', 'temp-main', '.git', '.github', '__pycache__', 'node_modules'}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        if "index.html" in files:
            if root == root_dir or root == ".": continue
            rel_path = os.path.relpath(root, root_dir)
            parts = rel_path.split(os.sep)
            
            if len(parts) >= 5:
                # Asumiendo estructura: Sitio/Dispositivo/Ambiente/Version/Fecha_Hora/index.html
                site, device, env, ver, date_folder = parts[0], parts[1], parts[2], parts[3], parts[4]
                
                # --- PARSING DE FECHA (Crítico para el ordenamiento) ---
                sort_date = datetime.min
                display_date = date_folder
                filter_date = "Otro"
                
                # Intentamos varios formatos comunes, priorizando el que enviaste (DD-MM-YYYY)
                date_clean = date_folder.replace('_', ' ').replace('hs', '')
                formats_to_try = [
                    '%d-%m-%Y %H-%M',    # 06-01-2026_17-10
                    '%d-%m-%Y %H:%M',    # 06-01-2026 17:10
                    '%Y-%m-%d %H-%M',    # 2026-01-06_17-10
                    '%Y-%m-%d %H:%M',    # 2026-01-06 17:10
                    '%d-%m-%Y %H-%M-%S'
                ]
                
                for fmt in formats_to_try:
                    try:
                        dt_obj = datetime.strptime(date_clean, fmt)
                        sort_date = dt_obj
                        display_date = dt_obj.strftime('%d-%m-%Y %H:%Mhs')
                        filter_date = dt_obj.strftime('%d-%m-%Y')
                        break
                    except:
                        continue

                unique_versions.add(ver)
                unique_sites.add(site.upper())
                unique_devices.add(device)
                if filter_date != "Otro": unique_dates.add(filter_date)

                reports.append({
                    'site': site.upper(),
                    'device': device,
                    'env': env.upper(),
                    'ver': ver,
                    'date_display': display_date,
                    'filter_date': filter_date,
                    'date_sort': sort_date,
                    'env_priority': ENV_PRIORITY.get(env.upper(), 0),
                    'site_priority': SITE_PRIORITY.get(site.upper(), 0),
                    'link': f"./{rel_path}/index.html"
                })

    # 4. ORDENAMIENTO JERÁRQUICO REAL
    # 1. Fecha Descendente, 2. Ambiente (PROD primero), 3. Sitio (TNPT1 primero)
    reports.sort(key=lambda x: (x['date_sort'], x['env_priority'], x['site_priority']), reverse=True)

    # 5. Construcción de Filtros HTML
    filters_html = f"""
            <section class="filters-section">
                <div class="filter-group">
                    <label>Sitio</label>
                    <select id="filterSite" onchange="filterTable()">
                        <option value="all">Todos</option>
                        {''.join([f'<option value="{s}">{s}</option>' for s in sorted(unique_sites)])}
                    </select>
                </div>
                <div class="filter-group">
                    <label>Dispositivo</label>
                    <select id="filterDevice" onchange="filterTable()">
                        <option value="all">Todos</option>
                        {''.join([f'<option value="{d}">{d}</option>' for d in sorted(unique_devices)])}
                    </select>
                </div>
                <div class="filter-group">
                    <label>Ambiente</label>
                    <select id="filterEnv" onchange="filterTable()">
                        <option value="all">Todos</option>
                        <option value="PROD">PROD</option>
                        <option value="SBX">SBX</option>
                        <option value="DEV">DEV</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Versión</label>
                    <select id="filterVer" onchange="filterTable()">
                        <option value="all">Todas</option>
                        {''.join([f'<option value="{v}">{v}</option>' for v in sorted(unique_versions, reverse=True)])}
                    </select>
                </div>
                <div class="filter-group">
                    <label>Fecha del Test</label>
                    <select id="filterDate" onchange="filterTable()">
                        <option value="all">Todos los días</option>
                        {''.join([f'<option value="{d}">{d}</option>' for d in sorted(unique_dates, reverse=True)])}
                    </select>
                </div>
            </section>
            
            <table id="reportsTable">
                <thead>
                    <tr>
                        <th>Sitio</th>
                        <th>Dispositivo</th>
                        <th>Ambiente</th>
                        <th>Versión</th>
                        <th>Fecha del Test</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody>
    """

    # 6. Generación de Filas
    html_rows = ""
    for r in reports:
        env_color = "#4caf50" if r['env'] == "PROD" else "#ffa500" if r['env'] == "SBX" else "#2196f3"
        html_rows += f"""
        <tr data-site="{r['site']}" data-env="{r['env']}" data-device="{r['device']}" data-date="{r['filter_date']}" data-ver="{r['ver']}">
            <td><strong>{r['site']}</strong></td>
            <td>{r['device']}</td>
            <td><span class="env-tag" style="color: {env_color}">{r['env']}</span></td>
            <td>{r['ver']}</td>
            <td>{r['date_display']}</td>
            <td><a class="btn-link" target="_blank" href="{r['link']}">ABRIR REPORTE</a></td>
        </tr>
        """

    js_script = """
        <script>
        function filterTable() {
            const fSite = document.getElementById('filterSite').value;
            const fEnv = document.getElementById('filterEnv').value;
            const fDevice = document.getElementById('filterDevice').value;
            const fDate = document.getElementById('filterDate').value;
            const fVer = document.getElementById('filterVer').value;
            
            const rows = document.querySelectorAll('#reportsTable tbody tr');

            rows.forEach(row => {
                const mSite = fSite === 'all' || row.getAttribute('data-site') === fSite;
                const mEnv = fEnv === 'all' || row.getAttribute('data-env') === fEnv;
                const mDevice = fDevice === 'all' || row.getAttribute('data-device') === fDevice;
                const mDate = fDate === 'all' || row.getAttribute('data-date') === fDate;
                const mVer = fVer === 'all' || row.getAttribute('data-ver') === fVer;

                if (mSite && mEnv && mDevice && mDate && mVer) {
                    row.classList.remove('hidden');
                } else {
                    row.classList.add('hidden');
                }
            });
        }
        </script>
    """

    full_html = html_start + filters_html + html_rows + "</tbody></table>" + js_script + "</div></body></html>"
    
    with open("index.html", "w", encoding='utf-8') as f:
        f.write(full_html)
    print(f"✅ Dashboard generado: Ordenado por Fecha > Ambiente > Sitio. Filtros actualizados.")

if __name__ == "__main__":
    generate_dashboard()
