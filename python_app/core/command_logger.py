"""
Command Logger - Registra todos los comandos enviados para debugging y análisis.
Formato: CSV para fácil importación a Excel/Pandas
"""

import os
import csv
from datetime import datetime
from pathlib import Path


class CommandLogger:
    """Logger de comandos enviados al Arduino."""
    
    def __init__(self, log_dir: str = None):
        """
        Inicializar logger de comandos.
        
        Args:
            log_dir: Directorio donde guardar logs. Si es None, usa ./logs/
        """
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear archivo de log con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"commands_{timestamp}.csv"
        
        # Inicializar CSV con headers
        self._init_csv()
        
        print(f"[LOG] Command logging initialized: {self.log_file}")
    
    def _init_csv(self):
        """Crear archivo CSV con headers."""
        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp',
                'Command Type',
                'Command',
                'Parameter 1',
                'Parameter 2',
                'Parameter 3',
                'Parameter 4',
                'Status',
                'Notes'
            ])
    
    def log_command(self, command: str, cmd_type: str = None, status: str = "SENT", notes: str = ""):
        """
        Registrar un comando enviado.
        
        Args:
            command: Comando completo (ej: "PUMP,200")
            cmd_type: Tipo de comando (PUMP, SERVO1, SERVO2, TIMECFG, TIMESEQ, etc)
            status: Estado del comando (SENT, SUCCESS, ERROR)
            notes: Notas adicionales
        """
        try:
            # Parse comando
            parts = command.strip().replace('\n', '').split(',')
            cmd_name = parts[0] if parts else "UNKNOWN"
            
            if cmd_type is None:
                cmd_type = cmd_name
            
            # Extraer parámetros
            params = ['', '', '', '']
            for i in range(1, min(5, len(parts))):
                params[i-1] = parts[i]
            
            # Escribir en CSV
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],  # Timestamp con ms
                    cmd_type,
                    command.strip(),
                    params[0],
                    params[1],
                    params[2],
                    params[3],
                    status,
                    notes
                ])
        except Exception as e:
            print(f"❌ Error logging command: {e}")
    
    def log_sequence_start(self, tank1_ms: int, tank1_angles: tuple, tank2_ms: int, 
                          tank2_angles: tuple, pwm: int):
        """Registrar inicio de secuencia con configuración."""
        self.log_command(
            f"TIMESEQ,{pwm}",
            cmd_type="SEQUENCE_START",
            status="SUCCESS",
            notes=f"Tank1: {tank1_ms}ms {tank1_angles}° | Tank2: {tank2_ms}ms {tank2_angles}° | PWM: {pwm}"
        )
    
    def log_sequence_complete(self, duration_ms: int, errors: int = 0):
        """Registrar finalización de secuencia."""
        self.log_command(
            "SEQUENCE_COMPLETE",
            cmd_type="SEQUENCE_END",
            status="SUCCESS" if errors == 0 else "WARNING",
            notes=f"Duration: {duration_ms}ms | Errors: {errors}"
        )
    
    def log_error(self, error_msg: str, command: str = ""):
        """Registrar error."""
        self.log_command(
            command if command else "ERROR",
            cmd_type="ERROR",
            status="ERROR",
            notes=error_msg
        )
    
    def get_log_path(self) -> str:
        """Retornar path del archivo de log actual."""
        return str(self.log_file)
    
    def get_all_logs(self) -> list:
        """Retornar lista de todos los archivos de log."""
        try:
            return sorted([f.name for f in self.log_dir.glob("commands_*.csv")])
        except Exception:
            return []
    
    def export_summary(self) -> dict:
        """
        Exportar resumen de estadísticas de comandos.
        
        Returns:
            Dict con estadísticas
        """
        try:
            stats = {
                'total_commands': 0,
                'by_type': {},
                'errors': 0,
                'sequences': 0
            }
            
            with open(self.log_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Command Type']:
                        stats['total_commands'] += 1
                        cmd_type = row['Command Type']
                        stats['by_type'][cmd_type] = stats['by_type'].get(cmd_type, 0) + 1
                        
                        if row['Status'] == 'ERROR':
                            stats['errors'] += 1
                        if row['Command Type'] == 'SEQUENCE_START':
                            stats['sequences'] += 1
            
            return stats
        except Exception as e:
            print(f"❌ Error exporting summary: {e}")
            return {}


# Instancia global del logger
_command_logger = None


def get_logger() -> CommandLogger:
    """Obtener instancia del logger (singleton)."""
    global _command_logger
    if _command_logger is None:
        _command_logger = CommandLogger()
    return _command_logger


def init_logger(log_dir: str = None) -> CommandLogger:
    """Inicializar logger de comandos."""
    global _command_logger
    _command_logger = CommandLogger(log_dir)
    return _command_logger
