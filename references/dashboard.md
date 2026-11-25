# Дашборд двух рынков

Шаблон: assets/dashboard.html. Все числа assets/combined-demo.json синтетические. Скопируйте их командой demo в новую папку и откройте страницу. Есть выбор рынка/счёта, позиции, PnL, маржа, концентрация и сценарий. USD и RUB показываются отдельно. Это не история доходности и не инвестиционный совет.

Для своих данных:
- Hyperliquid: `python scripts/build_snapshot.py --wallet <публичный-адрес> --dexes ,xyz --output onchain-current.json`. Адрес обязателен; чужой кошелёк по умолчанию не задан. Поддержка core/xyz не означает все DEX. Не нужен секретный ключ или подпись.
- Мосбиржа: сначала разрешённый API/MCP через Codex, затем instructions в alfa-mcp.md и локальный portfolio_model.py. Дашборд не принимает ключ и не логинится к брокеру.
- `python scripts/portfolio_model.py combine --input onchain-current.json moex-current.json --output portfolio-combined.json` → загрузите JSON в странице. Старые снимки сохраните. Legacy schema 1 поддерживается.

Схема 2: accounts[] с безопасным alias id, label, market=onchain/moex, currency=USD/RUB, mode=sample/snapshot, as_of с часовым поясом, equity, margin_used, source, coverage и positions[]. У позиции signed_size, multiplier, entry_price, mark_price, kind, unrealized_pnl, liquidation_price и leverage; неизвестное — null. У акций multiplier=1 и нет придуманной индивидуальной ликвидации. Не добавляйте номера счетов и секреты.

Математика в scripts/portfolio_core.js: объём=abs(size×mark×multiplier); PnL из источника при наличии, иначе по разнице цен; сценарий=sum(size×mark×multiplier×shift/100), отдельно по валютам. Доли считаются внутри одной валюты. Исключение позиции меняет только сценарий, не реальный баланс. Неизвестные цены делают сценарий неполным. Нет симуляции гэпов/ликвидаций/комиссий/фондирования. Не выдумывайте ROI и риск-скор.

Проверка: две позиции каждого рынка, знак шорта, multiplier фьючерса, 0%/−3%/+3%, отдельные RUB/USD, ошибки JSON и откат загрузки. В синтетическом примере USD: капитал 10 000, объём 12 400, PnL 400, −3% = −372; RUB: капитал 1 000 000, объём 190 000, PnL 2 000, −3% = −5 700. Эти числа не должны появляться как результат реального API.

Пакет сохраняет опубликованный шаблон мастер-класса. Визуальный образец MTW2 доступен в https://human20.app/presentations/mtw2/slides.html#risk ; его демонстрационные ROI и 64/100 не являются рассчитанными метриками пользовательского счёта.
