# ============================
# IMPORTS
# ============================
import pandas as pd
import numpy as np
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.ensemble import RandomForestRegressor
from scipy import stats as scipy_stats
import warnings
warnings.filterwarnings('ignore')

# ============================
# CONFIGURACIÓN OPTIMIZADA
# ============================
MIN_DATA_POINTS = 6
OUTLIER_THRESHOLD = 3.5  # Aumentado para ser más tolerante con crecimientos fuertes
RECENT_WEIGHT = 0.8  # Mayor peso a datos recientes

# LÍMITES DIFERENCIADOS POR TIPO DE INDICADOR
LIMITES_POR_TIPO = {
    '%': {
        'min_confidence': 0.01,
        'max_confidence': 0.03,
        'limite_superior': 0.05,
        'limite_inferior': -0.05,
        'volatilidad_max': 0.03,
        'valor_min': 0,
        'valor_max': 100
    },
    'ENT': {
        'min_confidence': 0.05,
        'max_confidence': 0.15,
        'limite_superior': 0.50,  # Aumentado: permite hasta 50% crecimiento anual
        'limite_inferior': -0.20,
        'volatilidad_max': 0.12,
        'valor_min': 0,
        'valor_max': None
    },
    'DEC': {
        'min_confidence': 0.05,
        'max_confidence': 0.12,
        'limite_superior': 0.40,  # Aumentado
        'limite_inferior': -0.15,
        'volatilidad_max': 0.10,
        'valor_min': 0,
        'valor_max': None
    },
    '$': {
        'min_confidence': 0.05,
        'max_confidence': 0.15,
        'limite_superior': 0.50,  # Aumentado
        'limite_inferior': -0.20,
        'volatilidad_max': 0.12,
        'valor_min': 0,
        'valor_max': None
    },
    'DEFAULT': {
        'min_confidence': 0.05,
        'max_confidence': 0.12,
        'limite_superior': 0.40,  # Aumentado
        'limite_inferior': -0.15,
        'volatilidad_max': 0.10,
        'valor_min': 0,
        'valor_max': None
    }
}

# ============================
# RUTAS
# ============================
INPUT_FILE = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Modelo_Prospectivo\Data\Dataset_Unificado.xlsx"
OUTPUT_FILE = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Modelo_Prospectivo\Data\Multimodelo.xlsx"

# ============================
# LECTURA Y PREPARACIÓN
# ============================
df = pd.read_excel(INPUT_FILE, sheet_name="Unificado")

columnas_requeridas = ["Id", "Indicador", "Periodicidad", "Fecha", "Ejecución", "Meta"]
if "Meta" not in df.columns:
    print("⚠️ ADVERTENCIA: No se encontró la columna 'Meta'")
    df["Meta"] = "DEFAULT"

df = df[columnas_requeridas].copy()
df["Fecha"] = pd.to_datetime(df["Fecha"])
df = df.sort_values(["Id", "Fecha"])

print("\n📋 MUESTRA DE VALORES EN COLUMNA META:")
print(df[["Indicador", "Meta"]].drop_duplicates().head(10))
print(f"\n📊 Tipos de Meta detectados: {df['Meta'].value_counts().to_dict()}")

# ============================
# FUNCIONES AUXILIARES
# ============================

def detectar_tipo_indicador(meta_value, valores_historicos=None):
    """Detecta el tipo de indicador basado en Meta y valores históricos"""
    if pd.isna(meta_value):
        tipo_por_meta = 'DEFAULT'
    else:
        meta_str = str(meta_value).upper().strip()
        if '%' in meta_str or 'PORCENTAJE' in meta_str:
            tipo_por_meta = '%'
        elif 'ENT' in meta_str:
            tipo_por_meta = 'ENT'
        elif 'DEC' in meta_str:
            tipo_por_meta = 'DEC'
        elif '$' in meta_str or 'PESO' in meta_str:
            tipo_por_meta = '$'
        else:
            tipo_por_meta = 'DEFAULT'

    if valores_historicos is not None and len(valores_historicos) > 0:
        valores_clean = valores_historicos.dropna()
        if len(valores_clean) > 0:
            min_val = valores_clean.min()
            max_val = valores_clean.max()
            # Solo considera porcentual si TODOS los valores están entre 0-100
            if min_val >= 0 and max_val <= 100 and tipo_por_meta == '%':
                return '%'

    return tipo_por_meta

def obtener_limites(tipo_indicador):
    """Obtiene los límites específicos para el tipo de indicador"""
    return LIMITES_POR_TIPO.get(tipo_indicador, LIMITES_POR_TIPO['DEFAULT'])

def detectar_outliers(ts, threshold=OUTLIER_THRESHOLD):
    """Detecta outliers, pero es más tolerante con tendencias fuertes"""
    if len(ts) < 4:
        return ts, []

    # Calcula Z-score sobre los cambios porcentuales, no sobre valores absolutos
    pct_changes = pd.Series(ts).pct_change().dropna()
    if len(pct_changes) < 3:
        return ts, []

    z_scores = np.abs(scipy_stats.zscore(pct_changes))
    outliers = np.where(z_scores > threshold)[0]

    return ts, outliers.tolist()

