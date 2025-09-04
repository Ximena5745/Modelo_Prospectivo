# pipeline_proyecciones_arima_v2.py
import pandas as pd
import numpy as np
import sqlite3
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

try:
    from pmdarima import auto_arima
    HAVE_AUTO = True
except:
    HAVE_AUTO = False

INPUT_FILE = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Prospectiva\Data\Dataset_Unificado.xlsx"
SHEET_NAME = "Unificado"
OUTPUT_EXCEL = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Prospectiva\Proyecciones_ARIMA_Escenarios.xlsx"
SQLITE_FILE = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Prospectiva\proyecciones.db"
TABLE_NAME = "proyecciones_arima"

# ---------- Helpers ----------
def safe_to_float_series(s):
    s = s.astype(str).str.replace(",", ".", regex=False)
    s = s.str.replace(r"[^0-9\.\-]", "", regex=True)
    return pd.to_numeric(s, errors="coerce")

def next_period_date(last_date, periodicidad):
    if periodicidad.lower().startswith("sem"):
        return last_date + pd.DateOffset(months=6)
    return last_date + pd.DateOffset(years=1)

def make_future_index(last_date, periodicidad, steps):
    dates = []
    cur = last_date
    for i in range(steps):
        cur = next_period_date(cur, periodicidad)
        dates.append(cur)
    return pd.DatetimeIndex(dates)

def try_arima_forecast(series, steps):
    if HAVE_AUTO:
        model = auto_arima(series, seasonal=False, stepwise=True,
                           suppress_warnings=True, error_action="ignore")
        fit = ARIMA(series, order=model.order).fit()
    else:
        fit = ARIMA(series, order=(1,1,1)).fit()
    forecast = fit.get_forecast(steps=steps)
    pred = forecast.predicted_mean
    ci = forecast.conf_int()
    return pred, ci.iloc[:,0], ci.iloc[:,1], str(fit.model_orders)

# ---------- Load ----------
df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)
df.columns = df.columns.str.strip()
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
df["Ejecución"] = safe_to_float_series(df["Ejecución"])

# ---------- Run forecasts ----------
all_forecasts = []
indicators = df[df["Periodicidad"].isin(["Semestral", "Anual"])]["Id"].unique()

for idx in indicators:
    sub = df[df["Id"] == idx].sort_values("Fecha")
    periodicidad = sub["Periodicidad"].iloc[0]
    indicador_name = sub["Indicador"].iloc[0]
    serie = sub.set_index("Fecha")["Ejecución"].dropna()
    if len(serie) < 3:
        continue
    steps = 10 if periodicidad.lower().startswith("sem") else 5
    
    try:
        pred, low, up, metodo = try_arima_forecast(serie, steps)
        idx_future = make_future_index(serie.index[-1], periodicidad, steps)

        # Escenarios: conservador, base, optimista
        escenarios = {
            "Conservador": pd.Series(low.values, index=idx_future),
            "Base": pd.Series(pred.values, index=idx_future),
            "Optimista": pd.Series(up.values, index=idx_future)
        }

        for esc, serie_esc in escenarios.items():
            for dt, val in serie_esc.items():
                all_forecasts.append({
                    "Id": idx,
                    "Indicador": indicador_name,
                    "Periodicidad": periodicidad,
                    "Fecha_Proyeccion": dt,
                    "Escenario": esc,
                    "Proyeccion_Ejecucion": max(0, float(val)),  # sin negativos
                    "Metodo": metodo,
                    "N_obs": len(serie)
                })

    except Exception as e:
        print(f"[Error] {idx} - {indicador_name}: {e}")

# ---------- Save ----------
df_out = pd.DataFrame(all_forecasts)
df_out = df_out.sort_values(["Id","Fecha_Proyeccion","Escenario"])
df_out.to_excel(OUTPUT_EXCEL, index=False)

conn = sqlite3.connect(SQLITE_FILE)
df_out.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
conn.close()

print("✅ Proyecciones generadas en 3 escenarios (Conservador, Base, Optimista).")
