"""
Página de Estadísticas - Interfaz UI
Muestra análisis de precisión y desempeño del sistema
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from core.execution_stats import StatsLogger
import csv
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class StatisticsPage(QWidget):
    def __init__(self, stats_logger: StatsLogger):
        super().__init__()
        self.stats_logger = stats_logger
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)
        
        # === TÍTULO ===
        title = QLabel("📊 ESTADÍSTICAS DE EJECUCIÓN")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # === RESUMEN RÁPIDO ===
        summary_group = QGroupBox("RESUMEN GENERAL")
        summary_layout = QHBoxLayout()
        
        self.total_exec_label = QLabel("Ejecuciones: 0")
        self.completed_label = QLabel("Completadas: 0")
        self.avg_dev_label = QLabel("Desv. Promedio: 0%")
        
        # Estilos
        for label in [self.total_exec_label, self.completed_label, self.avg_dev_label]:
            label_font = QFont()
            label_font.setPointSize(11)
            label_font.setBold(True)
            label.setFont(label_font)
        
        summary_layout.addWidget(self.total_exec_label)
        summary_layout.addWidget(self.completed_label)
        summary_layout.addWidget(self.avg_dev_label)
        summary_layout.addStretch()
        
        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)
        
        # === TABLA DE HISTÓRICO ===
        history_group = QGroupBox("HISTÓRICO DE EJECUCIONES")
        history_layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Esperado (ms)", "Real (ms)", 
            "Desv. (%)", "Tank1 (ms)", "Tank2 (ms)", "Estado", "Tiempo"
        ])
        
        # Ajustar ancho de columnas
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 80)
        self.table.setColumnWidth(7, 150)
        
        self.table.setMaximumHeight(300)
        
        history_layout.addWidget(self.table)
        
        # Botones
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Actualizar")
        export_btn = QPushButton("💾 Exportar CSV")
        clear_btn = QPushButton("🗑️ Limpiar")
        
        refresh_btn.clicked.connect(self.update_display)
        export_btn.clicked.connect(self.export_csv)
        clear_btn.clicked.connect(self.clear_history)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        history_layout.addLayout(button_layout)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        # === ESTADÍSTICAS DETALLADAS ===
        details_group = QGroupBox("ESTADÍSTICAS DETALLADAS")
        details_layout = QHBoxLayout()
        
        self.min_dev_label = QLabel("Desv. Mínima: -")
        self.max_dev_label = QLabel("Desv. Máxima: -")
        
        for label in [self.min_dev_label, self.max_dev_label]:
            label_font = QFont()
            label_font.setPointSize(10)
            label.setFont(label_font)
        
        details_layout.addWidget(self.min_dev_label)
        details_layout.addWidget(self.max_dev_label)
        details_layout.addStretch()
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        # === GRÁFICAS DE CONTROL DISCRETO ===
        if MATPLOTLIB_AVAILABLE:
            charts_group = QGroupBox("📊 GRÁFICAS DE CONTROL DISCRETO")
            charts_layout = QHBoxLayout()
            
            # Gráfica 1: Desviaciones en el tiempo
            self.fig1 = Figure(figsize=(4, 3), dpi=80, facecolor='#0a0e1a')
            self.ax1 = self.fig1.add_subplot(111)
            self.canvas1 = FigureCanvas(self.fig1)
            self.canvas1.setMinimumHeight(250)
            charts_layout.addWidget(self.canvas1)
            
            # Gráfica 2: Tiempo Real vs Esperado
            self.fig2 = Figure(figsize=(4, 3), dpi=80, facecolor='#0a0e1a')
            self.ax2 = self.fig2.add_subplot(111)
            self.canvas2 = FigureCanvas(self.fig2)
            self.canvas2.setMinimumHeight(250)
            charts_layout.addWidget(self.canvas2)
            
            charts_group.setLayout(charts_layout)
            layout.addWidget(charts_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Actualizar datos iniciales
        self.update_display()
        
        # Timer para auto-actualizar cada 2 segundos
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.update_display)
        self.refresh_timer.start(2000)  # 2 segundos
    
    def update_display(self):
        """Actualiza los datos mostrados"""
        # Recargar histórico desde archivos por si hubo cambios externos
        self.stats_logger.load_history()
        self.update_summary()
        self.update_table()
        if MATPLOTLIB_AVAILABLE:
            self.update_charts()
    
    def update_summary(self):
        """Actualiza el resumen rápido"""
        summary = self.stats_logger.get_summary_stats()
        
        self.total_exec_label.setText(
            f"Ejecuciones: {summary.get('total_executions', 0)}"
        )
        self.completed_label.setText(
            f"Completadas: {summary.get('completed', 0)}"
        )
        
        avg_dev = summary.get('avg_deviation', 0)
        
        # Color según desviación
        if abs(avg_dev) < 2:
            color = "green"
            symbol = "✓"
        elif abs(avg_dev) < 5:
            color = "orange"
            symbol = "⚠"
        else:
            color = "red"
            symbol = "✗"
        
        self.avg_dev_label.setText(
            f"Desv. Promedio: {avg_dev:.2f}% {symbol}"
        )
        self.avg_dev_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        
        # Estadísticas detalladas
        self.min_dev_label.setText(
            f"Desv. Mínima: {summary.get('min_deviation', 0):.2f}%"
        )
        self.max_dev_label.setText(
            f"Desv. Máxima: {summary.get('max_deviation', 0):.2f}%"
        )
    
    def update_table(self):
        """Actualiza tabla de histórico"""
        self.table.setRowCount(len(self.stats_logger.history))
        
        for row, stat in enumerate(self.stats_logger.history):
            # ID
            id_item = QTableWidgetItem(stat.execution_id)
            self.table.setItem(row, 0, id_item)
            
            # Esperado
            expected = f"{stat.total_expected}ms"
            self.table.setItem(row, 1, QTableWidgetItem(expected))
            
            # Real
            real = f"{stat.total_real}ms" if stat.total_real else "-"
            self.table.setItem(row, 2, QTableWidgetItem(real))
            
            # Desviación con color
            if stat.total_deviation is not None:
                dev_str = f"{stat.total_deviation:.2f}%"
                dev_item = QTableWidgetItem(dev_str)
                dev_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Color según desviación
                if abs(stat.total_deviation) < 2:
                    dev_item.setBackground(QColor(144, 238, 144))  # Verde claro
                elif abs(stat.total_deviation) < 5:
                    dev_item.setBackground(QColor(255, 255, 153))  # Amarillo
                else:
                    dev_item.setBackground(QColor(255, 182, 193))  # Rojo claro
                
                self.table.setItem(row, 3, dev_item)
            else:
                self.table.setItem(row, 3, QTableWidgetItem("-"))
            
            # Tank1
            tank1 = f"{stat.tank1_real}ms" if stat.tank1_real else "-"
            self.table.setItem(row, 4, QTableWidgetItem(tank1))
            
            # Tank2
            tank2 = f"{stat.tank2_real}ms" if stat.tank2_real else "-"
            self.table.setItem(row, 5, QTableWidgetItem(tank2))
            
            # Estado
            status_item = QTableWidgetItem(stat.status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 6, status_item)
            
            # Tiempo
            time_str = stat.timestamp.split('T')[1].split('.')[0] if stat.timestamp else "-"
            self.table.setItem(row, 7, QTableWidgetItem(time_str))
    
    def update_charts(self):
        """Actualiza gráficas de control discreto"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        history = self.stats_logger.history
        
        # ── Gráfica 1: Desviaciones en el tiempo ──
        self.ax1.clear()
        deviations = [s.total_deviation for s in history if s.total_deviation is not None]
        
        if deviations:
            self.ax1.plot(range(len(deviations)), deviations, 'o-', color='#00e5ff', linewidth=2, markersize=6)
            self.ax1.axhline(y=0, color='#00ff88', linestyle='--', linewidth=1, alpha=0.7)
            self.ax1.axhline(y=2, color='#fb5607', linestyle=':', linewidth=1, alpha=0.5)
            self.ax1.axhline(y=-2, color='#fb5607', linestyle=':', linewidth=1, alpha=0.5)
            self.ax1.fill_between(range(len(deviations)), -2, 2, alpha=0.1, color='#00ff88')
            
            self.ax1.set_title('Desviaciones en el Tiempo', color='#00e5ff', fontsize=10, fontweight='bold')
            self.ax1.set_xlabel('Ejecución #', color='#9aa0a6', fontsize=9)
            self.ax1.set_ylabel('Desviación (%)', color='#9aa0a6', fontsize=9)
            self.ax1.tick_params(colors='#9aa0a6', labelsize=8)
            self.ax1.spines['bottom'].set_color('#2d3548')
            self.ax1.spines['left'].set_color('#2d3548')
            self.ax1.spines['top'].set_visible(False)
            self.ax1.spines['right'].set_visible(False)
            self.ax1.grid(True, alpha=0.2, color='#2d3548')
            self.ax1.set_facecolor('#141827')
        else:
            # Sin datos
            self.ax1.text(0.5, 0.5, 'Sin datos\nEjecuta una secuencia primero', 
                         ha='center', va='center', color='#9aa0a6', fontsize=12,
                         transform=self.ax1.transAxes)
            self.ax1.set_title('Desviaciones en el Tiempo', color='#00e5ff', fontsize=10, fontweight='bold')
            self.ax1.set_facecolor('#141827')
            self.ax1.tick_params(colors='#9aa0a6')
            self.ax1.spines['bottom'].set_color('#2d3548')
            self.ax1.spines['left'].set_color('#2d3548')
            self.ax1.spines['top'].set_visible(False)
            self.ax1.spines['right'].set_visible(False)
        
        self.fig1.tight_layout()
        self.canvas1.draw()
        
        # ── Gráfica 2: Tiempo Real vs Esperado ──
        self.ax2.clear()
        real_times = [s.total_real for s in history if s.total_real is not None]
        expected_times = [s.total_expected for s in history if s.total_real is not None]
        
        if real_times:
            x_pos = range(len(real_times))
            width = 0.35
            self.ax2.bar([x - width/2 for x in x_pos], expected_times, width, label='Esperado', color='#fb5607', alpha=0.7)
            self.ax2.bar([x + width/2 for x in x_pos], real_times, width, label='Real', color='#00ff88', alpha=0.7)
            
            self.ax2.set_title('Tiempo Real vs Esperado (ms)', color='#00e5ff', fontsize=10, fontweight='bold')
            self.ax2.set_xlabel('Ejecución #', color='#9aa0a6', fontsize=9)
            self.ax2.set_ylabel('Tiempo (ms)', color='#9aa0a6', fontsize=9)
            self.ax2.tick_params(colors='#9aa0a6', labelsize=8)
            self.ax2.spines['bottom'].set_color('#2d3548')
            self.ax2.spines['left'].set_color('#2d3548')
            self.ax2.spines['top'].set_visible(False)
            self.ax2.spines['right'].set_visible(False)
            self.ax2.legend(facecolor='#141827', edgecolor='#2d3548', labelcolor='#e8eaed')
            self.ax2.grid(True, axis='y', alpha=0.2, color='#2d3548')
            self.ax2.set_facecolor('#141827')
        else:
            # Sin datos
            self.ax2.text(0.5, 0.5, 'Sin datos\nEjecuta una secuencia primero', 
                         ha='center', va='center', color='#9aa0a6', fontsize=12,
                         transform=self.ax2.transAxes)
            self.ax2.set_title('Tiempo Real vs Esperado (ms)', color='#00e5ff', fontsize=10, fontweight='bold')
            self.ax2.set_facecolor('#141827')
            self.ax2.tick_params(colors='#9aa0a6')
            self.ax2.spines['bottom'].set_color('#2d3548')
            self.ax2.spines['left'].set_color('#2d3548')
            self.ax2.spines['top'].set_visible(False)
            self.ax2.spines['right'].set_visible(False)
        
        self.fig2.tight_layout()
        self.canvas2.draw()
    
    def export_csv(self):
        """Exporta histórico a CSV"""
        if not self.stats_logger.history:
            QMessageBox.warning(self, "Sin datos", "No hay estadísticas para exportar")
            return
        
        filename = f"estadisticas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow([
                    "ID", "Fecha/Hora", "Esperado (ms)", "Real (ms)", 
                    "Desviación (%)", "Tank1 (ms)", "Tank1 Desv (%)", 
                    "Tank2 (ms)", "Tank2 Desv (%)", "Estado"
                ])
                
                for stat in self.stats_logger.history:
                    date_part = stat.timestamp.split('T')[0] if stat.timestamp else "-"
                    time_part = stat.timestamp.split('T')[1].split('.')[0] if stat.timestamp else "-"
                    datetime_str = f"{date_part} {time_part}"
                    
                    writer.writerow([
                        stat.execution_id,
                        datetime_str,
                        stat.total_expected,
                        stat.total_real or '-',
                        f"{stat.total_deviation:.2f}" if stat.total_deviation is not None else '-',
                        stat.tank1_real or '-',
                        f"{stat.tank1_deviation:.2f}" if stat.tank1_deviation is not None else '-',
                        stat.tank2_real or '-',
                        f"{stat.tank2_deviation:.2f}" if stat.tank2_deviation is not None else '-',
                        stat.status
                    ])
            
            QMessageBox.information(self, "Éxito", f"Exportado a: {filename}")
            print(f"✅ Estadísticas exportadas a: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")
    
    def clear_history(self):
        """Limpia histórico (con confirmación)"""
        reply = QMessageBox.question(
            self, "Confirmar", "¿Descartar todo el histórico?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.stats_logger.history.clear()
            
            # Limpiar archivos JSON
            import os
            try:
                for file in self.stats_logger.base_path.glob("stats_*.json"):
                    os.remove(file)
            except Exception as e:
                print(f"Error al limpiar archivos: {e}")
            
            self.update_display()
            QMessageBox.information(self, "Hecho", "Histórico eliminado")