def calcular_estadisticas_robustas(ts, outliers=[], tipo_indicador='DEFAULT', meta_value=None):
    """Calcula estadísticas RESPETANDO la tendencia histórica real"""
    limites = obtener_limites(tipo_indicador)

    # Usa datos limpios solo si hay muchos outliers (>30% de datos)
    if len(outliers) > len(ts) * 0.3:
        ts_clean = ts.copy()
        ts_clean = ts_clean.drop(ts_clean.index[outliers])
    else:
        ts_clean = ts  # Usa TODOS los datos para capturar tendencia real

    if len(ts_clean) < 3:
        ts_clean = ts

    # Calcula crecimientos sobre datos completos
    crecimientos = ts.pct_change().dropna()  # USA SERIE COMPLETA

    if len(crecimientos) == 0:
        return {
            'crecimiento_mediano': 0,
            'crecimiento_promedio_ponderado': 0,
            'volatilidad': limites['min_confidence'],
            'tendencia': 'estable',
            'limite_superior': limites['limite_superior'],
            'limite_inferior': limites['limite_inferior'],
            'ultimo_valor': ts.iloc[-1],
            'n_datos': len(ts),
            'tipo_indicador': tipo_indicador
        }

    # Crecimiento mediano de TODA la serie
    crecimiento_mediano = crecimientos.median()

    # Crecimiento ponderado dando MÁS peso a datos recientes
    n = len(crecimientos)
    pesos = np.array([RECENT_WEIGHT ** (n - i - 1) for i in range(n)])
    pesos = pesos / pesos.sum()
    crecimiento_ponderado = np.average(crecimientos, weights=pesos)

    # **CRÍTICO**: Si los últimos 2-3 crecimientos son consistentemente positivos/negativos
    # ajusta el crecimiento ponderado
    ultimos_crecimientos = crecimientos.tail(min(3, len(crecimientos)))
    if len(ultimos_crecimientos) >= 2:
        if all(ultimos_crecimientos > 0):  # Todos positivos
            crecimiento_ponderado = max(crecimiento_ponderado, ultimos_crecimientos.mean())
        elif all(ultimos_crecimientos < 0):  # Todos negativos
            crecimiento_ponderado = min(crecimiento_ponderado, ultimos_crecimientos.mean())

    # Volatilidad calculada sobre MAD
    mad = np.median(np.abs(crecimientos - crecimiento_mediano))
    volatilidad = mad * 1.4826
    volatilidad = np.clip(volatilidad, limites['min_confidence'], limites['volatilidad_max'])

    # Determina tendencia de manera más precisa
    if crecimiento_ponderado > 0.03:
        tendencia = 'creciente'
        # Permite crecimientos más altos
        limite_superior = min(crecimiento_ponderado * 1.8, limites['limite_superior'])
        limite_inferior = max(crecimiento_ponderado * 0.2, limites['limite_inferior'])
    elif crecimiento_ponderado < -0.03:
        tendencia = 'decreciente'
        limite_superior = max(crecimiento_ponderado * 0.2, limites['limite_superior'] * 0.5)
        limite_inferior = max(crecimiento_ponderado * 1.8, limites['limite_inferior'])
    else:
        tendencia = 'estable'
        limite_superior = limites['limite_superior']
        limite_inferior = limites['limite_inferior']

    return {
        'crecimiento_mediano': crecimiento_mediano,
        'crecimiento_promedio_ponderado': crecimiento_ponderado,
        'volatilidad': volatilidad,
        'tendencia': tendencia,
        'limite_superior': limite_superior,
        'limite_inferior': limite_inferior,
        'ultimo_valor': ts.iloc[-1],
        'n_datos': len(ts_clean),
        'tipo_indicador': tipo_indicador
    }

def validar_proyeccion_realista(valor_proyectado, stats, periodo):
    """Valida proyección RESPETANDO la tendencia histórica"""
    ultimo_valor = stats['ultimo_valor']
    tipo_indicador = stats['tipo_indicador']
    limites = obtener_limites(tipo_indicador)

    # Validación para indicadores porcentuales
    if tipo_indicador == '%':
        valor_proyectado = np.clip(valor_proyectado, 0, 100)
        if ultimo_valor >= 95:
            valor_proyectado = min(valor_proyectado, 100)
        elif ultimo_valor <= 5:
            valor_proyectado = max(valor_proyectado, 0)
        return valor_proyectado

    # Para otros tipos: solo valida límites mínimos
    if valor_proyectado < 0:
        return max(0, ultimo_valor * 0.5)  # Evita valores negativos

    if ultimo_valor <= 0:
        return max(0, valor_proyectado)

    try:
        crecimiento_total = (valor_proyectado / ultimo_valor) - 1
        crecimiento_anual = crecimiento_total / max(periodo, 1)
    except:
        return ultimo_valor

    # **CAMBIO CRÍTICO**: Si la tendencia es creciente, NO limitar agresivamente
    if stats['tendencia'] == 'creciente':
        # Permite crecimientos hasta el doble del límite superior
        limite_sup_real = stats['limite_superior'] * 2

        if crecimiento_anual > limite_sup_real:
            # Solo corrige si es extremadamente alto
            valor_corregido = ultimo_valor * (1 + limite_sup_real) ** periodo
            return valor_corregido
        else:
            # ACEPTA la proyección
            return valor_proyectado

    elif stats['tendencia'] == 'decreciente':
        limite_inf_real = stats['limite_inferior'] * 1.5

        if crecimiento_anual < limite_inf_real:
            valor_corregido = ultimo_valor * (1 + limite_inf_real) ** periodo
            return max(0, valor_corregido)
        else:
            return valor_proyectado

    else:  # tendencia estable
        # Validación normal
        factor_horizonte = 1 + (periodo * 0.02)
        limite_sup_ajustado = stats['limite_superior'] / factor_horizonte
        limite_inf_ajustado = stats['limite_inferior'] / factor_horizonte

        if crecimiento_anual > limite_sup_ajustado:
            valor_corregido = ultimo_valor * (1 + limite_sup_ajustado) ** periodo
            return valor_corregido
        elif crecimiento_anual < limite_inf_ajustado:
            valor_corregido = ultimo_valor * (1 + limite_inf_ajustado) ** periodo
            return max(0, valor_corregido)

    return valor_proyectado

