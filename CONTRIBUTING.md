# Get test coverage

    py.test \
    --tx socket=192.168.178.87:9999 \
    --pep8 \
    --spec \
    --instafail \
    --cov=gameprices \
    --cov-report html \
    gameprices/test

Enable paralell tests

    -n 8
