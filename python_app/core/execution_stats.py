"""
Módulo de Estadísticas de Ejecución
Registra y analiza tiempos de ejecución de secuencias
"""

from dataclasses import dataclass, asdict
from datetime import datetime
import json
from pathlib import Path
from typing import Optional


@dataclass
class ExecutionStats:
    """Estadísticas de una ejecución de secuencia"""
    
    # Información básica
    execution_id: str
    timestamp: str
    
    # Tiempos esperados (ms)
    tank1_expected: int
    tank2_expected: int
    total_expected: int
    
    # Tiempos reales (ms)
    tank1_real: Optional[int] = None
    tank2_real: Optional[int] = None
    total_real: Optional[int] = None
    
    # Desviaciones (%)
    tank1_deviation: Optional[float] = None
    tank2_deviation: Optional[float] = None
    total_deviation: Optional[float] = None
    
    # Estados
    status: str = "running"  # running, completed, stopped, timeout
    error_message: Optional[str] = None
    
    def calculate_deviations(self):
        """Calcula desviaciones después de finalizar"""
        if self.tank1_real is not None:
            self.tank1_deviation = ((self.tank1_real - self.tank1_expected) 
                                   / self.tank1_expected) * 100
        if self.tank2_real is not None:
            self.tank2_deviation = ((self.tank2_real - self.tank2_expected) 
                                   / self.tank2_expected) * 100
        if self.total_real is not None:
            self.total_deviation = ((self.total_real - self.total_expected) 
                                   / self.total_expected) * 100
    
    def to_dict(self) -> dict:
        """Convierte a diccionario"""
        return asdict(self)
    
    @staticmethod
    def to_json(stats: 'ExecutionStats') -> str:
        """Convierte a JSON"""
        return json.dumps(stats.to_dict(), indent=2)


class StatsLogger:
    """Gestor de estadísticas y persistencia"""
    
    def __init__(self, base_path: str = "logs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.current_stat: Optional[ExecutionStats] = None
        self.history: list = []
        self.load_history()
    
    def start_execution(self, tank1_ms: int, tank2_ms: int):
        """Inicia registro de nueva ejecución"""
        from uuid import uuid4
        
        exec_id = str(uuid4())[:8]
        self.current_stat = ExecutionStats(
            execution_id=exec_id,
            timestamp=datetime.now().isoformat(),
            tank1_expected=tank1_ms,
            tank2_expected=tank2_ms,
            total_expected=tank1_ms + tank2_ms
        )
        print(f"[StatsLogger] Ejecución iniciada: {exec_id}")
        return self.current_stat
    
    def record_tank_completion(self, tank_num: int, elapsed_ms: int):
        """Registra cuando se completa un tanque"""
        if self.current_stat is None:
            return
        
        if tank_num == 1:
            self.current_stat.tank1_real = elapsed_ms
            print(f"[StatsLogger] Tank1 completado en {elapsed_ms}ms")
        elif tank_num == 2:
            self.current_stat.tank2_real = elapsed_ms
            print(f"[StatsLogger] Tank2 completado en {elapsed_ms}ms")
    
    def end_execution(self, total_elapsed_ms: int, status: str = "completed"):
        """Finaliza ejecución y calcula estadísticas"""
        if self.current_stat is None:
            return
        
        self.current_stat.total_real = total_elapsed_ms
        self.current_stat.status = status
        self.current_stat.calculate_deviations()
        
        self.history.append(self.current_stat)
        self.save_stats(self.current_stat)
        
        print(f"[StatsLogger] Ejecución finalizada: {status}")
        self.current_stat = None
    
    def save_stats(self, stats: ExecutionStats):
        """Guarda estadísticas en archivo JSON"""
        filename = self.base_path / f"stats_{stats.execution_id}.json"
        try:
            with open(filename, 'w') as f:
                f.write(ExecutionStats.to_json(stats))
            print(f"[StatsLogger] Guardado: {filename}")
        except Exception as e:
            print(f"[StatsLogger] Error al guardar: {e}")
    
    def load_history(self):
        """Carga histórico desde archivos"""
        try:
            # NO limpiar el historial antes de cargar para evitar duplicados
            # Solo cargar archivos que no estén ya en el historial
            existing_ids = {s.execution_id for s in self.history}
            
            json_files = list(self.base_path.glob("stats_*.json"))
            loaded_count = 0
            
            for file in sorted(json_files):
                with open(file, 'r') as f:
                    data = json.load(f)
                    exec_id = data.get('execution_id')
                    
                    # Solo agregar si no está ya en el historial
                    if exec_id not in existing_ids:
                        stat = ExecutionStats(**data)
                        self.history.append(stat)
                        existing_ids.add(exec_id)
                        loaded_count += 1
            
            print(f"[StatsLogger] Cargado histórico: {len(self.history)} ejecuciones total ({loaded_count} nuevas)")
        except Exception as e:
            print(f"[StatsLogger] Error al cargar histórico: {e}")
    
    def get_summary_stats(self) -> dict:
        """Devuelve resumen de todas las ejecuciones"""
        if not self.history:
            return {
                "total_executions": 0,
                "completed": 0,
                "avg_deviation": 0,
                "max_deviation": 0,
                "min_deviation": 0,
            }
        
        deviations = [s.total_deviation for s in self.history 
                     if s.total_deviation is not None]
        
        return {
            "total_executions": len(self.history),
            "completed": sum(1 for s in self.history if s.status == "completed"),
            "avg_deviation": sum(deviations) / len(deviations) if deviations else 0,
            "max_deviation": max(deviations) if deviations else 0,
            "min_deviation": min(deviations) if deviations else 0,
        }