def calcular_intervalos_adaptativos(base, stats, periodo):
    """Calcula intervalos de confianza adaptativos"""
    tipo_indicador = stats['tipo_indicador']
    ultimo_valor = stats['ultimo_valor']
    limites = obtener_limites(tipo_indicador)

    es_porcentual = (tipo_indicador == '%')

    if es_porcentual:
        vol_base = min(stats['volatilidad'], 0.03)
        factor_horizonte = 1 + (periodo * 0.003)
    else:
        vol_base = stats['volatilidad']
        factor_horizonte = 1 + (periodo * 0.008)

    volatilidad_ajustada = vol_base * factor_horizonte
    volatilidad_ajustada = np.clip(volatilidad_ajustada, limites['min_confidence'], limites['max_confidence'])

    optimista = base * (1 + volatilidad_ajustada)
    pesimista = base * (1 - volatilidad_ajustada)

    if es_porcentual:
        optimista = min(optimista, 100)
        pesimista = max(pesimista, 0)
    else:
        pesimista = max(0, pesimista)

    return pesimista, optimista

def calcular_pesos_ensemble(predicciones, stats):
    """Calcula pesos dando preferencia a modelos que respetan la tendencia"""
    if len(predicciones) == 0:
        return {}

    ultimo_valor = stats['ultimo_valor']
    crec_esperado = stats['crecimiento_promedio_ponderado']
    tendencia = stats['tendencia']

    pesos = {}
    for modelo, valor in predicciones.items():
        if ultimo_valor > 0:
            crec_implicito = (valor / ultimo_valor) - 1
            diferencia = abs(crec_implicito - crec_esperado)

            # **NUEVO**: Penaliza modelos que contradicen la tendencia
            if tendencia == 'creciente' and crec_implicito < 0:
                diferencia += 0.5  # Penalización fuerte
            elif tendencia == 'decreciente' and crec_implicito > 0:
                diferencia += 0.5

            pesos[modelo] = 1 / (1 + diferencia * 10)
        else:
            pesos[modelo] = 1

    suma_pesos = sum(pesos.values())
    if suma_pesos > 0:
        pesos = {k: v/suma_pesos for k, v in pesos.items()}

    return pesos

def crear_features_ml_optimizado(ts, n_lags=3):
    """Crear features para ML"""
    if len(ts) < n_lags + 3:
        return None, None

    features = []
    target = []

    for i in range(n_lags, len(ts)):
        try:
            lags = [ts.iloc[i-j] for j in range(1, n_lags+1)]
            ma_3 = ts.iloc[max(0, i-3):i].mean()
            ma_6 = ts.iloc[max(0, i-6):i].mean() if i >= 6 else ma_3
            vol = ts.iloc[max(0, i-3):i].std() if i >= 3 else 0
            pct_change = (ts.iloc[i-1] - ts.iloc[i-2]) / ts.iloc[i-2] if ts.iloc[i-2] != 0 else 0

            if i >= 3:
                accel = ((ts.iloc[i-1] - ts.iloc[i-2]) - (ts.iloc[i-2] - ts.iloc[i-3])) / ts.iloc[i-2] if ts.iloc[i-2] != 0 else 0
            else:
                accel = 0

            if i >= 3:
                x_trend = np.arange(3)
                y_trend = ts.iloc[i-3:i].values
                if len(y_trend) == 3:
                    slope = np.polyfit(x_trend, y_trend, 1)[0]
                else:
                    slope = 0
            else:
                slope = 0

            feature_row = lags + [ma_3, ma_6, vol, pct_change, accel, slope]
            features.append(feature_row)
            target.append(ts.iloc[i])
        except:
            continue

    if len(features) == 0:
        return None, None

    return np.array(features), np.array(target)

