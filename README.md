# Clockify Neovim plugin

Based on [this template](https://github.com/jacobsimpson/nvim-example-python-plugin).

Only works on Neovim. Don't know the version you need but try to have the last one.

## Installing

_TODO_, but should be a normal plugin installation. 
Probably a `Plug 'tarasyarema/vim-clockify'` should work just fine.

## Developing

In a separate terminal, go to the root of this folder and run this command `nvim --cmd "set rtp+=$(pwd)"`. 
This will append the current tree to the runtime path of Neovim and will be able to run the plugin.

If there's some problem try running this from Neovim: `:UpdateRemotePlugins`.

You can setup via the `ClockifyKey` command (see below) or you may need to create an env file `.env` in the root directory with the following format
```env
CLOCKIFY_API_URL="https://api.clockify.me/api/v1"
CLOCKIFY_API_KEY="{your_clockify_api_key}"
```
Note that the url is not hardcoded, as it may (or not) change in the future.
You can also set them as env variables of your system so there would be no need to setup the env file.

## Clockify

_TODO_

### Commands

- `:ClockifyKey {clockify_api_key}` setups your Clockify API key.
- `:Clockify`: for the moment it's just a greeting window :3
