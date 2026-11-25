# Карта мастер-класса

Один основной вход: SKILL.md (`chip-hedge-fund-masterclass`). Он выбирает нужную инструкцию, а не загружает всё сразу.

| Шаг | Публичный модуль | Результат |
|---|---|---|
| Впервые в Codex | references/start.md | Папка и первый запуск |
| Новость | references/parallel.md | Исходные ссылки и что нового |
| График | references/tradingview.md + vendored tradingview-chip | Прочитанный график / честный запасной путь |
| Счёт | references/alfa-mcp.md | Выбранный read snapshot |
| Размер | references/risk.md | Проверенный расчёт и decision.md |
| Портфель | references/dashboard.md | dashboard.html, RUB/USD отдельно |

В vendored upstream сохранён его собственный skill `tradingview-chip` и поддерживающие references. Это компонент нашего набора, а не второй обязательный пользовательский установочный шаг. Не устанавливайте его глобально отдельно, если основной вход уже даёт нужные инструкции и MCP настроен.
