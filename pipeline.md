# Работа pipeline
## build
Делится на build_front и build_back каждый из которых билдит dockerfile и пушит на dockerhub
## deploy
Подключается к Виртуальной машине пулит имейджи front и back, копирует туда dockercompose
## helthcheck
поверяет статус helth у api в docker compose