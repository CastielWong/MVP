#!/bin/bash

usage() {
    echo "Usage: $0 {local|DEV|UAT|PRD}"
    exit 1
}

environment=$1
if [ -z "${environment}" ]; then
    usage
fi

case "${environment}" in
    local)
        export CHECK_USER=local
        export CHECK_PWD=local
        ;;
    DEV)
        export CHECK_USER=dev
        export CHECK_PWD=
        ;;
    UAT)
        export CHECK_USER=uat
        export CHECK_PWD=
        ;;
    PRD)
        export CHECK_USER=prd
        export CHECK_PWD=
        ;;
    *)
        usage
        ;;
esac

echo "Environment switched to: ${environment}"

echo ${CHECK_USER}
