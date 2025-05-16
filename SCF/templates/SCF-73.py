from fpdf import FPDF
from datetime import datetime

class SCF73PDF(FPDF):
    def header(self):
        # Logo o título
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'MINFAR', 0, 1, 'L')
        self.cell(0, 10, 'REGISTRO Y CONTROL DEL PRESUPUESTO DESAGREGADO Y SU EJECUCIÓN SCF-73', 0, 1, 'C')
        
        # Información de la unidad
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'UNIDAD MILITAR: {self.unit}', 0, 1, 'L')
        self.cell(0, 10, f'ESPECIALIDAD: {self.specialty}', 0, 1, 'L')
        self.cell(0, 10, f'PARTIDA DIRECTIVA: {self.directive_item}', 0, 1, 'L')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
        
    def create_pdf(self, data):
        self.unit = data['unidad_militar']
        self.specialty = data['especialidad']
        self.directive_item = data['partida_directiva']
        
        self.add_page()
        self.set_font('Arial', '', 10)
        
        # Encabezado de la tabla
        self.set_fill_color(200, 220, 255)
        self.cell(30, 10, 'FECHA', 1, 0, 'C', 1)
        self.cell(60, 10, 'DETALLES', 1, 0, 'C', 1)
        self.cell(30, 10, 'PRESUPUESTO', 1, 0, 'C', 1)
        self.cell(30, 10, '800440', 1, 0, 'C', 1)
        self.cell(30, 10, '890441', 1, 0, 'C', 1)
        self.cell(25, 10, 'SALDO', 1, 0, 'C', 1)
        self.cell(25, 10, '% EJECUT', 1, 1, 'C', 1)
        
        # Datos
        self.set_fill_color(255, 255, 255)
        self.cell(30, 10, data['fecha_d_m_a'], 1)
        self.cell(60, 10, data['detalles'], 1)
        self.cell(30, 10, data['presupuesto_aprobado'], 1)
        self.cell(30, 10, data['ejecución_partida_800440'], 1)
        self.cell(30, 10, data['ejecución_partida_890441'], 1)
        self.cell(25, 10, data.get('saldo', '0.00'), 1)
        self.cell(25, 10, data.get('porcentaje_ejecutado', '0.00%'), 1, 1)
        
        # Suma acumulada
        self.set_font('Arial', 'B', 10)
        self.cell(90, 10, 'SUMA ACUMULADA', 1, 0, 'R')
        self.cell(30, 10, data['presupuesto_aprobado'], 1)
        self.cell(30, 10, data['ejecución_partida_800440'], 1)
        self.cell(30, 10, data['ejecución_partida_890441'], 1)
        self.cell(25, 10, data.get('saldo', '0.00'), 1)
        self.cell(25, 10, data.get('porcentaje_ejecutado', '0.00%'), 1, 1)
        
        # Concepto de gastos
        self.ln(5)
        self.cell(0, 10, f"CONCEPTO DE GASTOS: {data['concepto_de_gastos'].upper()}", 0, 1)
        
        return self