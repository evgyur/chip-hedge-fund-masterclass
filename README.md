# chip-hedge-fund-masterclass

**Торговая идея и дашборд в Codex** — публичный набор для мастер-класса Chip / «Человек 2.0».

Один репозиторий: дашборд двух рынков, TradingView Chip, подключение Альфа PRO MCP, Parallel, калькулятор позиции и шаблон плана сделки. Это инструменты исследования, не сигналы и не обещание доходности. Торговые заявки не отправляются.

## Вставьте в Codex

```text
Подготовь этот мастер-класс в моей выбранной папке проекта:
https://github.com/evgyur/chip-hedge-fund-masterclass
Сначала прочитай README.md и SKILL.md. Если скил ещё не установлен,
клонируй этот репозиторий в .agents/skills/chip-hedge-fund-masterclass
текущего проекта. Существующую папку не перезаписывай.
Проверь программы и открой учебный дашборд. Затем проведи меня по шагам.
Не меняй настройки MCP без подтверждения и не проси секреты в чате.
```

После установки начните новый диалог в той же папке, если Codex ещё не видит скил. Пример вызова в Codex: `$chip-hedge-fund-masterclass помоги начать мастер-класс`.

## Что внутри

| Задача | Включено | Подключение |
|---|---|---|
| Страница портфеля | [Шаблон](assets/dashboard.html), [условные данные](assets/combined-demo.json), API/JSON адаптеры | [Инструкция](references/dashboard.md) |
| График TradingView | Полный публичный исходник [tradingview-chip](https://github.com/evgyur/tradingview-chip) на commit `abb651b5627946063f8dbd9931ec1f3ad1180841` | [Инструкция](references/tradingview.md) |
| Вид графика Биржевика | [Параметры](assets/birzhevik-chart-settings.json), реконструкция по публичным видео | [Установка вручную и через подсказки Codex](references/birzhevik-chart.md) |
| Мосбиржа через Альфа PRO | Инструкция native MCP и нормализатор фактических ответов | [Инструкция](references/alfa-mcp.md) |
| Поиск Parallel | Подключение официального MCP и проверка источников | [Инструкция](references/parallel.md) |
| Размер позиции | Детерминированный расчёт, комиссии и тесты | [Инструкция](references/risk.md) |
| План сделки | [Пустой шаблон](assets/decision-template.md) | [Карта мастер-класса](WORKSHOP-SKILLS.md) |

## Требования

- Codex через свой ChatGPT. Отдельный OpenAI API-ключ для упражнений не нужен.
- Python 3.10+ для расчётов и JSON-адаптеров (`python3` на Linux/macOS, `py -3` на Windows).
- Для TradingView: **Node.js 24+**, Chrome/Chromium/Edge и аккаунт TradingView. Отдельный браузер требует отдельного входа; уже открытая сессия не передаётся автоматически.
- Для своего брокера: установленный и авторизованный терминал с native MCP, выбранный счёт и разрешённое чтение. Если его нет, используйте явно учебные данные.

## Попробовать без подключений

Из корня этого репозитория:

```bash
python3 scripts/workshop.py doctor
python3 scripts/workshop.py demo --output ./output/demo
python3 scripts/workshop.py risk --entry 300 --stop 294 --lot 10 --capital 1000000 --risk 3000
python3 -m unittest discover -s tests -v
node scripts/verify-core.cjs
```

Откройте `output/demo/dashboard.html` в браузере. В примере нет реального счёта или кошелька. Установленный скил, работающий офлайн-пример и реальные подключения — три разные проверки.

Подключения [Parallel](references/parallel.md), [TradingView](references/tradingview.md) и [Альфа](references/alfa-mcp.md) настраиваются отдельно и только с вашего согласия. Codex читает данные локально и сохраняет снимок. Страница не принимает API-ключи и не аутентифицируется к брокеру.

## Публичные источники

- Основной набор: https://github.com/evgyur/chip-hedge-fund-masterclass
- Наш TradingView: https://github.com/evgyur/tradingview-chip
- Parallel MCP: https://docs.parallel.ai/integrations/mcp/installation
- Альфа PRO MCP: https://alfabank.ru/make-money/investments/pro-terminal/mcp/
- Навыки Codex: https://developers.openai.com/codex/skills/

См. [происхождение и лицензии](THIRD_PARTY_NOTICES.md), [разрешения](references/permissions.md) и [границы проверок](VALIDATION.md). Не добавляйте в публичный fork ключи, профили браузера или данные своего счёта.
