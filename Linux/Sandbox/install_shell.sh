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

# theme: powerlevel10k
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k
# # MANUAL STEP: config the theme
# p10k configure

# theme: spaceship
git clone --depth=1 https://github.com/spaceship-prompt/spaceship-prompt.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/spaceship-prompt
ln -s "${ZSH_CUSTOM}/themes/spaceship-prompt/spaceship.zsh-theme" "${ZSH_CUSTOM}/themes/spaceship.zsh-theme"

# theme: agnoster
git clone --depth=1 https://github.com/agnoster/agnoster-zsh-theme.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/agnoster
ln -s "${ZSH_CUSTOM}/themes/agnoster/agnoster.zsh-theme" "${ZSH_CUSTOM}/themes/agnoster.zsh-theme"

# -----------------------------------------------------------------------------
# add plugins in oh-my-zsh
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
