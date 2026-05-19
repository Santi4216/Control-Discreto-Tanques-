"""
Discrete State Monitor - Visualización gráfica del control por tiempos.
Muestra el progreso de llenado de tanques, PWM, y transiciones de estado.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QGroupBox, QProgressBar, QPushButton)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor
import pyqtgraph as pg
from datetime import datetime
from collections import deque

from core.serial_worker import SerialWorker


class DiscreteMonitorPage(QWidget):
    """Página de monitoreo de control discreto con gráficas."""
    
    # Señales para recibir datos
    state_updated = pyqtSignal(dict)
    
    def __init__(self, serial_worker: SerialWorker, parent=None):
        super().__init__(parent)
        self.serial_worker = serial_worker
        
        # Buffer para gráficas
        self.max_points = 300  # ~30 segundos a 10Hz
        self.time_data = deque(maxlen=self.max_points)
        self.tank1_progress = deque(maxlen=self.max_points)
        self.tank2_progress = deque(maxlen=self.max_points)
        self.pwm_data = deque(maxlen=self.max_points)
        self.current_tank = 0
        self.sequence_active = False
        self.start_time = None
        self.point_count = 0
        
        # Estados discretos
        self.state = {
            'tank': 0,
            'progress': 0,
            'pwm': 0,
            'status': 'IDLE'
        }
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)
        
        # ═══════════════════════════════════════════════════════════════
        # ENCABEZADO
        # ═══════════════════════════════════════════════════════════════
        title = QLabel("⏱ Discrete State Monitor – Time-Based Control")
        title.setObjectName("heading1")
        layout.addWidget(title)
        
        # ═══════════════════════════════════════════════════════════════
        # ESTADO ACTUAL
        # ═══════════════════════════════════════════════════════════════
        state_group = QGroupBox("Current State")
        state_layout = QHBoxLayout()
        
        # Status
        self.status_label = QLabel("Status: IDLE")
        self.status_label.setFont(QFont("Courier", 12, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: #888;")
        state_layout.addWidget(self.status_label)
        
        # Tank actual
        self.tank_label = QLabel("Tank: —")
        self.tank_label.setFont(QFont("Courier", 12, QFont.Weight.Bold))
        state_layout.addWidget(self.tank_label)
        
        # Progress
        self.progress_label = QLabel("Progress: 0%")
        self.progress_label.setFont(QFont("Courier", 12, QFont.Weight.Bold))
        state_layout.addWidget(self.progress_label)
        
        # PWM
        self.pwm_label = QLabel("Pump PWM: 0/255")
        self.pwm_label.setFont(QFont("Courier", 12, QFont.Weight.Bold))
        state_layout.addWidget(self.pwm_label)
        
        state_layout.addStretch()
        state_group.setLayout(state_layout)
        layout.addWidget(state_group)
        
        # ═══════════════════════════════════════════════════════════════
        # GRÁFICA 1: PROGRESO DE LLENADO
        # ═══════════════════════════════════════════════════════════════
        progress_group = QGroupBox("Fill Progress (%)")
        progress_layout = QVBoxLayout()
        
        self.plot_progress = pg.PlotWidget()
        self.plot_progress.setLabel('left', 'Progress', units='%')
        self.plot_progress.setLabel('bottom', 'Time', units='s')
        self.plot_progress.setYRange(0, 100)
        self.plot_progress.enableAutoRange(x=True, y=False)  # Fijo en Y, auto en X
        self.plot_progress.setBackground((20, 20, 20))
        self.plot_progress.showGrid(True, True, alpha=0.3)
        self.plot_progress.setMinimumHeight(200)
        
        # Líneas para Tank 1 y Tank 2
        self.curve_tank1 = self.plot_progress.plot(
            pen=pg.mkPen(color=(0, 200, 100), width=2),
            name='Tank 1'
        )
        self.curve_tank2 = self.plot_progress.plot(
            pen=pg.mkPen(color=(100, 150, 255), width=2),
            name='Tank 2'
        )
        
        # Leyenda
        self.plot_progress.addLegend(offset=(10, 10))
        
        progress_layout.addWidget(self.plot_progress)
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # ═══════════════════════════════════════════════════════════════
        # GRÁFICA 2: PWM DE BOMBA
        # ═══════════════════════════════════════════════════════════════
        pwm_group = QGroupBox("Pump PWM Over Time")
        pwm_layout = QVBoxLayout()
        
        self.plot_pwm = pg.PlotWidget()
        self.plot_pwm.setLabel('left', 'PWM', units='%')
        self.plot_pwm.setLabel('bottom', 'Time', units='s')
        self.plot_pwm.setYRange(0, 255)
        self.plot_pwm.enableAutoRange(x=True, y=False)  # Fijo en Y, auto en X
        self.plot_pwm.setBackground((20, 20, 20))
        self.plot_pwm.showGrid(True, True, alpha=0.3)
        self.plot_pwm.setMinimumHeight(180)
        
        self.curve_pwm = self.plot_pwm.plot(
            pen=pg.mkPen(color=(255, 100, 100), width=2),
            name='Pump PWM'
        )
        self.plot_pwm.addLegend(offset=(10, 10))
        
        pwm_layout.addWidget(self.plot_pwm)
        pwm_group.setLayout(pwm_layout)
        layout.addWidget(pwm_group)
        
        # ═══════════════════════════════════════════════════════════════
        # BARRAS DE PROGRESO
        # ═══════════════════════════════════════════════════════════════
        bars_group = QGroupBox("Individual Tank Progress")
        bars_layout = QVBoxLayout()
        
        # Tank 1 progress bar
        tank1_label = QLabel("Tank 1")
        tank1_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        bars_layout.addWidget(tank1_label)
        self.progress_tank1 = QProgressBar()
        self.progress_tank1.setRange(0, 100)
        self.progress_tank1.setValue(0)
        self.progress_tank1.setStyleSheet(
            "QProgressBar { border: 2px solid #444; border-radius: 3px; }"
            "QProgressBar::chunk { background-color: #00C864; }"
        )
        bars_layout.addWidget(self.progress_tank1)
        
        # Tank 2 progress bar
        tank2_label = QLabel("Tank 2")
        tank2_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        bars_layout.addWidget(tank2_label)
        self.progress_tank2 = QProgressBar()
        self.progress_tank2.setRange(0, 100)
        self.progress_tank2.setValue(0)
        self.progress_tank2.setStyleSheet(
            "QProgressBar { border: 2px solid #444; border-radius: 3px; }"
            "QProgressBar::chunk { background-color: #6496FF; }"
        )
        bars_layout.addWidget(self.progress_tank2)
        
        bars_group.setLayout(bars_layout)
        layout.addWidget(bars_group)
        
        # ═══════════════════════════════════════════════════════════════
        # BOTONES DE CONTROL
        # ═══════════════════════════════════════════════════════════════
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("🗑 Clear Data")
        clear_btn.clicked.connect(self.clear_data)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        # Timer para actualizar gráficas
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_graphs)
        self.update_timer.start(50)  # Actualizar cada 50ms para mejor fluidez
        
        # Conectar señal de estado
        self.state_updated.connect(self.on_state_updated)
    
    def on_state_updated(self, state_dict):
        """Recibir actualización de estado del serial worker."""
        self.state = state_dict
        self.sequence_active = state_dict.get('status') != 'IDLE'
        
        if self.sequence_active and self.start_time is None:
            self.start_time = datetime.now()
        elif not self.sequence_active:
            self.start_time = None
        
        # Agregar datos
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.time_data.append(elapsed)
            
            tank = state_dict.get('tank', 0)
            progress = state_dict.get('progress', 0)
            pwm = state_dict.get('pwm', 0)
            
            if tank == 1:
                self.tank1_progress.append(progress)
                self.tank2_progress.append(0)  # Tank 2 en espera
                self.progress_tank1.setValue(progress)
            elif tank == 2:
                self.tank1_progress.append(100)  # Tank 1 completado
                self.tank2_progress.append(progress)
                self.progress_tank2.setValue(progress)
            
            self.pwm_data.append(pwm)
        
        # Actualizar etiquetas
        status = state_dict.get('status', 'IDLE')
        self.status_label.setText(f"Status: {status}")
        self._update_status_color(status)
        
        tank = state_dict.get('tank', 0)
        tank_text = f"Tank {tank}" if tank > 0 else "—"
        self.tank_label.setText(f"Tank: {tank_text}")
        
        progress = state_dict.get('progress', 0)
        self.progress_label.setText(f"Progress: {progress}%")
        
        pwm = state_dict.get('pwm', 0)
        pwm_pct = int((pwm * 100) / 255)
        self.pwm_label.setText(f"Pump PWM: {pwm}/255 ({pwm_pct}%)")
    
    def _update_status_color(self, status):
        """Cambiar color según estado."""
        colors = {
            'IDLE': '#888',
            'FILL': '#00C864',
            'TRANSITION': '#FFB800',
            'COMPLETE': '#00C864',
            'STOPPED': '#FF3B30'
        }
        color = colors.get(status, '#888')
        self.status_label.setStyleSheet(f"color: {color};")
    
    def update_graphs(self):
        """Actualizar gráficas."""
        if len(self.time_data) == 0:
            return
        
        time_array = list(self.time_data)
        
        # Gráfica de progreso - Mantener último valor si no hay cambios
        tank1_data = list(self.tank1_progress)
        tank2_data = list(self.tank2_progress)
        
        # Asegurar que tenemos datos para cada punto de tiempo
        if len(tank1_data) < len(time_array):
            # Rellenar con el último valor conocido
            last_t1 = tank1_data[-1] if tank1_data else 0
            last_t2 = tank2_data[-1] if tank2_data else 0
            tank1_data.extend([last_t1] * (len(time_array) - len(tank1_data)))
            tank2_data.extend([last_t2] * (len(time_array) - len(tank2_data)))
        
        self.curve_tank1.setData(time_array, tank1_data)
        self.curve_tank2.setData(time_array, tank2_data)
        
        # Gráfica de PWM
        pwm_data = list(self.pwm_data)
        if len(pwm_data) < len(time_array):
            last_pwm = pwm_data[-1] if pwm_data else 0
            pwm_data.extend([last_pwm] * (len(time_array) - len(pwm_data)))
        
        pwm_pct = [(p * 100) / 255 for p in pwm_data]
        self.curve_pwm.setData(time_array, pwm_pct)
    
    def clear_data(self):
        """Limpiar datos y gráficas."""
        self.time_data.clear()
        self.tank1_progress.clear()
        self.tank2_progress.clear()
        self.pwm_data.clear()
        self.start_time = None
        self.sequence_active = False
        
        # Reset UI
        self.status_label.setText("Status: IDLE")
        self.tank_label.setText("Tank: —")
        self.progress_label.setText("Progress: 0%")
        self.pwm_label.setText("Pump PWM: 0/255")
        self.progress_tank1.setValue(0)
        self.progress_tank2.setValue(0)
        
        # Limpiar gráficas
        self.curve_tank1.setData([], [])
        self.curve_tank2.setData([], [])
        self.curve_pwm.setData([], [])
