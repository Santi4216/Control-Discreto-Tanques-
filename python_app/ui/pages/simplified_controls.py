"""
Manual Control Page - Direct pump and servo control.
Simple and intuitive manual operation interface.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QSlider, QSpinBox, QGroupBox, QFormLayout, QProgressBar, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from core.serial_worker import SerialWorker
from ui.components.metric_card import MetricCard


class SimplifiedControlsPage(QWidget):
    """Manual control panel for pump and servos."""
    
    def __init__(self, serial_worker: SerialWorker, parent=None):
        super().__init__(parent)
        self.serial_worker = serial_worker
        
        # Create scroll area for all content
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #0a0e1a; }")
        
        # Content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)
        
        # Title with icon
        title_layout = QHBoxLayout()
        title = QLabel("🎛 Manual Control")
        title.setObjectName("heading1")
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        subtitle = QLabel("Pre-startup hardware verification")
        subtitle.setObjectName("caption")
        layout.addWidget(subtitle)
        
        # ═══════════════════════════════════════════════════════════════
        # TELEMETRY SECTION - Flow Sensor
        # ═══════════════════════════════════════════════════════════════
        telemetry_group = QGroupBox("📊 Telemetry")
        telemetry_layout = QHBoxLayout()
        telemetry_layout.setContentsMargins(14, 12, 14, 12)
        telemetry_layout.setSpacing(12)
        
        self.flow_metric = MetricCard("Flow Rate", "L/min", "💧")
        telemetry_layout.addWidget(self.flow_metric)
        telemetry_layout.addStretch()
        
        telemetry_group.setLayout(telemetry_layout)
        telemetry_group.setMinimumHeight(140)
        layout.addWidget(telemetry_group)
        
        # Connect flow signal
        self.serial_worker.flow_received.connect(self._on_flow_received)
        
        # ═══════════════════════════════════════════════════════════════
        # PUMP CONTROL SECTION
        # ═══════════════════════════════════════════════════════════════
        pump_group = QGroupBox("💨 Pump Control")
        pump_group.setObjectName("controlPanel")
        pump_layout = QVBoxLayout()
        pump_layout.setSpacing(11)
        pump_layout.setContentsMargins(14, 12, 14, 12)
        
        # PWM Value and Status
        pump_header = QHBoxLayout()
        pump_label = QLabel("Power (PWM):")
        pump_label.setStyleSheet("font-weight: bold; color: #00e5ff; font-size: 12px;")
        pump_header.addWidget(pump_label)
        pump_header.addStretch()
        self.pump_status = QLabel("OFF")
        self.pump_status.setObjectName("statusChip")
        self.pump_status.setStyleSheet("background-color: rgba(255, 0, 110, 0.15); color: #ff006e;")
        pump_header.addWidget(self.pump_status)
        pump_layout.addLayout(pump_header)
        
        # Slider with value display
        slider_row = QHBoxLayout()
        self.pump_slider = QSlider(Qt.Orientation.Horizontal)
        self.pump_slider.setRange(0, 255)
        self.pump_slider.setValue(0)
        self.pump_slider.setTickInterval(51)
        self.pump_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.pump_slider.setMinimumHeight(36)
        slider_row.addWidget(self.pump_slider, stretch=1)
        
        self.pump_spin = QSpinBox()
        self.pump_spin.setRange(0, 255)
        self.pump_spin.setValue(0)
        self.pump_spin.setFixedWidth(100)
        self.pump_spin.setMinimumHeight(36)
        self.pump_spin.setStyleSheet("font-size: 13px; font-weight: bold;")
        slider_row.addWidget(self.pump_spin)
        pump_layout.addLayout(slider_row)
        
        # Progress bar and percentage
        self.pump_pct_label = QLabel("0% (0/255)")
        self.pump_pct_label.setObjectName("caption")
        self.pump_pct_label.setStyleSheet("font-size: 12px;")
        pump_layout.addWidget(self.pump_pct_label)
        
        self.pump_progress = QProgressBar()
        self.pump_progress.setValue(0)
        self.pump_progress.setMaximum(255)
        self.pump_progress.setMinimumHeight(10)
        pump_layout.addWidget(self.pump_progress)
        
        # Send button
        send_pump_btn = QPushButton("⚡ Send Command")
        send_pump_btn.setMinimumHeight(32)
        send_pump_btn.clicked.connect(self.send_pump_pwm)
        pump_layout.addWidget(send_pump_btn)
        
        self.pump_slider.valueChanged.connect(self._on_pump_slider_changed)
        self.pump_spin.valueChanged.connect(self._on_pump_spin_changed)
        
        pump_group.setLayout(pump_layout)
        layout.addWidget(pump_group)
        
        # ═══════════════════════════════════════════════════════════════
        # SERVO CONTROLS - Two Column Layout
        # ═══════════════════════════════════════════════════════════════
        
        # Create a horizontal layout for both servos
        servos_container = QHBoxLayout()
        servos_container.setSpacing(14)
        servos_container.setContentsMargins(0, 0, 0, 0)
        
        # ─────────────────────────────────────────────────────────────
        # SERVO 1
        # ─────────────────────────────────────────────────────────────
        servo1_group = QGroupBox("🔷 Servo 1 (Valve 1)")
        servo1_group.setObjectName("controlPanel")
        servo1_layout = QVBoxLayout()
        servo1_layout.setSpacing(11)
        servo1_layout.setContentsMargins(14, 12, 14, 12)
        
        servo1_header = QHBoxLayout()
        servo1_label = QLabel("Angle:")
        servo1_label.setStyleSheet("font-weight: bold; color: #00e5ff; font-size: 12px;")
        servo1_header.addWidget(servo1_label)
        servo1_header.addStretch()
        self.servo1_status = QLabel("90°")
        self.servo1_status.setStyleSheet("color: #00ff88; font-weight: bold;")
        servo1_header.addWidget(self.servo1_status)
        servo1_layout.addLayout(servo1_header)
        
        servo1_slider_row = QHBoxLayout()
        self.servo1_slider = QSlider(Qt.Orientation.Horizontal)
        self.servo1_slider.setRange(0, 180)
        self.servo1_slider.setValue(90)
        self.servo1_slider.setTickInterval(30)
        self.servo1_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.servo1_slider.setMinimumHeight(36)
        servo1_slider_row.addWidget(self.servo1_slider, stretch=1)
        
        self.servo1_spin = QSpinBox()
        self.servo1_spin.setRange(0, 180)
        self.servo1_spin.setValue(90)
        self.servo1_spin.setFixedWidth(100)
        self.servo1_spin.setMinimumHeight(36)
        self.servo1_spin.setStyleSheet("font-size: 13px; font-weight: bold;")
        servo1_slider_row.addWidget(self.servo1_spin)
        servo1_layout.addLayout(servo1_slider_row)
        
        # Servo position indicator
        self.servo1_label = QLabel("CLOSED")
        self.servo1_label.setObjectName("caption")
        self.servo1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        servo1_layout.addWidget(self.servo1_label)
        
        send_servo1_btn = QPushButton("✓ Send")
        send_servo1_btn.setMinimumHeight(32)
        send_servo1_btn.clicked.connect(self.send_servo1_angle)
        servo1_layout.addWidget(send_servo1_btn)
        
        self.servo1_slider.valueChanged.connect(self._on_servo1_slider_changed)
        self.servo1_spin.valueChanged.connect(self._on_servo1_spin_changed)
        
        servo1_group.setLayout(servo1_layout)
        servos_container.addWidget(servo1_group)
        
        # ─────────────────────────────────────────────────────────────
        # SERVO 2
        # ─────────────────────────────────────────────────────────────
        servo2_group = QGroupBox("🔶 Servo 2 (Valve 2)")
        servo2_group.setObjectName("controlPanel")
        servo2_layout = QVBoxLayout()
        servo2_layout.setSpacing(11)
        servo2_layout.setContentsMargins(14, 12, 14, 12)
        
        servo2_header = QHBoxLayout()
        servo2_label = QLabel("Angle:")
        servo2_label.setStyleSheet("font-weight: bold; color: #00e5ff; font-size: 12px;")
        servo2_header.addWidget(servo2_label)
        servo2_header.addStretch()
        self.servo2_status = QLabel("90°")
        self.servo2_status.setStyleSheet("color: #00ff88; font-weight: bold;")
        servo2_header.addWidget(self.servo2_status)
        servo2_layout.addLayout(servo2_header)
        
        servo2_slider_row = QHBoxLayout()
        self.servo2_slider = QSlider(Qt.Orientation.Horizontal)
        self.servo2_slider.setRange(0, 180)
        self.servo2_slider.setValue(90)
        self.servo2_slider.setTickInterval(30)
        self.servo2_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.servo2_slider.setMinimumHeight(36)
        servo2_slider_row.addWidget(self.servo2_slider, stretch=1)
        
        self.servo2_spin = QSpinBox()
        self.servo2_spin.setRange(0, 180)
        self.servo2_spin.setValue(90)
        self.servo2_spin.setFixedWidth(100)
        self.servo2_spin.setMinimumHeight(36)
        self.servo2_spin.setStyleSheet("font-size: 13px; font-weight: bold;")
        servo2_slider_row.addWidget(self.servo2_spin)
        servo2_layout.addLayout(servo2_slider_row)
        
        # Servo position indicator
        self.servo2_label = QLabel("CLOSED")
        self.servo2_label.setObjectName("caption")
        self.servo2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        servo2_layout.addWidget(self.servo2_label)
        
        send_servo2_btn = QPushButton("✓ Send")
        send_servo2_btn.setMinimumHeight(32)
        send_servo2_btn.clicked.connect(self.send_servo2_angle)
        servo2_layout.addWidget(send_servo2_btn)
        
        self.servo2_slider.valueChanged.connect(self._on_servo2_slider_changed)
        self.servo2_spin.valueChanged.connect(self._on_servo2_spin_changed)
        
        servo2_group.setLayout(servo2_layout)
        servos_container.addWidget(servo2_group)
        
        # Add servos container to main layout
        layout.addLayout(servos_container)
        
        # ═══════════════════════════════════════════════════════════════
        # EMERGENCY STOP SECTION
        # ═══════════════════════════════════════════════════════════════
        layout.addSpacing(10)
        
        stop_info = QLabel("⚠ Press below to immediately halt all systems")
        stop_info.setObjectName("caption")
        stop_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stop_info)
        
        stop_btn = QPushButton("⏹ EMERGENCY STOP")
        stop_btn.setObjectName("dangerButton")
        stop_btn.clicked.connect(self.stop_pump)
        stop_btn.setMinimumHeight(60)
        stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff006e;
                color: white;
                border: 2px solid #ff0055;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff1a75;
                border: 2px solid #ff3366;
            }
            QPushButton:pressed {
                background-color: #cc0055;
            }
        """)
        layout.addWidget(stop_btn)
        
        layout.addStretch()
        
        # Add content to scroll area and scroll area to main
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    # ═════════════════════════════════════════════════════════════════════
    # PUMP METHODS
    # ═════════════════════════════════════════════════════════════════════
    
    def _on_pump_slider_changed(self, value):
        """Slider changed → update spinbox and label."""
        if self.pump_spin.value() != value:
            self.pump_spin.blockSignals(True)
            self.pump_spin.setValue(value)
            self.pump_spin.blockSignals(False)
        self._update_pump_label()
    
    def _on_pump_spin_changed(self, value):
        """Spinbox changed → update slider and label."""
        if self.pump_slider.value() != value:
            self.pump_slider.blockSignals(True)
            self.pump_slider.setValue(value)
            self.pump_slider.blockSignals(False)
        self._update_pump_label()
    
    def _update_pump_label(self):
        """Update pump percentage label and progress bar."""
        value = self.pump_slider.value()
        pct = (value * 100) // 255
        self.pump_pct_label.setText(f"{pct}% ({value}/255)")
        self.pump_progress.setValue(value)
        
        # Update status indicator
        if value == 0:
            self.pump_status.setText("OFF")
            self.pump_status.setStyleSheet("background-color: rgba(255, 0, 110, 0.15); color: #ff006e; padding: 4px 12px; border-radius: 4px;")
        elif value < 85:
            self.pump_status.setText("LOW")
            self.pump_status.setStyleSheet("background-color: rgba(251, 86, 7, 0.15); color: #fb5607; padding: 4px 12px; border-radius: 4px;")
        elif value < 170:
            self.pump_status.setText("MEDIUM")
            self.pump_status.setStyleSheet("background-color: rgba(0, 229, 255, 0.15); color: #00e5ff; padding: 4px 12px; border-radius: 4px;")
        else:
            self.pump_status.setText("HIGH")
            self.pump_status.setStyleSheet("background-color: rgba(0, 255, 136, 0.15); color: #00ff88; padding: 4px 12px; border-radius: 4px;")
    
    def send_pump_pwm(self):
        """Send pump PWM command to Arduino."""
        value = self.pump_slider.value()
        cmd = f"PUMP,{value}\n"
        self.serial_worker.send_command(cmd)
    
    # ═════════════════════════════════════════════════════════════════════
    # SERVO 1 METHODS
    # ═════════════════════════════════════════════════════════════════════
    
    def _on_servo1_slider_changed(self, value):
        """Slider changed → update spinbox and label."""
        if self.servo1_spin.value() != value:
            self.servo1_spin.blockSignals(True)
            self.servo1_spin.setValue(value)
            self.servo1_spin.blockSignals(False)
        self._update_servo1_label()
    
    def _on_servo1_spin_changed(self, value):
        """Spinbox changed → update slider and label."""
        if self.servo1_slider.value() != value:
            self.servo1_slider.blockSignals(True)
            self.servo1_slider.setValue(value)
            self.servo1_slider.blockSignals(False)
        self._update_servo1_label()
    
    def _update_servo1_label(self):
        """Update servo 1 angle label."""
        angle = self.servo1_slider.value()
        self.servo1_status.setText(f"{angle}°")
        
        # Show if open/closed (180° = closed, 0° = open)
        if angle > 100:
            self.servo1_label.setText("🔴 CLOSED")
            self.servo1_label.setStyleSheet("color: #ff006e; font-weight: bold;")
        elif angle < 80:
            self.servo1_label.setText("🟢 OPEN")
            self.servo1_label.setStyleSheet("color: #00ff88; font-weight: bold;")
        else:
            self.servo1_label.setText("🟡 TRANSITION")
            self.servo1_label.setStyleSheet("color: #fb5607; font-weight: bold;")
    
    def send_servo1_angle(self):
        """Send servo 1 angle command to Arduino."""
        angle = self.servo1_slider.value()
        cmd = f"SERVO1,{angle}\n"
        self.serial_worker.send_command(cmd)
    
    # ═════════════════════════════════════════════════════════════════════
    # SERVO 2 METHODS
    # ═════════════════════════════════════════════════════════════════════
    
    def _on_servo2_slider_changed(self, value):
        """Slider changed → update spinbox and label."""
        if self.servo2_spin.value() != value:
            self.servo2_spin.blockSignals(True)
            self.servo2_spin.setValue(value)
            self.servo2_spin.blockSignals(False)
        self._update_servo2_label()
    
    def _on_servo2_spin_changed(self, value):
        """Spinbox changed → update slider and label."""
        if self.servo2_slider.value() != value:
            self.servo2_slider.blockSignals(True)
            self.servo2_slider.setValue(value)
            self.servo2_slider.blockSignals(False)
        self._update_servo2_label()
    
    def _update_servo2_label(self):
        """Update servo 2 angle label."""
        angle = self.servo2_slider.value()
        self.servo2_status.setText(f"{angle}°")
        
        # Show if open/closed (180° = closed, 0° = open)
        if angle > 100:
            self.servo2_label.setText("🔴 CLOSED")
            self.servo2_label.setStyleSheet("color: #ff006e; font-weight: bold;")
        elif angle < 80:
            self.servo2_label.setText("🟢 OPEN")
            self.servo2_label.setStyleSheet("color: #00ff88; font-weight: bold;")
        else:
            self.servo2_label.setText("🟡 TRANSITION")
            self.servo2_label.setStyleSheet("color: #fb5607; font-weight: bold;")
    
    def send_servo2_angle(self):
        """Send servo 2 angle command to Arduino."""
        angle = self.servo2_slider.value()
        cmd = f"SERVO2,{angle}\n"
        self.serial_worker.send_command(cmd)
    
    # ═════════════════════════════════════════════════════════════════════
    # SAFETY METHODS
    # ═════════════════════════════════════════════════════════════════════
    
    def stop_pump(self):
        """Stop pump immediately."""
        cmd = "STOP\n"
        self.serial_worker.send_command(cmd)
        # Reset UI
        self.pump_slider.blockSignals(True)
        self.pump_spin.blockSignals(True)
        self.pump_slider.setValue(0)
        self.pump_spin.setValue(0)
        self.pump_slider.blockSignals(False)
        self.pump_spin.blockSignals(False)
        self._update_pump_label()
    
    # ═════════════════════════════════════════════════════════════════════
    # FLOW SENSOR
    # ═════════════════════════════════════════════════════════════════════
    
    def _on_flow_received(self, flow_value: float):
        """Update flow rate display when new measurement arrives."""
        self.flow_metric.set_value(flow_value)