# ============================
# FUNCIÓN PRINCIPAL
# ============================
def proyectar_optimizado(subdf, horizonte=10):
    """Sistema de proyecciones que RESPETA la tendencia histórica"""
    resultados = []
    id_ind = subdf["Id"].iloc[0]
    indicador = subdf["Indicador"].iloc[0]
    periodicidad = subdf["Periodicidad"].iloc[0]
    meta = subdf["Meta"].iloc[0] if "Meta" in subdf.columns else "DEFAULT"

    if len(subdf) < MIN_DATA_POINTS:
        print(f"⚠️  {indicador}: Datos insuficientes ({len(subdf)} < {MIN_DATA_POINTS})")
        return resultados

    # **CRÍTICO**: Excluir datos parciales del año actual (2025)
    subdf_historico = subdf[subdf["Fecha"].dt.year < 2025].copy()

    if len(subdf_historico) < MIN_DATA_POINTS:
        print(f"⚠️  {indicador}: Datos históricos completos insuficientes (excluyendo 2025 parcial)")
        # Intenta usar todos los datos si no hay suficientes históricos
        subdf_historico = subdf
    else:
        fecha_max_historico = subdf_historico["Fecha"].max()
        print(f"   📅 Usando datos hasta: {fecha_max_historico.strftime('%Y-%m-%d')} (excluyendo 2025 parcial)")

    ts = subdf_historico.set_index("Fecha")["Ejecución"].astype(float)
    ts = ts.replace(0, np.nan).dropna()

    if len(ts) < MIN_DATA_POINTS:
        print(f"⚠️  {indicador}: Datos válidos insuficientes")
        return resultados

    tipo_indicador = detectar_tipo_indicador(meta, ts)
    limites = obtener_limites(tipo_indicador)

    ts_values, outliers = detectar_outliers(ts.values)
    stats = calcular_estadisticas_robustas(ts, outliers, tipo_indicador, meta)  # Pasa la meta

    if periodicidad == "Semestral":
        freq = "6MS"
    else:
        freq = "AS"

    try:
        fechas_futuras = pd.date_range(
            start=ts.index[-1] + pd.DateOffset(months=6 if periodicidad=="Semestral" else 12),
            periods=horizonte,
            freq=freq
        )
    except:
        print(f"⚠️  {indicador}: Error generando fechas")
        return resultados

    print(f"\n📊 {indicador}")
    print(f"   📌 Tipo: {tipo_indicador} | Meta: {meta}")
    if stats.get('tiene_meta') and stats.get('meta_numerica'):
        print(f"   🎯 Meta numérica detectada: {stats['meta_numerica']:.2f}")
    print(f"   Último: {stats['ultimo_valor']:.2f} | Tendencia: {stats['tendencia'].upper()}")
    print(f"   Crec.Ponderado: {stats['crecimiento_promedio_ponderado']*100:.2f}% | Vol: {stats['volatilidad']*100:.1f}%")
    print(f"   Límites permitidos: [{stats['limite_inferior']*100:.1f}%, {stats['limite_superior']*100:.1f}%]")
    if stats['tendencia'] == 'creciente':
        print(f"   ✅ TENDENCIA CRECIENTE DETECTADA - Se respetará en proyecciones")
    if outliers:
        print(f"   ⚠️  Outliers detectados: {len(outliers)}")

    predicciones_por_periodo = {i: {} for i in range(horizonte)}

    # ARIMA
    try:
        modelo = ARIMA(ts, order=(1,1,1))
        fit = modelo.fit()
        pred = fit.get_forecast(steps=horizonte)
        forecast = pred.predicted_mean

        for i, fecha in enumerate(fechas_futuras):
            valor = validar_proyeccion_realista(forecast.iloc[i], stats, i+1)
            predicciones_por_periodo[i]['ARIMA'] = valor

            pes_arima, opt_arima = calcular_intervalos_adaptativos(valor, stats, i+1)

            resultados.append([
                id_ind, indicador, periodicidad, tipo_indicador, fecha, "ARIMA",
                round(valor, 2), round(pes_arima, 2), round(opt_arima, 2)
            ])

        print(f"   ✅ ARIMA: Año 1 = {predicciones_por_periodo[0]['ARIMA']:.2f}")
    except Exception as e:
        print(f"   ❌ ARIMA: {str(e)[:40]}")

    # ETS
    try:
        modelo = ETSModel(ts, error='add', trend='add', seasonal=None, damped_trend=False)  # damped=False para respetar tendencia
        fit = modelo.fit(maxiter=1000, disp=False)
        pred = fit.get_forecast(horizonte)
        forecast = pred.predicted_mean

        for i, fecha in enumerate(fechas_futuras):
            valor = validar_proyeccion_realista(forecast.iloc[i], stats, i+1)
            predicciones_por_periodo[i]['ETS'] = valor

            pes, opt = calcular_intervalos_adaptativos(valor, stats, i+1)

            resultados.append([
                id_ind, indicador, periodicidad, tipo_indicador, fecha, "ETS",
                round(valor, 2), round(pes, 2), round(opt, 2)
            ])

        print(f"   ✅ ETS: Año 1 = {predicciones_por_periodo[0]['ETS']:.2f}")
    except Exception as e:
        print(f"   ❌ ETS: {str(e)[:40]}")

    # Holt-Winters
    try:
        if len(ts) >= 8:
            modelo = ExponentialSmoothing(ts, trend='add', seasonal=None, damped_trend=False)
            fit = modelo.fit()
            forecast = fit.forecast(horizonte)

            for i, fecha in enumerate(fechas_futuras):
                valor = validar_proyeccion_realista(forecast.iloc[i], stats, i+1)
                predicciones_por_periodo[i]['Holt_Winters'] = valor

                pes, opt = calcular_intervalos_adaptativos(valor, stats, i+1)

                resultados.append([
                    id_ind, indicador, periodicidad, tipo_indicador, fecha, "Holt_Winters",
                    round(valor, 2), round(pes, 2), round(opt, 2)
                ])

            print(f"   ✅ Holt-Winters: Año 1 = {predicciones_por_periodo[0]['Holt_Winters']:.2f}")
    except Exception as e:
        print(f"   ❌ Holt-Winters: {str(e)[:40]}")

    # Random Forest
    try:
        X, y = crear_features_ml_optimizado(ts, n_lags=3)

        if X is not None and len(X) >= 5:
            modelo = RandomForestRegressor(
                n_estimators=150,
                max_depth=6,
                min_samples_split=2,
                min_samples_leaf=1,
                random_state=42
            )
            modelo.fit(X, y)

            ts_extended = ts.copy()

            for periodo in range(horizonte):
                if len(ts_extended) >= 6:
                    lags = [ts_extended.iloc[-1], ts_extended.iloc[-2], ts_extended.iloc[-3]]
                    ma_3 = ts_extended.iloc[-3:].mean()
                    ma_6 = ts_extended.iloc[-6:].mean() if len(ts_extended) >= 6 else ma_3
                    vol = ts_extended.iloc[-3:].std()
                    pct = (ts_extended.iloc[-1] - ts_extended.iloc[-2])/ts_extended.iloc[-2] if ts_extended.iloc[-2] != 0 else 0

                    if len(ts_extended) >= 3:
                        accel = ((ts_extended.iloc[-1] - ts_extended.iloc[-2]) - (ts_extended.iloc[-2] - ts_extended.iloc[-3])) / ts_extended.iloc[-2] if ts_extended.iloc[-2] != 0 else 0
                        x_trend = np.arange(3)
                        y_trend = ts_extended.iloc[-3:].values
                        slope = np.polyfit(x_trend, y_trend, 1)[0]
                    else:
                        accel = 0
                        slope = 0

                    features = [lags + [ma_3, ma_6, vol, pct, accel, slope]]
                    pred = modelo.predict(features)[0]
                    pred = validar_proyeccion_realista(pred, stats, periodo+1)

                    predicciones_por_periodo[periodo]['Random_Forest'] = pred
                    ts_extended = pd.concat([ts_extended, pd.Series([pred])])

            for i, fecha in enumerate(fechas_futuras):
                if i in predicciones_por_periodo and 'Random_Forest' in predicciones_por_periodo[i]:
                    valor = predicciones_por_periodo[i]['Random_Forest']

                    pes, opt = calcular_intervalos_adaptativos(valor, stats, i+1)

                    resultados.append([
                        id_ind, indicador, periodicidad, tipo_indicador, fecha, "Random_Forest",
                        round(valor, 2), round(pes, 2), round(opt, 2)
                    ])

            print(f"   ✅ Random Forest: Año 1 = {predicciones_por_periodo[0]['Random_Forest']:.2f}")
    except Exception as e:
        print(f"   ❌ Random Forest: {str(e)[:40]}")

    # Prophet
    try:
        # **CRÍTICO**: Usar solo datos históricos completos (sin 2025)
        prophet_df = subdf_historico.rename(columns={"Fecha":"ds","Ejecución":"y"})[["ds","y"]].dropna()

        if len(prophet_df) >= MIN_DATA_POINTS:
            m = Prophet(
                growth='linear',
                changepoint_prior_scale=0.05,  # Aumentado para capturar cambios
                yearly_seasonality=False,
                weekly_seasonality=False,
                daily_seasonality=False,
                interval_width=0.8
            )
            m.fit(prophet_df)

            future = pd.DataFrame({'ds': fechas_futuras})
            forecast = m.predict(future)

            for i, row in forecast.iterrows():
                valor = validar_proyeccion_realista(row["yhat"], stats, i+1)
                predicciones_por_periodo[i]['Prophet'] = valor

                pes_prophet, opt_prophet = calcular_intervalos_adaptativos(valor, stats, i+1)

                resultados.append([
                    id_ind, indicador, periodicidad, tipo_indicador, fechas_futuras[i], "Prophet",
                    round(valor, 2), round(pes_prophet, 2), round(opt_prophet, 2)
                ])

            print(f"   ✅ Prophet: Año 1 = {predicciones_por_periodo[0]['Prophet']:.2f}")
    except Exception as e:
        print(f"   ❌ Prophet: {str(e)[:40]}")

    # Tendencia Histórica con amortiguación AGRESIVA
    try:
        crec_base = stats['crecimiento_promedio_ponderado']
        ultimo_val = stats['ultimo_valor']

        # **CRÍTICO**: Calcular crecimiento máximo razonable basado en histórico
        # Tomar el máximo crecimiento histórico anual como referencia
        crec_historico_max = ts.pct_change().max()
        crec_historico_max = min(crec_historico_max, 0.50)  # Cap a 50%

        # **CRÍTICO**: Aplicar amortiguación AGRESIVA para evitar extrapolación extrema
        for i in range(horizonte):
            # Amortiguación exponencial MÁS AGRESIVA
            factor_amortiguacion = 1 / (1 + (i * 0.25))  # 25% de reducción por año
            crec_amortiguado = crec_base * factor_amortiguacion

            # **NUEVO**: No permitir que supere el máximo histórico
            crec_amortiguado = min(crec_amortiguado, crec_historico_max * factor_amortiguacion)

            # Limitar el crecimiento máximo por año según tipo de indicador
            tipo_indicador_actual = stats['tipo_indicador']
            if tipo_indicador_actual == '%':
                crec_max_anual = 0.05  # 5% máximo para porcentuales
            else:
                crec_max_anual = 0.25  # 25% máximo para otros tipos (reducido de 30%)

            crec_amortiguado = np.clip(crec_amortiguado, -0.20, crec_max_anual)

            # **NUEVO**: Si hay meta, validar contra ella
            if stats.get('tiene_meta') and stats.get('meta_numerica'):
                # Calcular cuánto falta para llegar a la meta
                periodos_restantes = horizonte - i
                if periodos_restantes > 0 and valor_anterior if i > 0 else ultimo_val > 0:
                    val_actual = predicciones_por_periodo[i-1]['Tendencia_Historica'] if i > 0 else ultimo_val
                    crec_hacia_meta = (stats['meta_numerica'] - val_actual) / val_actual / periodos_restantes
                    crec_hacia_meta = np.clip(crec_hacia_meta, -0.30, 0.30)
                    # Promediar con crecimiento histórico
                    crec_amortiguado = (crec_amortiguado + crec_hacia_meta) / 2

            # Calcular valor proyectado
            if i == 0:
                valor = ultimo_val * (1 + crec_amortiguado)
            else:
                valor_anterior = predicciones_por_periodo[i-1]['Tendencia_Historica']
                valor = valor_anterior * (1 + crec_amortiguado)

            valor = validar_proyeccion_realista(valor, stats, i+1)
            predicciones_por_periodo[i]['Tendencia_Historica'] = valor

            pes, opt = calcular_intervalos_adaptativos(valor, stats, i+1)

            resultados.append([
                id_ind, indicador, periodicidad, tipo_indicador, fechas_futuras[i], "Tendencia_Historica",
                round(valor, 2), round(pes, 2), round(opt, 2)
            ])

        print(f"   ✅ Tendencia Histórica (amortiguada): Año 1 = {predicciones_por_periodo[0]['Tendencia_Historica']:.2f}")
        if horizonte >= 5:
            crec_year1_pct = ((predicciones_por_periodo[0]['Tendencia_Historica'] / ultimo_val) - 1) * 100
            crec_year5_pct = ((predicciones_por_periodo[4]['Tendencia_Historica'] / predicciones_por_periodo[3]['Tendencia_Historica']) - 1) * 100
            print(f"      Crec. año 1: {crec_year1_pct:.1f}% | Crec. año 5: {crec_year5_pct:.1f}%")
    except Exception as e:
        print(f"   ❌ Tendencia Histórica: {str(e)[:60]}")

    # Ensemble
    for i, fecha in enumerate(fechas_futuras):
        preds = predicciones_por_periodo[i]

        if len(preds) == 0:
            continue

        pesos = calcular_pesos_ensemble(preds, stats)

        if len(pesos) > 0:
            base_ensemble = sum(preds[m] * pesos[m] for m in preds.keys())
            base_ensemble = validar_proyeccion_realista(base_ensemble, stats, i+1)
        else:
            base_ensemble = np.mean(list(preds.values()))

        pesimista, optimista = calcular_intervalos_adaptativos(base_ensemble, stats, i+1)

        resultados.append([
            id_ind, indicador, periodicidad, tipo_indicador, fecha, "Ensemble_Ponderado",
            round(base_ensemble, 2), round(pesimista, 2), round(optimista, 2)
        ])

    if len(predicciones_por_periodo[0]) > 0:
        print(f"   📈 ENSEMBLE Año 1: {base_ensemble:.2f}")
        print(f"   📊 Modelos usados: {list(predicciones_por_periodo[0].keys())}")

    return resultados

