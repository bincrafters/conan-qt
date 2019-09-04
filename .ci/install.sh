#!/usr/bin/env bash

set -ex

if [[ "$(uname -s)" == 'Darwin' ]]; then
    unset PYENV_ROOT
    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
    export PATH="$HOME/.pyenv/bin:$PATH"

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

    pyenv install 3.7.1
    pyenv virtualenv 3.7.1 conan
    pyenv rehash
    pyenv activate conan

    pip install cmake --upgrade
else
    export PATH="$HOME/.local/bin:$PATH"
fi

pip install wheel
pip install conan --upgrade
pip install conan_package_tools bincrafters_package_tools

conan user

pip install requests spdx-lookup
conan config install https://github.com/conan-io/hooks.git -sf hooks -tf hooks
conan config set hooks.conan-center
conan config set hooks.attribute_checker
if [[ "$(uname -s)" == 'Linux' ]]; then
  conan config set hooks.binary_linter
fi
conan config set hooks.bintray_updater
conan config set hooks.github_updater
conan config set hooks.spdx_checker
