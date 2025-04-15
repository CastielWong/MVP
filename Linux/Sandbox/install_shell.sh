#!/bin/bash
# # set proxy if needed
# export http_proxy="http://xxx:8080"
# export https_proxy="http://xxx:8080"
# export no_proxy="*.com,vdi*,sso.com*"

# =============================================================================
# ensure the proxy is reserved when using `sudo`
sudo -E apt-get update
# install zsh
echo y | sudo -E apt install zsh
# install font for theme going to use
echo y | sudo -E apt-get install fonts-powerline

# =============================================================================

# install oh-my-zsh for zsh configuration
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# -----------------------------------------------------------------------------
# add themes in oh-my-zsh
ZSH_CUSTOM=${ZSH_CUSTOM:-~/.oh-my-zsh/custom}
ZSH_THEMES=${ZSH_CUSTOM}/themes

download_theme() {
    local theme_name=$1
    local repo_url=$2

    proj_theme=${ZSH_THEMES}/${theme_name}
    if [[ ! -d "${proj_theme}" ]]; then
        echo "Downloading theme: '${theme_name}'"
        git clone --depth=1 "${repo_url}" "${proj_theme}" || echo "Failed to download '${theme_name}'"
    else
        echo "Theme '${theme_name}' is available already"
    fi
}

link_theme() {
    local theme_name=$1
    local name_linked=$2

    source_theme="${ZSH_THEMES}/${theme_name}/${name_linked}.zsh-theme"
    target_theme="${ZSH_THEMES}/${name_linked}.zsh-theme"
    if [[ ! -f ${target_theme} ]]; then
        echo "Linking to '${target_theme}'"
        ln -s "${source_theme}" "${target_theme}" || echo "Failed to link '${theme_name}'"
    else
        echo "'${target_theme}' was linked before"
    fi
}


themes=(
    # run `p10k configure` to configure
    "powerlevel10k https://github.com/romkatv/powerlevel10k.git"
    "spaceship-prompt https://github.com/spaceship-prompt/spaceship-prompt.git"
    "agnoster https://github.com/agnoster/agnoster-zsh-theme.git"
)


themes_to_link=(
    "spaceship-prompt spaceship"
    "agnoster agnoster"
)

for theme in "${themes[@]}"; do
    echo "--------------------------------------------------------------------"
    read -r theme_name repo_url <<< "${theme}"
    download_theme "${theme_name}" "${repo_url}"
done

for theme in "${themes_to_link[@]}"; do
    echo "--------------------------------------------------------------------"
    read -r theme_name name_linked <<< "${theme}"
    link_theme "${theme_name}" "${name_linked}"
done

# -----------------------------------------------------------------------------
# add plugins in oh-my-zsh
plugins=(
    "zsh-autosuggestions https://github.com/zsh-users/zsh-autosuggestions"
)

for plugin in "${plugins[@]}"; do
    echo "--------------------------------------------------------------------"
    read -r plugin_name repo_url <<< "${plugin}"

    plugin_folder=${ZSH_CUSTOM}/plugins/${plugin_name}
    if [[ ! -d ${plugin_folder} ]]; then
        echo "Downloading plugin '${target_theme}'"
        git clone "${repo_url}" "${plugin_folder}"
    else
        echo "Plugin '${plugin}' is available alread"
    fi
done