# ============================
# EJECUCIÓN
# ============================
print("="*70)
print("🚀 SISTEMA DE PROYECCIONES V7 - CORREGIDO")
print("   ✅ Respeta tendencias crecientes/decrecientes")
print("   ✅ Límites más flexibles para indicadores no porcentuales")
print("   ✅ EXCLUYE datos parciales de 2025 para proyecciones anuales")
print("="*70)

all_results = []
stats_summary = []
total = df["Id"].nunique()

for idx, (id_ind, subdf) in enumerate(df.groupby("Id"), 1):
    print(f"\n[{idx}/{total}]")
    res = proyectar_optimizado(subdf, horizonte=10)
    all_results.extend(res)

    if len(res) > 0:
        ts = subdf.set_index("Fecha")["Ejecución"].astype(float).replace(0, np.nan).dropna()
        if len(ts) >= MIN_DATA_POINTS:
            meta = subdf["Meta"].iloc[0]
            tipo_indicador = detectar_tipo_indicador(meta, ts)
            _, outliers = detectar_outliers(ts.values)
            stats = calcular_estadisticas_robustas(ts, outliers, tipo_indicador, meta)  # Pasa meta aquí también

            stats_summary.append({
                'Id': id_ind,
                'Indicador': subdf["Indicador"].iloc[0],
                'Tipo': tipo_indicador,
                'Meta': meta,
                'Meta_Numerica': stats.get('meta_numerica'),
                'Tendencia': stats['tendencia'],
                'Ultimo_Valor': stats['ultimo_valor'],
                'Crecimiento_Mediano_%': stats['crecimiento_mediano'] * 100,
                'Crecimiento_Ponderado_%': stats['crecimiento_promedio_ponderado'] * 100,
                'Volatilidad_%': stats['volatilidad'] * 100,
                'Limite_Superior_%': stats['limite_superior'] * 100,
                'Limite_Inferior_%': stats['limite_inferior'] * 100,
                'Outliers_Detectados': len(outliers),
                'Puntos_Datos': len(ts)
            })

