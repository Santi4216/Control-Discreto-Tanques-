"""
Timed Sequence Control Page - Configure and run automated tank fill sequences.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QSpinBox, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt
from core.serial_worker import SerialWorker


class TimedSequencePage(QWidget):
    """Configuration and execution of timed fill sequences."""
    
    def __init__(self, serial_worker: SerialWorker, stats_logger=None, parent=None):
        super().__init__(parent)
        self.serial_worker = serial_worker
        self.stats_logger = stats_logger
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("⏱ Timed Fill Sequence")
        title.setObjectName("heading1")
        layout.addWidget(title)
        
        subtitle = QLabel("Automatically fill Tank 1, then Tank 2 with configured timings and servo angles")
        subtitle.setObjectName("caption")
        layout.addWidget(subtitle)
        
        # ═══════════════════════════════════════════════════════════════
        # TANK 1 CONFIG
        # ═══════════════════════════════════════════════════════════════
        tank1_group = QGroupBox("Tank 1")
        tank1_form = QFormLayout()
        
        self.tank1_fill_time = QSpinBox()
        self.tank1_fill_time.setRange(100, 60000)
        self.tank1_fill_time.setValue(5000)
        self.tank1_fill_time.setSuffix(" ms")
        self.tank1_fill_time.setSingleStep(500)
        tank1_form.addRow("Fill Time:", self.tank1_fill_time)
        
        tank1_angles_layout = QHBoxLayout()
        self.tank1_open = QSpinBox()
        self.tank1_open.setRange(0, 180)
        self.tank1_open.setValue(45)
        self.tank1_open.setSuffix("°")
        tank1_angles_layout.addWidget(QLabel("Open:"))
        tank1_angles_layout.addWidget(self.tank1_open)
        
        self.tank1_close = QSpinBox()
        self.tank1_close.setRange(0, 180)
        self.tank1_close.setValue(135)
        self.tank1_close.setSuffix("°")
        tank1_angles_layout.addWidget(QLabel("Close:"))
        tank1_angles_layout.addWidget(self.tank1_close)
        tank1_angles_layout.addStretch()
        tank1_form.addRow("Servo Angles:", tank1_angles_layout)
        
        tank1_group.setLayout(tank1_form)
        layout.addWidget(tank1_group)
        
        # ═══════════════════════════════════════════════════════════════
        # TANK 2 CONFIG
        # ═══════════════════════════════════════════════════════════════
        tank2_group = QGroupBox("Tank 2")
        tank2_form = QFormLayout()
        
        self.tank2_fill_time = QSpinBox()
        self.tank2_fill_time.setRange(100, 60000)
        self.tank2_fill_time.setValue(8000)
        self.tank2_fill_time.setSuffix(" ms")
        self.tank2_fill_time.setSingleStep(500)
        tank2_form.addRow("Fill Time:", self.tank2_fill_time)
        
        tank2_angles_layout = QHBoxLayout()
        self.tank2_open = QSpinBox()
        self.tank2_open.setRange(0, 180)
        self.tank2_open.setValue(45)
        self.tank2_open.setSuffix("°")
        tank2_angles_layout.addWidget(QLabel("Open:"))
        tank2_angles_layout.addWidget(self.tank2_open)
        
        self.tank2_close = QSpinBox()
        self.tank2_close.setRange(0, 180)
        self.tank2_close.setValue(135)
        self.tank2_close.setSuffix("°")
        tank2_angles_layout.addWidget(QLabel("Close:"))
        tank2_angles_layout.addWidget(self.tank2_close)
        tank2_angles_layout.addStretch()
        tank2_form.addRow("Servo Angles:", tank2_angles_layout)
        
        tank2_group.setLayout(tank2_form)
        layout.addWidget(tank2_group)
        
        # ═══════════════════════════════════════════════════════════════
        # PUMP PWM CONFIG
        # ═══════════════════════════════════════════════════════════════
        pump_group = QGroupBox("Pump")
        pump_form = QFormLayout()
        
        self.pump_pwm = QSpinBox()
        self.pump_pwm.setRange(0, 255)
        self.pump_pwm.setValue(200)
        self.pump_pwm.setSuffix("/255")
        pump_form.addRow("PWM:", self.pump_pwm)
        
        pump_group.setLayout(pump_form)
        layout.addWidget(pump_group)
        
        # ═══════════════════════════════════════════════════════════════
        # ACTION BUTTONS
        # ═══════════════════════════════════════════════════════════════
        button_layout = QHBoxLayout()
        
        self.send_config_btn = QPushButton("⚙ Configure")
        self.send_config_btn.clicked.connect(self.send_config)
        button_layout.addWidget(self.send_config_btn)
        
        self.start_btn = QPushButton("▶ Start Sequence")
        self.start_btn.setObjectName("primaryButton")
        self.start_btn.clicked.connect(self.start_sequence)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.clicked.connect(self.stop_sequence)
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def send_config(self):
        """Send configuration to Arduino."""
        tank1_cmd = f"TIMECFG,1,{self.tank1_fill_time.value()},{self.tank1_open.value()},{self.tank1_close.value()}\n"
        tank2_cmd = f"TIMECFG,2,{self.tank2_fill_time.value()},{self.tank2_open.value()},{self.tank2_close.value()}\n"
        
        self.serial_worker.send_command(tank1_cmd)
        self.serial_worker.send_command(tank2_cmd)
    
    def start_sequence(self):
        """Start the timed sequence."""
        self.send_config()
        
        # Iniciar timing de estadísticas
        tank1_ms = self.tank1_fill_time.value()
        tank2_ms = self.tank2_fill_time.value()
        
        # El SerialWorker se encarga de iniciar las estadísticas
        self.serial_worker.start_sequence_timing(tank1_ms, tank2_ms)
        
        pwm = self.pump_pwm.value()
        cmd = f"TIMESEQ,{pwm}\n"
        self.serial_worker.send_command(cmd)
    
    def stop_sequence(self):
        """Stop the sequence."""
        cmd = "TIMESTOP\n"
        self.serial_worker.send_command(cmd)
