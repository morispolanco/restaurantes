import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta, datetime

# Configuración de la página
st.set_page_config(page_title="Sistema de Gestión de Restaurante", page_icon="🍽️", layout="wide")

# Estilos CSS
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.5rem;
        font-weight: 600;
        color: #34495e;
        margin-bottom: 0.5rem;
    }
    .card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3498db;
    }
    .metric-label {
        font-size: 1rem;
        color: #7f8c8d;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión para datos si no existe
if 'reservations' not in st.session_state:
    # Crear algunos datos de ejemplo
    start_date = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    example_reservations = []
    
    # Nombres comunes en español
    names = ["García", "Rodríguez", "López", "Martínez", "González", "Pérez", "Sánchez", 
             "Fernández", "Torres", "Ramírez", "Flores", "Díaz", "Morales", "Ruiz"]
    
    # Generar 20 reservas de ejemplo
    for i in range(20):
        hour = np.random.choice([12, 13, 14, 19, 20, 21])
        minute = np.random.choice([0, 15, 30, 45])
        day_offset = np.random.randint(0, 7)
        
        reservation_time = start_date + timedelta(days=day_offset, hours=(hour-12), minutes=minute)
        party_size = np.random.randint(1, 9)
        
        example_reservations.append({
            "id": i+1,
            "nombre": np.random.choice(names),
            "telefono": f"+34 6{np.random.randint(10, 100)} {np.random.randint(100, 1000)} {np.random.randint(100, 1000)}",
            "fecha": reservation_time,
            "comensales": party_size,
            "mesa": np.random.randint(1, 16) if np.random.random() > 0.2 else None,
            "estado": np.random.choice(["Confirmada", "Pendiente", "Completada", "Cancelada"], 
                                     p=[0.6, 0.2, 0.1, 0.1]),
            "notas": np.random.choice(["", "Alergia a frutos secos", "Celebración de cumpleaños", 
                                      "Prefieren mesa interior", "Solicitan trona para bebé"], 
                                     p=[0.7, 0.1, 0.1, 0.05, 0.05])
        })
    
    st.session_state.reservations = pd.DataFrame(example_reservations)

if 'tables' not in st.session_state:
    # Crear datos de mesas
    tables = []
    for i in range(15):
        capacity = 2 if i < 5 else 4 if i < 10 else 6 if i < 13 else 8
        tables.append({
            "numero": i+1,
            "capacidad": capacity,
            "ubicacion": np.random.choice(["Interior", "Exterior", "Terraza"]),
            "estado": np.random.choice(["Libre", "Ocupada", "Reservada"], p=[0.5, 0.3, 0.2])
        })
    
    st.session_state.tables = pd.DataFrame(tables)

# Filtro de fecha para toda la aplicación
st.sidebar.markdown("<div class='subtitle'>Filtros Generales</div>", unsafe_allow_html=True)
today = datetime.now().date()
selected_date = st.sidebar.date_input("Fecha", today)

# Navegación
st.sidebar.markdown("<div class='subtitle'>Navegación</div>", unsafe_allow_html=True)
page = st.sidebar.radio("Ir a:", ["Panel Principal", "Reservas", "Gestión de Mesas", "Análisis"])

# Función para mostrar el panel principal
def show_dashboard():
    st.markdown("<div class='title'>Panel de Control</div>", unsafe_allow_html=True)
    
    # Filtrar datos por la fecha seleccionada
    selected_datetime = datetime.combine(selected_date, datetime.min.time())
    next_day = selected_datetime + timedelta(days=1)
    
    daily_reservations = st.session_state.reservations[(st.session_state.reservations.fecha >= selected_datetime) & 
                                                     (st.session_state.reservations.fecha < next_day)]
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{len(daily_reservations)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Reservas Hoy</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        expected_guests = daily_reservations.comensales.sum()
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{expected_guests}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Comensales Esperados</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        tables_in_use = len(st.session_state.tables[st.session_state.tables.estado != "Libre"])
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{tables_in_use}/{len(st.session_state.tables)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Mesas Ocupadas</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        confirmed = len(daily_reservations[daily_reservations.estado == "Confirmada"])
        pending = len(daily_reservations[daily_reservations.estado == "Pendiente"])
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{confirmed}/{confirmed+pending}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Reservas Confirmadas</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Gráficos y visualizaciones
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Distribución de Reservas por Hora</div>", unsafe_allow_html=True)
        
        # Agrupar reservas por hora
        daily_reservations['hora'] = daily_reservations.fecha.dt.hour
        hourly_counts = daily_reservations.groupby('hora').size().reset_index(name='count')
        
        fig = px.bar(hourly_counts, x='hora', y='count', 
                   labels={'hora': 'Hora del Día', 'count': 'Número de Reservas'},
                   color_discrete_sequence=['#3498db'])
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Estado de Mesas</div>", unsafe_allow_html=True)
        
        # Contar mesas por estado
        table_status = st.session_state.tables.estado.value_counts().reset_index()
        table_status.columns = ['Estado', 'Cantidad']
        
        fig = px.pie(table_status, values='Cantidad', names='Estado', 
                   color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12'])
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Próximas reservas
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Próximas Reservas</div>", unsafe_allow_html=True)
    
    now = datetime.now()
    upcoming = daily_reservations[daily_reservations.fecha >= now].sort_values('fecha').head(5)
    
    if len(upcoming) > 0:
        for _, res in upcoming.iterrows():
            status_color = {"Confirmada": "green", "Pendiente": "orange", 
                           "Completada": "blue", "Cancelada": "red"}
            
            st.markdown(f"""
            <div style="border-left: 4px solid {status_color[res.estado]}; padding-left: 10px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong>{res.nombre}</strong> - {res.comensales} personas
                    </div>
                    <div>
                        {res.fecha.strftime('%H:%M')} ({(res.fecha - now).seconds // 60} min)
                    </div>
                </div>
                <div style="color: gray; font-size: 0.9rem;">
                    Mesa: {res.mesa if pd.notna(res.mesa) else 'Sin asignar'} | 
                    Tel: {res.telefono} | 
                    {res.estado}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No hay próximas reservas para hoy.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Función para gestionar reservas
def manage_reservations():
    st.markdown("<div class='title'>Gestión de Reservas</div>", unsafe_allow_html=True)
    
    # Filtrar reservas por fecha
    selected_datetime = datetime.combine(selected_date, datetime.min.time())
    next_day = selected_datetime + timedelta(days=1)
    
    daily_reservations = st.session_state.reservations[(st.session_state.reservations.fecha >= selected_datetime) & 
                                                     (st.session_state.reservations.fecha < next_day)]
    
    # Tabs para diferentes operaciones
    tab1, tab2, tab3 = st.tabs(["Ver Reservas", "Nueva Reserva", "Búsqueda"])
    
    with tab1:
        # Filtros adicionales
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect("Estado", 
                                          options=["Confirmada", "Pendiente", "Completada", "Cancelada"],
                                          default=["Confirmada", "Pendiente"])
        
        with col2:
            time_filter = st.multiselect("Horario", 
                                        options=["Comida (12-16h)", "Cena (19-23h)"],
                                        default=["Comida (12-16h)", "Cena (19-23h)"])
        
        with col3:
            table_filter = st.checkbox("Solo sin mesa asignada", False)
        
        # Aplicar filtros
        filtered_df = daily_reservations.copy()
        
        if status_filter:
            filtered_df = filtered_df[filtered_df.estado.isin(status_filter)]
        
        if time_filter:
            mask = pd.Series(False, index=filtered_df.index)
            if "Comida (12-16h)" in time_filter:
                mask = mask | ((filtered_df.fecha.dt.hour >= 12) & (filtered_df.fecha.dt.hour < 16))
            if "Cena (19-23h)" in time_filter:
                mask = mask | ((filtered_df.fecha.dt.hour >= 19) & (filtered_df.fecha.dt.hour < 23))
            filtered_df = filtered_df[mask]
        
        if table_filter:
            filtered_df = filtered_df[filtered_df.mesa.isna()]
        
        # Mostrar reservas filtradas
        if not filtered_df.empty:
            st.dataframe(filtered_df[['id', 'nombre', 'fecha', 'comensales', 'mesa', 'estado', 'telefono', 'notas']], 
                       column_config={
                           "id": "ID",
                           "nombre": "Nombre",
                           "fecha": st.column_config.DatetimeColumn("Fecha y Hora", format="DD/MM/YYYY HH:mm"),
                           "comensales": "Comensales",
                           "mesa": "Mesa",
                           "estado": st.column_config.SelectboxColumn("Estado", options=["Confirmada", "Pendiente", "Completada", "Cancelada"]),
                           "telefono": "Teléfono",
                           "notas": "Notas"
                       },
                       hide_index=True,
                       use_container_width=True,
                       height=400,
                       on_change=lambda: 1)  # Función dummy para el ejemplo
        else:
            st.info("No hay reservas que coincidan con los filtros seleccionados.")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Nombre del cliente")
            new_phone = st.text_input("Teléfono")
            new_size = st.number_input("Número de comensales", min_value=1, max_value=20, value=2)
        
        with col2:
            new_date = st.date_input("Fecha de reserva", selected_date)
            new_time = st.time_input("Hora", datetime.now().replace(hour=14, minute=0).time())
            new_status = st.selectbox("Estado", ["Confirmada", "Pendiente"])
        
        new_table = st.selectbox("Mesa (opcional)", 
                              options=[None] + list(st.session_state.tables[st.session_state.tables.estado == "Libre"].numero.values))
        
        new_notes = st.text_area("Notas adicionales")
        
        if st.button("Crear Reserva"):
            # Preparar la nueva entrada
            new_id = st.session_state.reservations.id.max() + 1 if len(st.session_state.reservations) > 0 else 1
            new_datetime = datetime.combine(new_date, new_time)
            
            new_reservation = pd.DataFrame([{
                "id": new_id,
                "nombre": new_name,
                "telefono": new_phone,
                "fecha": new_datetime,
                "comensales": new_size,
                "mesa": new_table,
                "estado": new_status,
                "notas": new_notes
            }])
            
            # Añadir a las reservas existentes
            st.session_state.reservations = pd.concat([st.session_state.reservations, new_reservation], ignore_index=True)
            
            # Actualizar estado de la mesa si se ha asignado
            if new_table is not None:
                st.session_state.tables.loc[st.session_state.tables.numero == new_table, 'estado'] = "Reservada"
            
            st.success(f"Reserva creada con éxito (ID: {new_id})")
    
    with tab3:
        search_query = st.text_input("Buscar por nombre o teléfono")
        
        if search_query:
            # Buscar en todas las reservas, no solo en las del día
            search_results = st.session_state.reservations[
                st.session_state.reservations.nombre.str.contains(search_query, case=False) | 
                st.session_state.reservations.telefono.str.contains(search_query, case=False)
            ]
            
            if not search_results.empty:
                st.dataframe(search_results[['id', 'nombre', 'fecha', 'comensales', 'mesa', 'estado', 'telefono']], 
                           hide_index=True, 
                           use_container_width=True)
            else:
                st.info("No se encontraron resultados.")

# Función para gestionar mesas
def manage_tables():
    st.markdown("<div class='title'>Gestión de Mesas</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Mapa de Mesas</div>", unsafe_allow_html=True)
        
        # Crear mapa visual de mesas
        tables_df = st.session_state.tables.copy()
        
        # Definir colores por estado
        color_map = {"Libre": "green", "Ocupada": "red", "Reservada": "orange"}
        tables_df['color'] = tables_df.estado.map(color_map)
        
        # Crear coordenadas para visualización
        tables_per_row = 5
        tables_df['x'] = tables_df.index % tables_per_row
        tables_df['y'] = tables_df.index // tables_per_row
        
        # Crear figura con plotly
        fig = go.Figure()
        
        # Añadir mesas como círculos
        for _, table in tables_df.iterrows():
            fig.add_trace(go.Scatter(
                x=[table.x],
                y=[table.y],
                mode='markers+text',
                marker=dict(
                    size=table.capacidad * 5,  # Tamaño según capacidad
                    color=table.color,
                    line=dict(width=2, color='white')
                ),
                text=[f"{table.numero}"],
                textposition="middle center",
                hoverinfo="text",
                hovertext=f"Mesa {table.numero}<br>Capacidad: {table.capacidad}<br>Estado: {table.estado}<br>Ubicación: {table.ubicacion}"
            ))
        
        # Configuración de layout
        fig.update_layout(
            showlegend=False,
            margin=dict(l=5, r=5, t=5, b=5),
            height=400,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            plot_bgcolor='rgba(240,240,240,0.8)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Leyenda
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("🟢 Libre")
        with col_b:
            st.markdown("🟠 Reservada")
        with col_c:
            st.markdown("🔴 Ocupada")
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Detalles de Mesa</div>", unsafe_allow_html=True)
        
        selected_table = st.selectbox("Seleccionar Mesa", options=tables_df.numero.tolist())
        
        if selected_table:
            table_data = tables_df[tables_df.numero == selected_table].iloc[0]
            
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 5px; background-color: #f8f9fa;">
                <h3>Mesa {selected_table}</h3>
                <p><strong>Capacidad:</strong> {table_data.capacidad} personas</p>
                <p><strong>Ubicación:</strong> {table_data.ubicacion}</p>
                <p><strong>Estado:</strong> <span style="color: {color_map[table_data.estado]};">{table_data.estado}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Buscar reservas para esta mesa
            table_reservations = st.session_state.reservations[
                (st.session_state.reservations.mesa == selected_table) & 
                (st.session_state.reservations.fecha.dt.date == selected_date)
            ]
            
            if not table_reservations.empty:
                st.markdown("<p><strong>Reservas para hoy:</strong></p>", unsafe_allow_html=True)
                for _, res in table_reservations.iterrows():
                    st.markdown(f"""
                    <div style="margin-top: 10px; padding: 5px 10px; border-left: 3px solid {color_map[res.estado]};">
                        <div><strong>{res.nombre}</strong> - {res.comensales} personas</div>
                        <div>{res.fecha.strftime('%H:%M')} | {res.estado}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<p>No hay reservas para esta mesa hoy.</p>", unsafe_allow_html=True)
            
            # Cambiar estado
            new_status = st.selectbox("Cambiar estado", 
                                   options=["Libre", "Ocupada", "Reservada"],
                                   index=["Libre", "Ocupada", "Reservada"].index(table_data.estado))
            
            if st.button("Actualizar Estado"):
                st.session_state.tables.loc[st.session_state.tables.numero == selected_table, 'estado'] = new_status
                st.success(f"Estado de mesa {selected_table} actualizado a {new_status}")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Función para mostrar análisis
def show_analysis():
    st.markdown("<div class='title'>Análisis de Datos</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Ocupación Semanal</div>", unsafe_allow_html=True)
        
        # Generar datos para la semana
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
        
        # Filtrar reservas para la semana actual
        week_start = datetime.combine(start_of_week, datetime.min.time())
        week_end = datetime.combine(week_dates[-1], datetime.max.time())
        
        week_reservations = st.session_state.reservations[
            (st.session_state.reservations.fecha >= week_start) & 
            (st.session_state.reservations.fecha <= week_end)
        ]
        
        # Agrupar por día
        week_reservations['dia'] = week_reservations.fecha.dt.date
        daily_customers = week_reservations.groupby('dia')['comensales'].sum().reindex(week_dates, fill_value=0)
        
        # Crear gráfico
        fig = px.bar(
            x=[d.strftime("%a %d/%m") for d in daily_customers.index],
            y=daily_customers.values,
            labels={'x': 'Día', 'y': 'Comensales'},
            title="Ocupación por Día de la Semana",
            color_discrete_sequence=['#3498db']
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Distribución de Comensales</div>", unsafe_allow_html=True)
        
        # Agrupar por tamaño de grupo
        size_distribution = st.session_state.reservations.groupby('comensales').size()
        
        fig = px.pie(
            names=size_distribution.index,
            values=size_distribution.values,
            title="Distribución por Tamaño de Grupo",
            color_discrete_sequence=px.colors.sequential.Blues
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Heatmap de ocupación por hora y día
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Mapa de Calor de Ocupación</div>", unsafe_allow_html=True)
    
    # Preparar datos
    all_reservations = st.session_state.reservations.copy()
    all_reservations['dia_semana'] = all_reservations.fecha.dt.day_name()
    all_reservations['hora'] = all_reservations.fecha.dt.hour
    
    # Días de la semana en español y en orden
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    day_map = {
        'Monday': 'Lunes', 
        'Tuesday': 'Martes', 
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves', 
        'Friday': 'Viernes', 
        'Saturday': 'Sábado', 
        'Sunday': 'Domingo'
    }
    
    all_reservations['dia_semana'] = all_reservations['dia_semana'].map(day_map)
    
    # Crear pivot table para el heatmap
    heatmap_data = all_reservations.pivot_table(
        index='hora',
        columns='dia_semana',
        values='comensales',
        aggfunc='sum',
        fill_value=0
    ).reindex(columns=dias)
    
    # Filtrar solo horas de servicio
    service_hours = list(range(12, 16)) + list(range(19, 23))
    heatmap_data = heatmap_data.loc[heatmap_data.index.isin(service_hours)]
    
    # Crear heatmap
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Día", y="Hora", color="Comensales"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale='YlGnBu'
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Métricas de rendimiento
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Métricas de Rendimiento</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Tasa de conversión de reservas
        completed = len(st.session_state.reservations[st.session_state.reservations.estado == "Completada"])
        cancelled = len(st.session_state.reservations[st.session_state.reservations.estado == "Cancelada"])
        total = len(st.session_state.reservations)
        
        conversion_rate = completed / total * 100 if total > 0 else 0
        cancellation_rate = cancelled / total * 100 if total > 0 else 0
        
        st.metric("Tasa de Conversión", f"{conversion_rate:.1f}%", 
                delta=f"-{cancellation_rate:.1f}%" if cancellation_rate > 0 else None,
                delta_color="inverse")
    
    with col2:
        # Promedio de comensales por reserva
        avg_party_size = st.session_state.reservations.comensales.mean()
        st.metric("Promedio Comensales", f"{avg_party_size:.1f}")
    
    with col3:
        # Rotación de mesas (estimado)
        table_capacity = st.session_state.tables.capacidad.sum()
        total_customers = st.session_state.reservations[
            st.session_state.reservations.estado.isin(["Completada", "Confirmada"])
        ].comensales.sum()
         
        # Estimación simple de rotación
        rotation_estimate = total_customers / table_capacity if table_capacity > 0 else 0
        
        st.metric("Índice de Rotación", f"{rotation_estimate:.2f}x")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # KPIs y recomendaciones
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Recomendaciones</div>", unsafe_allow_html=True)
    
    # Calcular horas pico basadas en datos históricos
    peak_hours = all_reservations.groupby('hora')['comensales'].sum().sort_values(ascending=False).head(3)
    
    # Identificar días más ocupados
    busy_days = all_reservations.groupby('dia_semana')['comensales'].sum().sort_values(ascending=False).head(2)
    
    # Tamaño promedio de grupo
    avg_group = all_reservations.comensales.mean()
    
    st.markdown(f"""
    <div style="background-color: #f0f7ff; padding: 15px; border-radius: 5px; margin-top: 10px;">
        <h4>Análisis de Operaciones</h4>
        <ul>
            <li>Las horas pico de servicio son: {', '.join([f"{h}:00" for h in peak_hours.index])}</li>
            <li>Los días más ocupados son: {', '.join(busy_days.index)}</li>
            <li>El tamaño promedio de grupo es de {avg_group:.1f} personas</li>
        </ul>
        
        <h4>Recomendaciones:</h4>
        <ul>
            <li>Considere aumentar el personal durante {', '.join([f"{h}:00" for h in peak_hours.index])} para mejorar el servicio.</li>
            <li>Reorganice las mesas para optimizar el espacio según el tamaño promedio de grupo.</li>
            <li>Ofrezca promociones en días menos concurridos para equilibrar la ocupación semanal.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Renderizar la página seleccionada
if page == "Panel Principal":
    show_dashboard()
elif page == "Reservas":
    manage_reservations()
elif page == "Gestión de Mesas":
    manage_tables()
elif page == "Análisis":
    show_analysis()
