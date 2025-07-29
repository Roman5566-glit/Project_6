import pygame
import sys
import time

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Полноэкранный режим
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
pygame.display.set_caption("HackSim 2077")

font = pygame.font.Font(None, 28)
input_text = ""
log = []
mission_index = 0
start_time = time.time()
mission_timer = 120  # секунд на миссию
scroll_offset = 0  # прокрутка терминала

# Звук клавиш (опционально)
try:
    beep = pygame.mixer.Sound("assets/beep.wav")
except:
    beep = None

missions = [
    {
        "intro": ["Миссия 1: Взломать сервер 'OmegaCorp'.", "Введите: connect OmegaCorp"],
        "steps": {
            "connect OmegaCorp": "Соединение установлено. Введите: scan_ports",
            "scan_ports": "Открытые порты: 22, 80, 443. Введите: brute_force 22",
            "brute_force 22": "Пароль найден: hunter2. Миссия выполнена!"
        }
    },
    {
        "intro": ["Миссия 2: Получить доступ к базе данных 'NovaNet'.", "Введите: ping NovaNet"],
        "steps": {
            "ping NovaNet": "Сеть активна. Введите: inject_payload",
            "inject_payload": "Payload внедрён. Введите: decrypt_key",
            "decrypt_key": "Ключ расшифрован: NOVA-77. Миссия выполнена!"
        }
    },
    {
        "intro": ["Миссия 3: Взломать систему наблюдения 'EyeWatch'.", "Введите: override_camera"],
        "steps": {
            "override_camera": "Камеры отключены. Введите: access_feed",
            "access_feed": "Получен видеопоток. Введите: extract_frames",
            "extract_frames": "Кадры сохранены. Миссия выполнена!"
        }
    },
    {
        "intro": ["Миссия 4: Взломать дрон 'SkyRider'.", "Введите: locate_drone"],
        "steps": {
            "locate_drone": "Дрон найден. Введите: hijack_signal",
            "hijack_signal": "Сигнал перехвачен. Введите: redirect_path",
            "redirect_path": "Дрон перенаправлен. Миссия выполнена!"
        }
    },
    {
        "intro": ["Миссия 5: Получить доступ к архиву 'DeepVault'.", "Введите: unlock_archive"],
        "steps": {
            "unlock_archive": "Архив открыт. Введите: scan_documents",
            "scan_documents": "Документы отсканированы. Введите: download_all",
            "download_all": "Загрузка завершена. Миссия выполнена!"
        }
    },
    {
        "intro": ["Миссия 6: Взломать терминал 'BlackBox'.", "Введите: connect BlackBox"],
        "steps": {
            "connect BlackBox": "Терминал подключён. Введите: run_diagnostics",
            "run_diagnostics": "Диагностика завершена. Введите: patch_kernel",
            "patch_kernel": "Ядро обновлено. Миссия выполнена!"
        }
    },
    {
        "intro": ["Миссия 7: Получить доступ к спутнику 'OrbNet'.", "Введите: ping OrbNet"],
        "steps": {
            "ping OrbNet": "Связь установлена. Введите: align_frequency",
            "align_frequency": "Частота синхронизирована. Введите: stream_data",
            "stream_data": "Данные получены. Миссия выполнена!"
        }
    },
    {
        "intro": ["Миссия 8: Взломать сервер 'GhostShell'.", "Введите: breach_firewall"],
        "steps": {
            "breach_firewall": "Брандмауэр обойдён. Введите: inject_ghost",
            "inject_ghost": "Призрак внедрён. Введите: erase_logs",
            "erase_logs": "Следы удалены. Миссия выполнена!"
        }
    },
    {
        "intro": ["Миссия 9: Получить доступ к базе 'QuantumCore'.", "Введите: access_core"],
        "steps": {
            "access_core": "Доступ получен. Введите: decode_matrix",
            "decode_matrix": "Матрица расшифрована. Введите: extract_code",
            "extract_code": "Код извлечён. Миссия выполнена!"
        }
    },
    {
        "intro": ["Миссия 10: Взломать систему 'FinalGate'.", "Введите: initiate_protocol"],
        "steps": {
            "initiate_protocol": "Протокол активирован. Введите: bypass_gate",
            "bypass_gate": "Ворота обойдены. Введите: shutdown_system",
            "shutdown_system": "Система отключена. Миссия выполнена!"
        }
    }
]

def draw_terminal():
    screen.fill((10, 10, 10))
    visible_lines = (HEIGHT - 80) // 30  # динамически рассчитываем количество строк
    start_index = max(0, len(log) - visible_lines - scroll_offset)
    end_index = len(log) - scroll_offset
    y = 20
    for line in log[start_index:end_index]:
        rendered = font.render(line, True, (0, 255, 0))
        screen.blit(rendered, (20, y))
        y += 30
    input_render = font.render("> " + input_text, True, (0, 255, 0))
    screen.blit(input_render, (20, HEIGHT - 40))

    # Таймер
    elapsed = int(time.time() - start_time)
    remaining = max(0, mission_timer - elapsed)
    timer_render = font.render(f"⏱️ Время: {remaining}s", True, (255, 100, 100))
    screen.blit(timer_render, (WIDTH - 200, 20))

    pygame.display.flip()

def process_command(cmd):
    global mission_index, start_time, scroll_offset

    if mission_index >= len(missions):
        log.append("✅ Все миссии уже выполнены. Нет новых заданий.")
        return

    mission = missions[mission_index]
    steps = mission["steps"]
    if cmd in steps:
        log.append(steps[cmd])
        if "Миссия выполнена!" in steps[cmd]:
            mission_index += 1
            if mission_index < len(missions):
                log.append("")
                log.append(f"--- Переход к миссии {mission_index + 1} ---")
                log.extend(missions[mission_index]["intro"])
                start_time = time.time()
            else:
                log.append("")
                log.append("🎉 Все миссии выполнены! Ты — легенда хакерского мира.")
    else:
        log.append(f"❌ Неизвестная команда: {cmd}")
    scroll_offset = 0  # сброс прокрутки после команды

# Инициализация
log.append("Добро пожаловать в HackSim 2077.")
log.extend(missions[0]["intro"])

running = True
while running:
    draw_terminal()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if beep: beep.play()
            if event.key == pygame.K_RETURN:
                log.append("> " + input_text)
                process_command(input_text.strip())
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                running = False  # выход по ESC
            elif event.key == pygame.K_PAGEUP:
                scroll_offset = min(scroll_offset + 5, len(log) - 1)
            elif event.key == pygame.K_PAGEDOWN:
                scroll_offset = max(scroll_offset - 5, 0)
            else:
                input_text += event.unicode

        elif event.type == pygame.MOUSEWHEEL:
            scroll_offset -= event.y  # вверх = +1, вниз = -1
            scroll_offset = max(0, min(scroll_offset, len(log) - 1))

    # Проверка таймера
    if mission_index < len(missions) and time.time() - start_time > mission_timer:
        log.append("⛔ Время вышло. Миссия провалена.")
        mission_index += 1
        if mission_index < len(missions):
            log.append("")
            log.append(f"--- Переход к миссии {mission_index + 1} ---")
            log.extend(missions[mission_index]["intro"])
            start_time = time.time()
        else:
            log.append("")
            log.append("🎉 Все миссии завершены. Некоторые провалены, но ты дошёл до конца!")

pygame.quit()
sys.exit()