import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
    start_date = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    example_reservations = []
    
    names = ["García", "Rodríguez", "López", "Martínez", "González", "Pérez", "Sánchez", 
             "Fernández", "Torres", "Ramírez", "Flores", "Díaz", "Morales", "Ruiz"]
    
    for i in range(20):
        hour = np.random.choice([12, 13, 14, 19, 20, 21])
        minute = np.random.choice([0, 15, 30, 45])
        day_offset = np.random.randint(0, 7)
        
        reservation_time = start_date.replace(hour=hour, minute=minute) + timedelta(days=day_offset)
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

def show_dashboard():
    st.markdown("<div class='title'>Panel de Control</div>", unsafe_allow_html=True)
    
    selected_datetime = datetime.combine(selected_date, datetime.min.time())
    next_day = selected_datetime + timedelta(days=1)
    
    daily_reservations = st.session_state.reservations[(st.session_state.reservations['fecha'] >= selected_datetime) & 
                                                     (st.session_state.reservations['fecha'] < next_day)].copy()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{len(daily_reservations)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Reservas Hoy</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        expected_guests = daily_reservations['comensales'].sum()
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{expected_guests}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Comensales Esperados</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        tables_in_use = len(st.session_state.tables[st.session_state.tables['estado'] != "Libre"])
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{tables_in_use}/{len(st.session_state.tables)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Mesas Ocupadas</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        confirmed = len(daily_reservations[daily_reservations['estado'] == "Confirmada"])
        pending = len(daily_reservations[daily_reservations['estado'] == "Pendiente"])
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{confirmed}/{confirmed+pending}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Reservas Confirmadas</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Distribución de Reservas por Hora</div>", unsafe_allow_html=True)
        
        daily_reservations['hora'] = daily_reservations['fecha'].dt.hour
        hourly_counts = daily_reservations.groupby('hora').size().reindex(range(12, 24), fill_value=0).reset_index(name='count')
        hourly_counts['hora'] = hourly_counts['hora'].astype(int)
        
        fig = px.bar(hourly_counts, x='hora', y='count',
                    labels={'hora': 'Hora del Día', 'count': 'Número de Reservas'},
                    color_discrete_sequence=['#3498db'])
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Estado de Mesas</div>", unsafe_allow_html=True)
        
        table_status = st.session_state.tables['estado'].value_counts().reset_index()
        table_status.columns = ['Estado', 'Cantidad']
        
        fig = px.pie(table_status, values='Cantidad', names='Estado',
                    color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12'])
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Próximas Reservas</div>", unsafe_allow_html=True)
    
    now = datetime.now()
    upcoming = daily_reservations[daily_reservations['fecha'] >= now].sort_values('fecha').head(5)
    
    if not upcoming.empty:
        status_color = {
            "Confirmada": "green",
            "Pendiente": "orange",
            "Completada": "blue",
            "Cancelada": "red"
        }
        
        for idx, res in upcoming.iterrows():
            time_diff = (res['fecha'] - now).total_seconds() / 60
            st.markdown(f"""
            <div style="border-left: 4px solid {status_color[res['estado']]}; padding-left: 10px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong>{res['nombre']}</strong> - {res['comensales']} personas
                    </div>
                    <div>
                        {res['fecha'].strftime('%H:%M')} ({int(time_diff)} min)
                    </div>
                </div>
                <div style="color: gray; font-size: 0.9rem;">
                    Mesa: {res['mesa'] if pd.notna(res['mesa']) else 'Sin asignar'} | 
                    Tel: {res['telefono']} | 
                    {res['estado']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No hay próximas reservas para hoy.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def manage_reservations():
    st.markdown("<div class='title'>Gestión de Reservas</div>", unsafe_allow_html=True)
    
    selected_datetime = datetime.combine(selected_date, datetime.min.time())
    next_day = selected_datetime + timedelta(days=1)
    
    daily_reservations = st.session_state.reservations[
        (st.session_state.reservations['fecha'] >= selected_datetime) &
        (st.session_state.reservations['fecha'] < next_day)
    ].copy()
    
    tab1, tab2, tab3 = st.tabs(["Ver Reservas", "Nueva Reserva", "Búsqueda"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect(
                "Estado",
                options=["Confirmada", "Pendiente", "Completada", "Cancelada"],
                default=["Confirmada", "Pendiente"]
            )
        
        with col2:
            time_filter = st.multiselect(
                "Horario",
                options=["Comida (12-16h)", "Cena (19-23h)"],
                default=["Comida (12-16h)", "Cena (19-23h)"]
            )
        
        with col3:
            table_filter = st.checkbox("Solo sin mesa asignada", False)
        
        filtered_df = daily_reservations.copy()
        
        if status_filter:
            filtered_df = filtered_df[filtered_df['estado'].isin(status_filter)]
        
        if time_filter:
            mask = pd.Series(False, index=filtered_df.index)
            if "Comida (12-16h)" in time_filter:
                mask |= ((filtered_df['fecha'].dt.hour >= 12) & (filtered_df['fecha'].dt.hour < 16))
            if "Cena (19-23h)" in time_filter:
                mask |= ((filtered_df['fecha'].dt.hour >= 19) & (filtered_df['fecha'].dt.hour < 23))
            filtered_df = filtered_df[mask]
        
        if table_filter:
            filtered_df = filtered_df[filtered_df['mesa'].isna()]
        
        if not filtered_df.empty:
            st.write("### Lista de Reservas")
            for idx, row in filtered_df.iterrows():
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.write(f"ID: {row['id']} | {row['nombre']} | {row['fecha'].strftime('%d/%m/%Y %H:%M')} | "
                            f"{row['comensales']} personas | Mesa: {row['mesa'] if pd.notna(row['mesa']) else 'Sin asignar'} | "
                            f"{row['estado']}")
                with col_b:
                    if st.button("Editar", key=f"edit_{row['id']}"):
                        st.session_state.edit_reservation_id = row['id']
                with col_c:
                    if st.button("Borrar", key=f"delete_{row['id']}"):
                        if pd.notna(row['mesa']):
                            st.session_state.tables.loc[
                                st.session_state.tables['numero'] == row['mesa'], 'estado'
                            ] = "Libre"
                        st.session_state.reservations = st.session_state.reservations[
                            st.session_state.reservations['id'] != row['id']
                        ]
                        st.success(f"Reserva ID {row['id']} borrada con éxito")
                        st.rerun()
            
            if 'edit_reservation_id' in st.session_state:
                reservation_to_edit = st.session_state.reservations[
                    st.session_state.reservations['id'] == st.session_state.edit_reservation_id
                ].iloc[0]
                
                st.write("### Editar Reserva")
                edit_col1, edit_col2 = st.columns(2)
                
                with edit_col1:
                    edit_name = st.text_input("Nombre del cliente", value=reservation_to_edit['nombre'], key="edit_name")
                    edit_phone = st.text_input("Teléfono", value=reservation_to_edit['telefono'], key="edit_phone")
                    edit_size = st.number_input("Número de comensales", min_value=1, max_value=20, 
                                              value=int(reservation_to_edit['comensales']), key="edit_size")
                
                with edit_col2:
                    edit_date = st.date_input("Fecha de reserva", value=reservation_to_edit['fecha'].date(), key="edit_date")
                    edit_time = st.time_input("Hora", value=reservation_to_edit['fecha'].time(), key="edit_time")
                    edit_status = st.selectbox("Estado", ["Confirmada", "Pendiente", "Completada", "Cancelada"],
                                             index=["Confirmada", "Pendiente", "Completada", "Cancelada"].index(reservation_to_edit['estado']),
                                             key="edit_status")
                
                edit_table = st.selectbox(
                    "Mesa (opcional)",
                    options=[None] + st.session_state.tables[
                        st.session_state.tables['estado'] == "Libre"
                    ]['numero'].tolist(),
                    index=0 if pd.isna(reservation_to_edit['mesa']) else 
                          st.session_state.tables[st.session_state.tables['estado'] == "Libre"]['numero'].tolist().index(reservation_to_edit['mesa']) + 1 if reservation_to_edit['mesa'] in st.session_state.tables[st.session_state.tables['estado'] == "Libre"]['numero'].tolist() else 0,
                    key="edit_table"
                )
                edit_notes = st.text_area("Notas adicionales", value=reservation_to_edit['notas'], key="edit_notes")
                
                if st.button("Guardar Cambios", key="save_edit"):
                    if not edit_name or not edit_phone:
                        st.error("Nombre y teléfono son obligatorios")
                    else:
                        old_table = reservation_to_edit['mesa']
                        if pd.notna(old_table) and old_table != edit_table:
                            st.session_state.tables.loc[
                                st.session_state.tables['numero'] == old_table, 'estado'
                            ] = "Libre"
                        
                        new_datetime = datetime.combine(edit_date, edit_time)
                        st.session_state.reservations.loc[
                            st.session_state.reservations['id'] == st.session_state.edit_reservation_id,
                            ['nombre', 'telefono', 'fecha', 'comensales', 'mesa', 'estado', 'notas']
                        ] = [edit_name, edit_phone, new_datetime, edit_size, edit_table, edit_status, edit_notes]
                        
                        if edit_table is not None:
                            st.session_state.tables.loc[
                                st.session_state.tables['numero'] == edit_table, 'estado'
                            ] = "Reservada"
                        
                        st.success(f"Reserva ID {st.session_state.edit_reservation_id} actualizada con éxito")
                        del st.session_state.edit_reservation_id
                        st.rerun()
                
                if st.button("Cancelar Edición", key="cancel_edit"):
                    del st.session_state.edit_reservation_id
                    st.rerun()
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
        
        new_table = st.selectbox(
            "Mesa (opcional)",
            options=[None] + st.session_state.tables[
                st.session_state.tables['estado'] == "Libre"
            ]['numero'].tolist()
        )
        new_notes = st.text_area("Notas adicionales")
        
        if st.button("Crear Reserva"):
            if not new_name or not new_phone:
                st.error("Nombre y teléfono son obligatorios")
            else:
                new_id = st.session_state.reservations['id'].max() + 1 if not st.session_state.reservations.empty else 1
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
                
                st.session_state.reservations = pd.concat(
                    [st.session_state.reservations, new_reservation],
                    ignore_index=True
                )
                
                if new_table is not None:
                    st.session_state.tables.loc[
                        st.session_state.tables['numero'] == new_table, 'estado'
                    ] = "Reservada"
                
                st.success(f"Reserva creada con éxito (ID: {new_id})")
    
    with tab3:
        search_query = st.text_input("Buscar por nombre o teléfono")
        
        if search_query:
            search_results = st.session_state.reservations[
                st.session_state.reservations['nombre'].str.contains(search_query, case=False, na=False) |
                st.session_state.reservations['telefono'].str.contains(search_query, case=False, na=False)
            ]
            
            if not search_results.empty:
                st.dataframe(
                    search_results[['id', 'nombre', 'fecha', 'comensales', 'mesa', 'estado', 'telefono']],
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No se encontraron resultados.")

def manage_tables():
    st.markdown("<div class='title'>Gestión de Mesas</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Ver Mesas", "Agregar Mesa"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='subtitle'>Mapa de Mesas</div>", unsafe_allow_html=True)
            
            tables_df = st.session_state.tables.copy()
            color_map = {"Libre": "green", "Ocupada": "red", "Reservada": "orange"}
            tables_df['color'] = tables_df['estado'].map(color_map)
            
            tables_per_row = 5
            tables_df['x'] = tables_df.index % tables_per_row
            tables_df['y'] = tables_df.index // tables_per_row
            
            fig = go.Figure()
            for _, table in tables_df.iterrows():
                fig.add_trace(go.Scatter(
                    x=[table['x']],
                    y=[table['y']],
                    mode='markers+text',
                    marker=dict(
                        size=table['capacidad'] * 5,
                        color=table['color'],
                        line=dict(width=2, color='white')
                    ),
                    text=[str(table['numero'])],
                    textposition="middle center",
                    hoverinfo="text",
                    hovertext=f"Mesa {table['numero']}<br>Capacidad: {table['capacidad']}<br>Estado: {table['estado']}<br>Ubicación: {table['ubicacion']}"
                ))
            
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
            
            selected_table = st.selectbox(
                "Seleccionar Mesa",
                options=tables_df['numero'].tolist()
            )
            
            if selected_table:
                table_data = tables_df[tables_df['numero'] == selected_table].iloc[0]
                
                st.markdown(f"""
                <div style="padding: 10px; border-radius: 5px; background-color: #f8f9fa;">
                    <h3>Mesa {selected_table}</h3>
                    <p><strong>Capacidad:</strong> {table_data['capacidad']} personas</p>
                    <p><strong>Ubicación:</strong> {table_data['ubicacion']}</p>
                    <p><strong>Estado:</strong> <span style="color: {color_map[table_data['estado']]};">{table_data['estado']}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                table_reservations = st.session_state.reservations[
                    (st.session_state.reservations['mesa'] == selected_table) &
                    (st.session_state.reservations['fecha'].dt.date == selected_date)
                ]
                
                if not table_reservations.empty:
                    st.markdown("<p><strong>Reservas para hoy:</strong></p>", unsafe_allow_html=True)
                    for _, res in table_reservations.iterrows():
                        st.markdown(f"""
                        <div style="margin-top: 10px; padding: 5px 10px; border-left: 3px solid {color_map[res['estado']]};">
                            <div><strong>{res['nombre']}</strong> - {res['comensales']} personas</div>
                            <div>{res['fecha'].strftime('%H:%M')} | {res['estado']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("<p>No hay reservas para esta mesa hoy.</p>", unsafe_allow_html=True)
                
                new_status = st.selectbox(
                    "Cambiar estado",
                    options=["Libre", "Ocupada", "Reservada"],
                    index=["Libre", "Ocupada", "Reservada"].index(table_data['estado'])
                )
                
                if st.button("Actualizar Estado"):
                    st.session_state.tables.loc[
                        st.session_state.tables['numero'] == selected_table, 'estado'
                    ] = new_status
                    st.success(f"Estado de mesa {selected_table} actualizado a {new_status}")
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Agregar Nueva Mesa</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_table_number = st.number_input("Número de Mesa", min_value=1, value=int(st.session_state.tables['numero'].max() + 1) if not st.session_state.tables.empty else 1, step=1)
            new_capacity = st.number_input("Capacidad", min_value=1, max_value=20, value=4)
        
        with col2:
            new_location = st.selectbox("Ubicación", ["Interior", "Exterior", "Terraza"])
            new_status = st.selectbox("Estado Inicial", ["Libre", "Ocupada", "Reservada"], index=0)
        
        if st.button("Agregar Mesa"):
            # Verificar si el número de mesa ya existe
            if new_table_number in st.session_state.tables['numero'].values:
                st.error(f"La mesa número {new_table_number} ya existe. Por favor, elija otro número.")
            else:
                new_table = pd.DataFrame([{
                    "numero": new_table_number,
                    "capacidad": new_capacity,
                    "ubicacion": new_location,
                    "estado": new_status
                }])
                
                st.session_state.tables = pd.concat(
                    [st.session_state.tables, new_table],
                    ignore_index=True
                )
                st.success(f"Mesa {new_table_number} agregada con éxito")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_analysis():
    st.markdown("<div class='title'>Análisis de Datos</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Ocupación Semanal</div>", unsafe_allow_html=True)
        
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
        
        week_start = datetime.combine(start_of_week, datetime.min.time())
        week_end = datetime.combine(week_dates[-1], datetime.max.time())
        
        week_reservations = st.session_state.reservations[
            (st.session_state.reservations['fecha'] >= week_start) &
            (st.session_state.reservations['fecha'] <= week_end)
        ].copy()
        
        week_reservations['dia'] = week_reservations['fecha'].dt.date
        daily_customers = week_reservations.groupby('dia')['comensales'].sum().reindex(week_dates, fill_value=0)
        
        fig = px.bar(
            x=[d.strftime("%a %d/%m") for d in daily_customers.index],
            y=daily_customers.values,
            labels={'x': 'Día', 'y': 'Comensales'},
            color_discrete_sequence=['#3498db']
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Distribución de Comensales</div>", unsafe_allow_html=True)
        
        size_distribution = st.session_state.reservations.groupby('comensales').size()
        
        fig = px.pie(
            names=size_distribution.index,
            values=size_distribution.values,
            color_discrete_sequence=px.colors.sequential.Blues
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Mapa de Calor de Ocupación</div>", unsafe_allow_html=True)
    
    all_reservations = st.session_state.reservations.copy()
    all_reservations['dia_semana'] = all_reservations['fecha'].dt.day_name()
    all_reservations['hora'] = all_reservations['fecha'].dt.hour
    
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
    
    heatmap_data = all_reservations.pivot_table(
        index='hora',
        columns='dia_semana',
        values='comensales',
        aggfunc='sum',
        fill_value=0
    ).reindex(columns=dias)
    
    service_hours = list(range(12, 16)) + list(range(19, 23))
    heatmap_data = heatmap_data.loc[heatmap_data.index.isin(service_hours)]
    
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
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Métricas de Rendimiento</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        completed = len(st.session_state.reservations[st.session_state.reservations['estado'] == "Completada"])
        cancelled = len(st.session_state.reservations[st.session_state.reservations['estado'] == "Cancelada"])
        total = len(st.session_state.reservations)
        
        conversion_rate = completed / total * 100 if total > 0 else 0
        cancellation_rate = cancelled / total * 100 if total > 0 else 0
        
        st.metric(
            "Tasa de Conversión",
            f"{conversion_rate:.1f}%",
            delta=f"-{cancellation_rate:.1f}%" if cancellation_rate > 0 else None,
            delta_color="inverse"
        )
    
    with col2:
        avg_party_size = st.session_state.reservations['comensales'].mean()
        st.metric("Promedio Comensales", f"{avg_party_size:.1f}")
    
    with col3:
        table_capacity = st.session_state.tables['capacidad'].sum()
        total_customers = st.session_state.reservations[
            st.session_state.reservations['estado'].isin(["Completada", "Confirmada"])
        ]['comensales'].sum()
        
        rotation_estimate = total_customers / table_capacity if table_capacity > 0 else 0
        st.metric("Índice de Rotación", f"{rotation_estimate:.2f}x")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Recomendaciones</div>", unsafe_allow_html=True)
    
    peak_hours = all_reservations.groupby('hora')['comensales'].sum().sort_values(ascending=False).head(3)
    busy_days = all_reservations.groupby('dia_semana')['comensales'].sum().sort_values(ascending=False).head(2)
    avg_group = all_reservations['comensales'].mean()
    
    st.markdown(f"""
    <div style="background-color: #f0f7ff; padding: 15px; border-radius: 5px; margin-top: 10px;">
        <h4>Análisis de Operaciones</h4>
        <ul>
            <li>Las horas pico de servicio son: {', '.join([f'{h}:00' for h in peak_hours.index])}</li>
            <li>Los días más ocupados son: {', '.join(busy_days.index)}</li>
            <li>El tamaño promedio de grupo es de {avg_group:.1f} personas</li>
        </ul>
        <h4>Recomendaciones:</h4>
        <ul>
            <li>Considere aumentar el personal durante {', '.join([f'{h}:00' for h in peak_hours.index])} para mejorar el servicio.</li>
            <li>Reorganice las mesas para optimizar el espacio según el tamaño promedio de grupo.</li>
            <li>Ofrezca promociones en días menos concurridos para equilibrar la ocupación semanal.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if page == "Panel Principal":
    show_dashboard()
elif page == "Reservas":
    manage_reservations()
elif page == "Gestión de Mesas":
    manage_tables()
elif page == "Análisis":
    show_analysis()
