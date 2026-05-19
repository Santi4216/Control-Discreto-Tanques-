"""
Serial communication worker running in separate thread.
"""
import serial
import serial.tools.list_ports
from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition
from typing import List, Optional, Dict
import time
import re

from core.protocol import ProtocolParser, DiscreteStateMessage
from core.models import TelemetryData, StatusMessage, MetricsData
from core.command_logger import get_logger
from core.execution_stats import StatsLogger


class SerialWorker(QThread):
    """Non-blocking serial communication thread."""
    
    # Signals
    telemetry_received = pyqtSignal(TelemetryData)
    status_received = pyqtSignal(StatusMessage)
    metrics_received = pyqtSignal(MetricsData)
    discrete_state_received = pyqtSignal(dict)  # Estado discreto {status, tank, progress, pwm}
    flow_received = pyqtSignal(float)  # Caudal en L/min
    connection_changed = pyqtSignal(bool)  # True=connected, False=disconnected
    error_occurred = pyqtSignal(str)
    
    def __init__(self, stats_logger: Optional[StatsLogger] = None, parent=None):
        super().__init__(parent)
        self.serial_port: Optional[serial.Serial] = None
        self.parser = ProtocolParser()
        self.logger = get_logger()  # Initialize command logger
        self.stats_logger = stats_logger  # Use provided stats logger instance
        
        self.port_name = ""
        self.baud_rate = 115200
        self.running = False
        self.connected = False
        
        # Thread-safe command queue
        self.command_queue = []
        self.queue_mutex = QMutex()
        self.queue_condition = QWaitCondition()
        
        # Rate limiting
        self.last_command_time = 0
        self.min_command_interval = 0.05  # 50ms between commands
        
        # Status polling
        self.last_status_request = 0
        self.status_request_interval = 1000  # Request STATUS every 1 second (ms)
        
        # Sequence timing
        self.start_time = None
        self.last_tank2_progress = 0  # Detectar cuando Tank2 llega a 100% (fallback)
    
    def connect(self, port: str, baud_rate: int = 115200):
        """Connect to serial port."""
        self.port_name = port
        self.baud_rate = baud_rate
        
        if not self.isRunning():
            self.running = True
            self.start()
        else:
            self._reconnect()
    
    def disconnect(self):
        """Disconnect from serial port."""
        self.running = False
        self._close_port()
        if self.isRunning():
            self.quit()
            self.wait(2000)  # Wait up to 2 seconds
    
    def send_command(self, command: str):
        """Queue command to send to Arduino.
        
        Args:
            command: Command string (should end with newline)
        """
        self.queue_mutex.lock()
        self.command_queue.append(command)
        self.queue_condition.wakeOne()
        self.queue_mutex.unlock()
    
    def _reconnect(self):
        """Internal reconnect logic."""
        self._close_port()
        self._open_port()
    
    def _open_port(self):
        """Open serial port."""
        try:
            self.serial_port = serial.Serial(
                port=self.port_name,
                baudrate=self.baud_rate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1,  # Non-blocking read with timeout
                write_timeout=0.5
            )
            time.sleep(2)  # Wait for Arduino reset after serial connection
            self.connected = True
            self.connection_changed.emit(True)
            self.parser.reset()
            self.status_received.emit(
                StatusMessage("INFO", f"Connected to {self.port_name} @ {self.baud_rate} baud")
            )
        except serial.SerialException as e:
            self.connected = False
            self.connection_changed.emit(False)
            self.error_occurred.emit(f"Failed to open {self.port_name}: {str(e)}")
    
    def _close_port(self):
        """Close serial port."""
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
            except Exception as e:
                self.error_occurred.emit(f"Error closing port: {str(e)}")
        
        if self.connected:
            self.connected = False
            self.connection_changed.emit(False)
            self.status_received.emit(StatusMessage("INFO", "Disconnected"))
    
    def run(self):
        """Main thread loop."""
        self._open_port()
        
        while self.running:
            if not self.connected:
                time.sleep(0.5)
                continue
            
            try:
                # Read incoming data
                if self.serial_port and self.serial_port.in_waiting > 0:
                    line = self.serial_port.readline().decode('utf-8', errors='ignore')
                    if line:
                        self._process_line(line)
                
                # Request status periodically (for flow sensor reading)
                self._request_status_periodic()
                
                # Send queued commands (rate limited)
                self._send_queued_commands()
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.001)
                
            except serial.SerialException as e:
                self.error_occurred.emit(f"Serial error: {str(e)}")
                self.connected = False
                self.connection_changed.emit(False)
                time.sleep(1)  # Wait before retry
                self._reconnect()
            
            except Exception as e:
                self.error_occurred.emit(f"Unexpected error: {str(e)}")
        
        self._close_port()
    
    def _process_line(self, line: str):
        """Parse and emit line data."""
        result = self.parser.parse_line(line)
        
        if isinstance(result, dict) and 'flow' in result:
            # Flow data
            self.flow_received.emit(result['flow'])
        elif isinstance(result, TelemetryData):
            self.telemetry_received.emit(result)
        elif isinstance(result, DiscreteStateMessage):
            # Convertir a diccionario y emitir
            self.discrete_state_received.emit(result.to_dict())
            # Registrar tiempos en estadísticas
            self._update_stats_from_discrete(result)
        elif isinstance(result, StatusMessage):
            self.status_received.emit(result)
        elif isinstance(result, MetricsData):
            self.metrics_received.emit(result)
    
    def _send_queued_commands(self):
        """Send commands from queue with rate limiting."""
        if not self.serial_port or not self.serial_port.is_open:
            return
        
        current_time = time.time()
        
        # Rate limiting
        if current_time - self.last_command_time < self.min_command_interval:
            return
        
        self.queue_mutex.lock()
        if self.command_queue:
            command = self.command_queue.pop(0)
            self.queue_mutex.unlock()
            
            try:
                self.serial_port.write(command.encode('utf-8'))
                self.serial_port.flush()
                self.last_command_time = current_time
                
                # Log command for debugging
                self.logger.log_command(command, status="SENT")
                
                # Echo sent command
                self.status_received.emit(
                    StatusMessage("CMD", f"→ {command.strip()}")
                )
            except Exception as e:
                self.logger.log_error(f"Send failed: {str(e)}", command.strip())
                self.error_occurred.emit(f"Send failed: {str(e)}")
        else:
            self.queue_mutex.unlock()
    
    def _request_status_periodic(self):
        """Request STATUS periodically to get flow readings."""
        import time as time_module
        current_time_ms = int(time_module.time() * 1000)
        
        if current_time_ms - self.last_status_request >= self.status_request_interval:
            self.send_command("STATUS\n")
            self.last_status_request = current_time_ms
    
    @staticmethod
    def list_available_ports() -> List[str]:
        """Get list of available serial ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def start_sequence_timing(self, tank1_ms: int, tank2_ms: int):
        """Inicia cronómetro de secuencia."""
        if self.stats_logger:
            self.stats_logger.start_execution(tank1_ms, tank2_ms)
        self.start_time = time.time()
        print(f"[SerialWorker] Timing iniciado: T1={tank1_ms}ms, T2={tank2_ms}ms")
    
    def _update_stats_from_discrete(self, msg: DiscreteStateMessage):
        """Actualiza estadísticas basado en mensaje discreto."""
        if self.start_time is None or self.stats_logger is None or self.stats_logger.current_stat is None:
            return
        
        try:
            elapsed = int((time.time() - self.start_time) * 1000)
            msg_type = msg.msg_type
            progress = msg.progress
            tank = msg.tank
            
            print(f"[StatsLogger] Mensaje discreto: type={msg_type}, tank={tank}, progress={progress}, elapsed={elapsed}ms")
            
            # Registra cuando Tank1 se completa (100% en FILL con tank=1)
            if msg_type == "FILL" and tank == 1 and progress == 100:
                print(f"[StatsLogger] Tank1 completado en {elapsed}ms")
                self.stats_logger.record_tank_completion(1, elapsed)
            
            # Registra cuando Tank2 se completa (100% en FILL con tank=2)
            elif msg_type == "FILL" and tank == 2 and progress == 100:
                print(f"[StatsLogger] Tank2 completado en {elapsed}ms")
                self.stats_logger.record_tank_completion(2, elapsed)
                self.last_tank2_progress = 100
                # FALLBACK: Si Tank2 llegó a 100%, es probable que la secuencia termine pronto
                # Esperar un poco para ver si llega COMPLETE
            
            # Registra cuando secuencia finaliza (evento explícito COMPLETE)
            elif msg_type == "COMPLETE":
                print(f"[StatsLogger] Secuencia COMPLETADA en {elapsed}ms")
                self.stats_logger.end_execution(elapsed, "completed")
                self.start_time = None
                self.last_tank2_progress = 0
            
            # FALLBACK: Si volvemos a IDLE cuando Tank2 estaba en 100%, finalizar secuencia
            elif msg_type == "IDLE" and self.last_tank2_progress == 100:
                print(f"[StatsLogger] FALLBACK: Secuencia terminada en {elapsed}ms (IDLE detectado)")
                self.stats_logger.end_execution(elapsed, "completed")
                self.start_time = None
                self.last_tank2_progress = 0
            
            # Reset si hay error o parada
            elif msg_type == "STOPPED":
                print(f"[StatsLogger] Secuencia DETENIDA en {elapsed}ms")
                if self.stats_logger.current_stat:
                    self.stats_logger.end_execution(elapsed, "stopped")
                self.start_time = None
                self.last_tank2_progress = 0
        
        except Exception as e:
            print(f"[SerialWorker] Error en timing: {e}")
