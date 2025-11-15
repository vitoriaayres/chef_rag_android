import threading
import time
from datetime import datetime, timedelta
from .database import history_db
import os
import winsound  # Para Windows

class TimerManager:
    """Gerenciador de timers para receitas"""
    
    def __init__(self):
        self.active_threads = {}
        self.timers_data = {}
    
    def create_timer(self, timer_name, duration_minutes, recipe_name='', step_description='', user_id='default_user'):
        """Cria e inicia um novo timer"""
        timer_id = history_db.add_timer(
            timer_name=timer_name,
            recipe_name=recipe_name,
            step_description=step_description,
            duration_minutes=duration_minutes,
            user_id=user_id
        )
        
        # Cria thread para o timer
        timer_thread = threading.Thread(
            target=self._run_timer,
            args=(timer_id, duration_minutes, timer_name),
            daemon=True
        )
        
        self.active_threads[timer_id] = timer_thread
        self.timers_data[timer_id] = {
            'name': timer_name,
            'recipe': recipe_name,
            'step': step_description,
            'duration': duration_minutes,
            'start_time': datetime.now(),
            'status': 'running'
        }
        
        timer_thread.start()
        
        return timer_id
    
    def _run_timer(self, timer_id, duration_minutes, timer_name):
        """Executa o timer em background"""
        try:
            # Converte para segundos
            duration_seconds = duration_minutes * 60
            
            # Aguarda o tempo especificado
            time.sleep(duration_seconds)
            
            # Timer finalizado
            if timer_id in self.timers_data:
                self.timers_data[timer_id]['status'] = 'finished'
            
            # Para o timer no banco
            history_db.stop_timer(timer_id)
            
            # Toca som de alerta (apenas no Windows)
            self._play_alert_sound()
            
            # Remove da lista de threads ativas
            if timer_id in self.active_threads:
                del self.active_threads[timer_id]
                
        except Exception as e:
            print(f"Erro no timer {timer_id}: {e}")
    
    def _play_alert_sound(self):
        """Toca som de alerta quando o timer termina"""
        try:
            # Toca som do sistema
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            # Ou toca frequência específica
            winsound.Beep(800, 1000)  # 800Hz por 1 segundo
        except:
            # Se não conseguir tocar som, apenas imprime
            print("\a")  # Bell character
    
    def stop_timer(self, timer_id):
        """Para um timer antes de terminar"""
        if timer_id in self.active_threads:
            # Para o timer no banco
            history_db.stop_timer(timer_id)
            
            # Atualiza status local
            if timer_id in self.timers_data:
                self.timers_data[timer_id]['status'] = 'stopped'
            
            # Remove da lista (a thread vai terminar naturalmente)
            if timer_id in self.active_threads:
                del self.active_threads[timer_id]
            
            return True
        return False
    
    def get_active_timers(self, user_id='default_user'):
        """Retorna timers ativos com tempo restante"""
        db_timers = history_db.get_active_timers(user_id)
        active_timers = []
        
        for timer in db_timers:
            timer_id, name, recipe, step, duration, start_time_str, created_at = timer
            
            # Calcula tempo restante
            start_time = datetime.fromisoformat(start_time_str)
            elapsed = (datetime.now() - start_time).total_seconds() / 60  # minutos
            remaining = max(0, duration - elapsed)
            
            # Se o tempo acabou, para o timer
            if remaining <= 0:
                history_db.stop_timer(timer_id)
                continue
            
            timer_info = {
                'id': timer_id,
                'name': name,
                'recipe': recipe,
                'step': step,
                'duration': duration,
                'remaining_minutes': remaining,
                'remaining_formatted': self._format_time(remaining),
                'start_time': start_time_str,
                'status': 'running' if timer_id in self.active_threads else 'paused'
            }
            
            active_timers.append(timer_info)
        
        return active_timers
    
    def _format_time(self, minutes):
        """Formata tempo em minutos para HH:MM:SS"""
        total_seconds = int(minutes * 60)
        hours = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{mins:02d}:{secs:02d}"
        else:
            return f"{mins:02d}:{secs:02d}"
    
    def get_timer_status(self, timer_id):
        """Retorna status de um timer específico"""
        if timer_id in self.timers_data:
            return self.timers_data[timer_id]
        return None
    
    def list_timer_presets(self):
        """Lista presets comuns de timer para receitas"""
        return {
            'Ferver água': 5,
            'Cozinhar ovo': 7,
            'Massas al dente': 8,
            'Refogado básico': 5,
            'Dourar carne': 3,
            'Assar pão': 25,
            'Descansar massa': 30,
            'Marinada rápida': 15,
            'Cozinhar arroz': 20,
            'Levedura ativar': 10
        }

# Instância global do gerenciador de timers
timer_manager = TimerManager()