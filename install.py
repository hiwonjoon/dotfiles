#!/usr/bin/env python


################# BEGIN OF FIXME #################

# Task Definition
# (path of target symlink) : (location of source file in the repository)

tasks = {
    # SHELLS
    '~/.bashrc' : 'bashrc',
    '~/.screenrc' : 'screenrc',

    # VIM
    '~/.vimrc' : 'vim/vimrc',
    '~/.vim' : 'vim',
    '~/.vim/autoload/plug.vim' : 'vim/bundle/vim-plug/plug.vim',

    # NeoVIM
    '~/.config/nvim' : 'nvim',

    # GIT
    '~/.gitconfig' : 'git/gitconfig',
    '~/.gitignore' : 'git/gitignore',

    # ZSH
    '~/.zprezto'  : 'zsh/zprezto',
    '~/.zsh'      : 'zsh',
    '~/.zlogin'   : 'zsh/zlogin',
    '~/.zlogout'  : 'zsh/zlogout',
    '~/.zpreztorc': 'zsh/zpreztorc',
    '~/.zprofile' : 'zsh/zprofile',
    '~/.zshenv'   : 'zsh/zshenv',
    '~/.zshrc'    : 'zsh/zshrc',

    # Bins
    '~/.local/bin/fasd' : 'zsh/fasd/fasd',
    '~/.local/bin/imgcat' : 'bin/imgcat',
    '~/.local/bin/imgls' : 'bin/imgls',
    '~/.local/bin/fzf' : '~/.fzf/bin/fzf', # fzf is at $HOME/.fzf
    '~/.local/bin/tb' : 'bin/tb',

    # X
    '~/.Xmodmap' : 'Xmodmap',

    # GTK
    '~/.gtkrc-2.0' : 'gtkrc-2.0',

    # tmux
    '~/.tmux'     : 'tmux',
    '~/.tmux.conf' : 'tmux/tmux.conf',

    # .config
    '~/.config/terminator' : 'config/terminator',
    '~/.config/pudb/pudb.cfg' : 'config/pudb/pudb.cfg',

    # pip and python
    #'~/.pip/pip.conf' : 'pip/pip.conf',
    '~/.pythonrc.py' : 'pythonrc.py',
}

post_actions = [
    # Run vim-plug installation
    'vim +PlugInstall +qall',

    # Change default shell if possible
    r'''# Change default shell to zsh
    if [[ ! "$SHELL" = *zsh ]]; then
        echo -e '\033[0;33mPlease type your password if you wish to change the default shell to ZSH\e[m'
        chsh -s /bin/zsh && echo -e 'Successfully changed the default shell, please re-login'
    fi
    '''
]

################# END OF FIXME #################

def _wrap_colors(ansicode):
    return (lambda msg: ansicode + str(msg) + '\033[0m')
GRAY   = _wrap_colors("\033[0;37m")
WHITE  = _wrap_colors("\033[1;37m")
RED    = _wrap_colors("\033[0;31m")
GREEN  = _wrap_colors("\033[0;32m")
YELLOW = _wrap_colors("\033[0;33m")
BLUE   = _wrap_colors("\033[0;34m")


import os
import sys
import subprocess
from optparse import OptionParser
from sys import stderr

def log(msg, cr=True):
    stderr.write(msg)
    if cr:
        stderr.write('\n')

# command line arguments
def option():
    parser = OptionParser()
    parser.add_option("-f", "--force", action="store_true", default=False)
    (options, args) = parser.parse_args()
    return options

options = option()

# get current directory (absolute path) and options
current_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(current_dir)

# check if git submodules are loaded properly
stat = subprocess.check_output("git submodule status --recursive", shell=True)
submodule_missing = [l.split()[1] for l in stat.split('\n') if len(l) and l[0] == '-']

if submodule_missing:
    log(RED("git submodule %s does not exist!" % submodule_missing[0]))
    log(RED(" you may run: $ git submodule update --init --recursive"))

    log("")
    log(YELLOW("Do you want to update submodules? (y/n) "), cr=False)
    shall_we = (raw_input().lower() == 'y')
    if shall_we:
        subprocess.call('git submodule update --init --recursive', shell=True)
    else:
        log(RED("Aborted."))
        sys.exit(1)


for target, source in sorted(tasks.items()):
    # normalize paths
    source = os.path.join(current_dir, os.path.expanduser(source))
    target = os.path.expanduser(target)

    # bad entry if source does not exists...
    if not os.path.lexists(source):
        log(RED("source %s : does not exist" % source))
        continue

    # if --force option is given, delete and override the previous symlink
    if os.path.lexists(target):
        if options.force:
            if os.path.islink(target):
                os.unlink(target)
            else:
                log("{:50s} : {}".format(
                    BLUE(target),
                    YELLOW("already exists but not a symbolic link; --force option ignored")
                ))
        else:
            log("{:50s} : {}".format(
                BLUE(target),
                GRAY("already exists, skipped")
            ))

    # make a symbolic link if available
    if not os.path.lexists(target):
        try:
            mkdir_target = os.path.split(target)[0]
            os.makedirs(mkdir_target)
            log(GREEN('Created directory : %s' % mkdir_target))
        except:
            pass
        os.symlink(source, target)
        log("{:50s} : {}".format(
            BLUE(target),
            GREEN("symlink created from '%s'" % source)
        ))

for action in post_actions:
    print(WHITE('Executing : ') + action.strip().split('\n')[0])
    subprocess.call(['bash', '-c', action])
