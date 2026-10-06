# Вариант №7 — практика по Python

Три этапа:
1. Модель слоя доступа к данным (NamedTuple + Storage, REPL, тесты).
2. Удалённый вызов процедур на основе TCP (RPC, XML, LE-порядок байт).
3. Тестирование на основе модели (hypothesis RuleBasedStateMachine).

## Команды
- make install  — установка зависимостей
- make run      — REPL
- make demo     — демонстрация
- make server   — RPC-сервер
- make test     — тесты
- make coverage — покрытие
- make lint     — ruff + radon

## Пример
    from src.models import Storage
    from src import repository as repo
    s = Storage.empty()
    a = repo.create_agent(s, "127.0.0.1", "linux", "curl/8")
    print(repo.get_agents(s))
