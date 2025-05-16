from fpdf import FPDF
from datetime import datetime

class SCF72PDF(FPDF):
    def header(self):
        # Logo o título
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'MINFAR', 0, 1, 'L')
        self.cell(0, 10, 'REGISTRO Y CONTROL DEL PRESUPUESTO APROBADO POR GRUPO PRESUPUESTARIO SCF-72', 0, 1, 'C')
        
        # Información de la unidad
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'UNIDAD MILITAR: {self.unit}', 0, 1, 'L')
        self.cell(0, 10, f'ESPECIALIDAD: {self.specialty}', 0, 1, 'L')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
        
    def create_pdf(self, data):
        self.unit = data['unidad_militar']
        self.specialty = data['especialidad']
        
        self.add_page()
        self.set_font('Arial', '', 10)
        
        # Encabezado de la tabla
        self.set_fill_color(200, 220, 255)
        self.cell(40, 10, 'FECHA', 1, 0, 'C', 1)
        self.cell(60, 10, 'DETALLES', 1, 0, 'C', 1)
        self.cell(40, 10, 'PRESUPUESTO APROBADO', 1, 0, 'C', 1)
        self.cell(30, 10, '110101', 1, 0, 'C', 1)
        self.cell(30, 10, '110406', 1, 0, 'C', 1)
        self.cell(30, 10, '800000', 1, 1, 'C', 1)
        
        # Datos
        self.set_fill_color(255, 255, 255)
        self.cell(40, 10, data['fecha_d_m_a'], 1)
        self.cell(60, 10, data['detalles'], 1)
        self.cell(40, 10, data['presupuesto_aprobado'], 1)
        self.cell(30, 10, data['partida_directiva_110101'], 1)
        self.cell(30, 10, data['partida_directiva_110406'], 1)
        self.cell(30, 10, data['partida_directiva_800000'], 1)
        
        # Suma acumulada
        self.set_font('Arial', 'B', 10)
        self.cell(100, 10, 'SUMA ACUMULADA', 1, 0, 'R')
        self.cell(40, 10, data['presupuesto_aprobado'], 1)
        self.cell(30, 10, data['partida_directiva_110101'], 1)
        self.cell(30, 10, data['partida_directiva_110406'], 1)
        self.cell(30, 10, data['partida_directiva_800000'], 1, 1)
        
        return self