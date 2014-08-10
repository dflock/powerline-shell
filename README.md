A Powerline style prompt for your shell
=======================================

__This was originally forked from [milkbikis powerline-shell](https://github.com/milkbikis/powerline-shell)__

A [Powerline](https://github.com/Lokaltog/vim-powerline) like prompt for Bash, ZSH and Fish:

*  Shows some important details about the git/svn/hg/fossil branch:
    *  Displays the current branch which changes background color when the branch is dirty
    *  VCS specific symbols are used to indicate other status info (e.g.: pending stashes, ahead/behind origin, etc...)
    *  The git segment is the most mature, but the others should at least get you basic info
*  Changes color if the last command exited with a failure code
*  If you're too deep into a directory tree, shortens the displayed path with an ellipsis
*  Shows current battery status on Linux laptops (or Windows under Cygwin)
*  Shows the current Python [virtualenv](http://www.virtualenv.org/) environment
*  Support for Python 2.5+
*  It's easy to customize and extend. See below for details.

# Setup

This script uses ANSI color codes (256 color mode) to display colors in a terminal. These are notoriously non-portable, so may not work for you out of the box, but try setting your $TERM to `xterm-256color`, because that works for me. In order to get all the symbols working correctly, you will have to do the following:

* Clone this repository somewhere:

        git clone https://github.com/qwindelzorf/powerline-shell

* Copy `config.py.dist` to `config.py` and edit it to configure the segments you want. Then run

        ./install.py

  * This will generate `powerline-shell.py`

* (optional) Create a symlink to this python script in your home:

        ln -s <path/to/powerline-shell.py> ~/powerline-shell.py

  * If you don't want the symlink, just copy it somewhere convenient and modify the path in the commands below
  * If you want to get _really_ fancy, you can run the output powerline-shell.py file through [pyinstller](http://www.pyinstaller.org/), which will get you a single binary exe that should be independant of the system python.

            ./install.py
            pyinstaller -F powerline-shell.py
            cp ./dist/powerline-shell ~/bin/

* Patch the font you use for your terminal: see `https://github.com/Lokaltog/powerline-fonts`
  * The `powerline-fonts` repo is included inside this one as a submodule in the `fonts` folder, but is not actually pulled down to your computer by default. Assuming you have already cloned this repo, and are inside it, the fonts can be pulled with:

            git submodule init
            git sumbodule update

  * For Cygwin, just download one of the already patched fonts and set your terminal to use it.
  * If you struggle too much to get working fonts in your terminal, you can use "compatible" mode, which uses only standard unicode characters
  * If "compatible" mode causes you trouble too, you can use "flat" mode, which uses only standard ASCII characters.

### All Shells:
There are a few optional arguments which can be seen by running `powerline-shell.py --help`.

```
  --cwd-only            Only show the current directory
  --cwd-max-depth CWD_MAX_DEPTH
                        Maximum number of directories to show in path
  --colorize-hostname   Colorize the hostname based on a hash of itself.
  --mode {patched,compatible,flat}
                        The characters used to make separators between
                        segments. Patched works with the powerline fonts,
                        compatible uses standard unicode characters, and
                        flat does nothing for symbols, just colorization
```

### Bash:
Add the following to your `.bashrc`:

        function _update_ps1() {
           export PS1="$(~/powerline-shell.py $? 2> /dev/null)"
        }

        export PROMPT_COMMAND="_update_ps1; $PROMPT_COMMAND"

### ZSH:
Add the following to your `.zshrc`:

        function powerline_precmd() {
          export PS1="$(~/powerline-shell.py $? --shell zsh 2> /dev/null)"
        }

        function install_powerline_precmd() {
          for s in "${precmd_functions[@]}"; do
            if [ "$s" = "powerline_precmd" ]; then
              return
            fi
          done
          precmd_functions+=(powerline_precmd)
        }

        install_powerline_precmd

### Fish:
Redefine `fish_prompt` in ~/.config/fish/config.fish:

        function fish_prompt
            ~/powerline-shell.py $status --shell bare ^/dev/null
        end

# Customization

### Adding, Removing and Re-arranging segments

The `config.py` file defines which segments are drawn and in which order. Simply comment out and rearrange segment names to get your desired arrangement. Every time you change `config.py`, run `install.py`, which will generate a new `powerline-shell.py` customized to your configuration. If you symlinked the built file, you should see the new prompt immediately. Otherwise, copy it over your existing `powerline-shell.py`, and you should be good to go.

### Right-aligned segments
Right-aligned segments are kind of a hack right now, so be warned. If you have trouble with them, please open a ticket and let me know what's not working. To set up right-aligned segments, just add them to the `RIGHT_SEGMENTS` list in `config.py` and do the normal build.

Current limitations:
* They seem to work (in bash at least), but only if you are running a multi-line prompt (at least one `newline` segment).
* If your left and right segments begin to collide, left segments will overwrite right segments
* Old lines do not get moved left/right if the terminal is resized
* Probably lots of other stuff too.

### Contributing new types of segments

The `segments` directory contains python scripts which are injected as is into a single file `powerline-shell.py.template`. Each segment script defines a function that inserts one or more segments into the prompt. If you want to add a new segment, simply create a new file in the segments directory and add its name to the `config.py` file at the appropriate location.

Make sure that your script does not introduce new globals which might conflict with other scripts. Your script should fail silently and run quickly in any scenario. Custom segments should be completely stand alone, not requiring any other files or non-standard packages. Additionally, for maximum compatibility, your segment should provide all its own imports at the top of the file, rather than relying on imports made by other segments.

Make sure you introduce new default colors in `themes/default.py` for every new segment you create. Test your segment with this theme first.

### Themes

The `themes` directory stores themes for your prompt, which are basically color values used by segments. The `default.py` defines a default theme which can be used standalone, and every other theme falls back to it if they miss colors for any segments. Create new themes by copying any other existing theme and changing the values. To use a theme, set the `THEME` variable in `config.py` to the name of your theme.

A script for testing color combinations is provided at `themes/colortest.py`. Note that the colors you see may vary depending on your terminal. When designing a theme, please test your theme on multiple terminals, especially with default settings.
