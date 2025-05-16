import sqlite3
from datetime import datetime
from ...database import get_db_connection

def save_approved_budget(data, username):
    """Guarda un registro de presupuesto aprobado (SCF-72)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO approved_budget (
            military_unit, specialty, date, details, 
            approved_budget, item_110101, item_110406, item_800000, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['unidad_militar'],
            data['especialidad'],
            data['fecha_d_m_a'],
            data['detalles'],
            float(data['presupuesto_aprobado']),
            float(data['partida_directiva_110101']),
            float(data['partida_directiva_110406']),
            float(data['partida_directiva_800000']),
            username
        ))
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        raise Exception(f"Error de base de datos: {str(e)}")
    finally:
        conn.close()

def get_approved_budgets(filters=None):
    """Recupera registros de presupuesto aprobado con filtros avanzados"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
        SELECT * FROM approved_budget 
        WHERE 1=1
        '''
        params = []
        
        if filters:
            # Filtros por unidad y especialidad
            if 'military_unit' in filters:
                query += ' AND military_unit LIKE ?'
                params.append(f'%{filters["military_unit"]}%')
                
            if 'specialty' in filters:
                query += ' AND specialty LIKE ?'
                params.append(f'%{filters["specialty"]}%')
            
            # Filtros por fechas
            if 'date_from' in filters:
                query += ' AND date >= ?'
                params.append(filters['date_from'])
                
            if 'date_to' in filters:
                query += ' AND date <= ?'
                params.append(filters['date_to'])
            
            # Filtros por montos
            if 'min_amount' in filters:
                query += ' AND approved_budget >= ?'
                params.append(float(filters['min_amount']))
                
            if 'max_amount' in filters:
                query += ' AND approved_budget <= ?'
                params.append(float(filters['max_amount']))
            
            # Filtro por partidas específicas
            if 'items' in filters:
                items = filters['items']
                if items.get('110101'):
                    query += ' AND item_110101 > 0'
                if items.get('110406'):
                    query += ' AND item_110406 > 0'
                if items.get('800000'):
                    query += ' AND item_800000 > 0'
        
        # Ordenamiento
        sort_field = filters.get('sort_field', 'date') if filters else 'date'
        sort_order = filters.get('sort_order', 'DESC') if filters else 'DESC'
        valid_sort_fields = ['date', 'approved_budget', 'military_unit']
        sort_field = sort_field if sort_field in valid_sort_fields else 'date'
        
        query += f' ORDER BY {sort_field} {sort_order}'
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        raise Exception(f"Error de base de datos: {str(e)}")
    finally:
        conn.close()

def save_budget_execution(data, username):
    """Guarda un registro de presupuesto ejecutado (SCF-73)"""
    try:
        # Calcular saldo y porcentaje
        approved = float(data['presupuesto_aprobado'])
        executed_800440 = float(data['ejecución_partida_800440'] or 0)
        executed_890441 = float(data['ejecución_partida_890441'] or 0)
        balance = approved - (executed_800440 + executed_890441)
        percentage = ((executed_800440 + executed_890441) / approved) * 100 if approved != 0 else 0
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO budget_execution (
            military_unit, specialty, directive_item, date, details,
            approved_budget, executed_800440, executed_890441, balance,
            execution_percentage, expense_concept, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['unidad_militar'],
            data['especialidad'],
            data['partida_directiva'],
            data['fecha_d_m_a'],
            data['detalles'],
            approved,
            executed_800440,
            executed_890441,
            balance,
            percentage,
            data['concepto_de_gastos'],
            username
        ))
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        raise Exception(f"Error de base de datos: {str(e)}")
    finally:
        conn.close()

def get_budget_executions(filters=None):
    """Recupera registros de presupuesto ejecutado con filtros opcionales"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
        SELECT * FROM budget_execution 
        WHERE 1=1
        '''
        params = []
        
        if filters:
            if 'military_unit' in filters:
                query += ' AND military_unit = ?'
                params.append(filters['military_unit'])
            if 'directive_item' in filters:
                query += ' AND directive_item = ?'
                params.append(filters['directive_item'])
            if 'start_date' in filters:
                query += ' AND date >= ?'
                params.append(filters['start_date'])
            if 'end_date' in filters:
                query += ' AND date <= ?'
                params.append(filters['end_date'])
            if 'expense_concept' in filters:
                query += ' AND expense_concept = ?'
                params.append(filters['expense_concept'])
        
        query += ' ORDER BY date DESC'
        cursor.execute(query, params)
        
        return cursor.fetchall()
    except sqlite3.Error as e:
        raise Exception(f"Error de base de datos: {str(e)}")
    finally:
        conn.close()