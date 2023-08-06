


# podman run --rm -ti --security-opt label=disable -v $HOME:$HOME -e HOME=$HOME --workdir=`pwd` greyrook/cde-deploy-k8s:master bash