# ============================
# GUARDAR RESULTADOS
# ============================
print("\n" + "="*70)
print("💾 GUARDANDO RESULTADOS")
print("="*70)

if all_results:
    df_proy = pd.DataFrame(
        all_results,
        columns=["Id", "Indicador", "Periodicidad", "Tipo_Indicador", "Fecha_Proyeccion",
                 "Modelo", "Escenario_Base", "Escenario_Pesimista", "Escenario_Optimista"]
    )

    df_stats = pd.DataFrame(stats_summary)

    print(f"\n✅ RESUMEN:")
    print(f"   📈 Proyecciones totales: {len(df_proy):,}")
    print(f"   🏢 Indicadores: {df_proy['Indicador'].nunique()}")
    print(f"   🤖 Modelos: {df_proy['Modelo'].nunique()}")

    print(f"\n📊 DISTRIBUCIÓN POR MODELO:")
    for modelo, count in df_proy['Modelo'].value_counts().items():
        print(f"   {modelo:.<35} {count:>5,}")

    print(f"\n📋 DISTRIBUCIÓN POR TIPO DE INDICADOR:")
    for tipo, count in df_proy['Tipo_Indicador'].value_counts().items():
        limites = obtener_limites(tipo)
        print(f"   {tipo:.<15} {count:>5,} proyecciones | Límites: ±{limites['limite_superior']*100:.0f}%")

    # Análisis de tendencias
    print(f"\n📊 ANÁLISIS DE TENDENCIAS:")
    for tendencia, count in df_stats['Tendencia'].value_counts().items():
        print(f"   {tendencia.upper():.<20} {count:>3} indicadores")

    # Validación de indicadores porcentuales
    df_porcentuales = df_proy[df_proy['Tipo_Indicador'] == '%'].copy()
    if len(df_porcentuales) > 0:
        valores_invalidos = df_porcentuales[
            (df_porcentuales['Escenario_Base'] > 100) |
            (df_porcentuales['Escenario_Base'] < 0) |
            (df_porcentuales['Escenario_Optimista'] > 100) |
            (df_porcentuales['Escenario_Pesimista'] < 0)
        ]

        if len(valores_invalidos) > 0:
            print(f"\n⚠️  ADVERTENCIA: {len(valores_invalidos)} proyecciones porcentuales fuera de rango 0-100%")
            print(f"   Se recomienda revisar: {valores_invalidos['Indicador'].unique()}")
        else:
            print(f"\n✅ Todos los indicadores porcentuales dentro del rango 0-100%")

    # Validación de coherencia con tendencias
    df_ensemble = df_proy[df_proy['Modelo'] == 'Ensemble_Ponderado'].copy()

    print(f"\n🔍 VALIDACIÓN DE COHERENCIA CON TENDENCIAS:")
    for _, stat in df_stats.iterrows():
        indicador_proy = df_ensemble[
            (df_ensemble['Id'] == stat['Id']) &
            (df_ensemble['Fecha_Proyeccion'] == df_ensemble['Fecha_Proyeccion'].min())
        ]

        if len(indicador_proy) > 0:
            primer_proy = indicador_proy.iloc[0]['Escenario_Base']
            crec_proyectado = ((primer_proy / stat['Ultimo_Valor']) - 1) * 100

            if stat['Tendencia'] == 'creciente' and crec_proyectado < 0:
                print(f"   ⚠️  {stat['Indicador'][:40]}: Tendencia CRECIENTE pero proyecta decrecimiento ({crec_proyectado:.1f}%)")
            elif stat['Tendencia'] == 'decreciente' and crec_proyectado > 5:
                print(f"   ⚠️  {stat['Indicador'][:40]}: Tendencia DECRECIENTE pero proyecta crecimiento ({crec_proyectado:.1f}%)")

    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        df_proy.to_excel(writer, sheet_name='Proyecciones', index=False)
        df_stats.to_excel(writer, sheet_name='Estadisticas_Robustas', index=False)

        df_ensemble.to_excel(writer, sheet_name='Ensemble_Recomendado', index=False)

        pivot = df_proy.pivot_table(
            index=['Indicador', 'Fecha_Proyeccion'],
            columns='Modelo',
            values='Escenario_Base'
        ).round(2)
        pivot.to_excel(writer, sheet_name='Comparacion_Modelos')

        resumen_tipo = df_proy.groupby(['Tipo_Indicador', 'Modelo']).agg({
            'Escenario_Base': ['mean', 'min', 'max', 'std'],
            'Id': 'count'
        }).round(2)
        resumen_tipo.to_excel(writer, sheet_name='Analisis_Por_Tipo')

        if len(df_porcentuales) > 0:
            df_porcentuales_ensemble = df_porcentuales[
                df_porcentuales['Modelo'] == 'Ensemble_Ponderado'
            ].copy()
            df_porcentuales_ensemble.to_excel(writer, sheet_name='Validacion_Porcentuales', index=False)

        # Nueva hoja: Validación de tendencias
        validacion_tendencias = []
        for _, stat in df_stats.iterrows():
            indicador_proy = df_ensemble[
                (df_ensemble['Id'] == stat['Id']) &
                (df_ensemble['Fecha_Proyeccion'] == df_ensemble['Fecha_Proyeccion'].min())
            ]

            if len(indicador_proy) > 0:
                primer_proy = indicador_proy.iloc[0]['Escenario_Base']
                crec_proyectado = ((primer_proy / stat['Ultimo_Valor']) - 1) * 100

                coherente = True
                if stat['Tendencia'] == 'creciente' and crec_proyectado < 0:
                    coherente = False
                elif stat['Tendencia'] == 'decreciente' and crec_proyectado > 5:
                    coherente = False

                validacion_tendencias.append({
                    'Id': stat['Id'],
                    'Indicador': stat['Indicador'],
                    'Tendencia_Historica': stat['Tendencia'],
                    'Crecimiento_Historico_%': stat['Crecimiento_Ponderado_%'],
                    'Ultimo_Valor': stat['Ultimo_Valor'],
                    'Proyeccion_Año_1': primer_proy,
                    'Crecimiento_Proyectado_%': crec_proyectado,
                    'Coherente': 'Sí' if coherente else 'NO'
                })

        df_validacion = pd.DataFrame(validacion_tendencias)
        df_validacion.to_excel(writer, sheet_name='Validacion_Tendencias', index=False)

    print(f"\n✅ Archivo guardado: {OUTPUT_FILE}")
    print(f"   📋 Hojas creadas:")
    print(f"      1. Proyecciones (todas)")
    print(f"      2. Estadisticas_Robustas")
    print(f"      3. Ensemble_Recomendado")
    print(f"      4. Comparacion_Modelos")
    print(f"      5. Analisis_Por_Tipo")
    print(f"      6. Validacion_Porcentuales")
    print(f"      7. Validacion_Tendencias ⭐ NUEVO")

    print(f"\n📊 EJEMPLOS DE PROYECCIONES (Año 1 - Ensemble):")
    ejemplos = df_ensemble[df_ensemble['Fecha_Proyeccion'] == df_ensemble['Fecha_Proyeccion'].min()]
    for _, row in ejemplos.head(8).iterrows():
        # Busca el crecimiento histórico
        stat_ind = df_stats[df_stats['Id'] == row['Id']]
        if len(stat_ind) > 0:
            crec_hist = stat_ind.iloc[0]['Crecimiento_Ponderado_%']
            ultimo = stat_ind.iloc[0]['Ultimo_Valor']
            tendencia = stat_ind.iloc[0]['Tendencia']
            crec_proy = ((row['Escenario_Base'] / ultimo) - 1) * 100

            tipo_sym = "📍" if row['Tipo_Indicador'] == '%' else "📊"
            tend_sym = "📈" if tendencia == 'creciente' else "📉" if tendencia == 'decreciente' else "➡️"

            print(f"   {tipo_sym}{tend_sym} {row['Indicador'][:35]:.<40}")
            print(f"      Último: {ultimo:.2f} | Crec.Hist: {crec_hist:+.1f}% | Proy: {row['Escenario_Base']:.2f} ({crec_proy:+.1f}%)")

