#!/usr/bin/env bash

ERR_MSG="Информация временно недоступна|Не определен ни один сервер"

case "$1" in
  "good")
    jq -c "select(.status==200 and (.body | test(\"$ERR_MSG\") | not))"
    ;;
  "bad")
    jq -c "select(.status!=200 or (.err != null) or (.body | test(\"$ERR_MSG\")))"
    ;;
esac
