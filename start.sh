#!/bin/bash
# Docker　Container起動
docker run -itd -p 10022:10022 --name cargoview_test cargoview_test sh /init.sh