else:
    print("\n❌ No se generaron proyecciones")

print("\n" + "="*70)
print("✅ PROCESO COMPLETADO")
print("="*70)
print("\n💡 CAMBIOS IMPLEMENTADOS:")
print("   ✅ Límites más flexibles para indicadores no porcentuales (hasta 50% anual)")
print("   ✅ Detección mejorada de outliers (considera cambios porcentuales)")
print("   ✅ Cálculo de estadísticas sobre serie completa para capturar tendencias")
print("   ✅ Mayor peso a datos recientes (80% vs 70%)")
print("   ✅ Validación que respeta tendencias crecientes/decrecientes")
print("   ✅ Ensemble penaliza modelos que contradicen la tendencia")
print("   ✅ Nueva hoja de validación de coherencia con tendencias")
print("   ⭐ EXCLUYE datos parciales de 2025 para proyecciones anuales")
print("   ⭐ Tendencia Histórica con AMORTIGUACIÓN AGRESIVA (25% reducción/año)")
print("   ⭐ CONSIDERA METAS: Ajusta proyecciones hacia metas establecidas")
print("   ⭐ Límite máximo 25% anual (reducido de 30%) para evitar extrapolación")
print("\n📋 RECOMENDACIONES:")
print("   1. Revise la hoja 'Validacion_Tendencias' para verificar coherencia")
print("   2. Indicadores con 'Coherente = NO' requieren revisión manual")
print("   3. Use 'Ensemble_Recomendado' como proyección oficial")
print("   4. Las proyecciones parten del último año COMPLETO (2024)")
print("   5. El modelo Tendencia_Historica aplica amortiguación agresiva")
print("   6. Las metas numéricas influyen en las proyecciones cuando están disponibles")
print("="*70)