import socket
import time
import random
from datetime import datetime

class STM32Emulator:
    def __init__(self, device_id="STM32_001", server_host='localhost', server_port=8888):
        self.device_id = device_id
        self.server_host = server_host
        self.server_port = server_port
        self.message_count = 0
        self.connected = False
        
        print(f"🎮 Эмулятор STM32: {device_id}")
        print(f"📍 Сервер: {server_host}:{server_port}")
    
    def send_data(self, data_value):
        """Отправка данных на TCP сервер"""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(5)
            client.connect((self.server_host, self.server_port))
            
            # Формируем сообщение в формате: устройство:данные:временная_метка
            timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            message = f"{self.device_id}:{data_value}:{timestamp}"
            
            client.send(message.encode('utf-8'))
            
            # Получаем ответ от сервера
            response = client.recv(1024).decode('utf-8').strip()
            client.close()
            
            self.message_count += 1
            
            if response.startswith("OK"):
                print(f"✅ [{self.message_count}] Отправлено: {message} | Ответ: {response}")
                return True
            else:
                print(f"❌ [{self.message_count}] Ошибка: {message} | Ответ: {response}")
                return False
            
        except Exception as e:
            print(f"❌ [{self.message_count}] Ошибка подключения: {e}")
            return False
    
    def generate_sensor_data(self):
        """Генерация тестовых данных датчиков"""
        # Типы данных для эмуляции с разной вероятностью
        data_options = [
            # Температура (40%)
            ("TEMP", [
                "TEMP_22", "TEMP_23", "TEMP_24", "TEMP_25", 
                "TEMP_26", "TEMP_27", "TEMP_28"
            ], 0.4),
            
            # Влажность (25%)
            ("HUMIDITY", [
                "HUMIDITY_45", "HUMIDITY_50", "HUMIDITY_55", 
                "HUMIDITY_60", "HUMIDITY_65"
            ], 0.25),
            
            # Давление (15%)
            ("PRESSURE", [
                "PRESSURE_1000", "PRESSURE_1005", "PRESSURE_1010", 
                "PRESSURE_1015", "PRESSURE_1020"
            ], 0.15),
            
            # Статус LED (10%)
            ("LED", ["LED_ON", "LED_OFF"], 0.1),
            
            # События (10%)
            ("EVENT", [
                "MOTION_DETECTED", "BUTTON_PRESSED", "SYSTEM_OK",
                "ALARM_TRIGGERED", "BATTERY_LOW"
            ], 0.1)
        ]
        
        # Выбираем тип данных на основе вероятности
        rand = random.random()
        cumulative_prob = 0
        
        for data_type, values, probability in data_options:
            cumulative_prob += probability
            if rand <= cumulative_prob:
                return random.choice(values)
        
        return "UNKNOWN_DATA"
    
    def start_emulation(self, interval=5, duration=None):
        """Запуск эмуляции работы STM32"""
        print(f"\n🚀 Запуск эмуляции...")
        print(f"⏱️  Интервал отправки: {interval} секунд")
        print(f"⏰ Продолжительность: {duration if duration else 'бесконечно'} секунд")
        print("⏸  Для остановки нажмите Ctrl+C\n")
        
        start_time = time.time()
        message_count = 0
        success_count = 0
        
        try:
            while True:
                # Проверяем продолжительность работы
                if duration and (time.time() - start_time) > duration:
                    print(f"\n⏰ Завершение по времени ({duration} секунд)")
                    break
                
                # Генерируем и отправляем данные
                data_value = self.generate_sensor_data()
                success = self.send_data(data_value)
                
                if success:
                    success_count += 1
                message_count += 1
                
                # Рассчитываем статистику
                success_rate = (success_count / message_count) * 100
                
                # Выводим статистику каждые 10 сообщений
                if message_count % 10 == 0:
                    print(f"\n📈 Статистика: {success_count}/{message_count} успешно ({success_rate:.1f}%)")
                
                # Ждем указанный интервал
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Остановка эмулятора по команде пользователя")
        
        # Финальная статистика
        total_time = time.time() - start_time
        print(f"\n📊 ИТОГИ РАБОТЫ:")
        print(f"   📨 Всего отправлено: {message_count} сообщений")
        print(f"   ✅ Успешных: {success_count}")
        print(f"   ❌ Ошибок: {message_count - success_count}")
        print(f"   📈 Успешность: {success_rate:.1f}%")
        print(f"   ⏱️  Общее время: {total_time:.1f} секунд")
        print(f"   📊 Средняя скорость: {message_count/total_time:.1f} сообщ/сек")

def main():
    """Основная функция эмулятора"""
    # Можно создать несколько эмуляторов для тестирования
    emulator1 = STM32Emulator("STM32_001")
    
    # Запускаем на 2 минуты для демонстрации (120 секунд)
    emulator1.start_emulation(interval=5, duration=120)

if __name__ == "__main__":
    main()