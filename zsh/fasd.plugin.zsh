#default fasd plugin

if [ $commands[fasd] ]; then # check if fasd is installed
  fasd_cache="$HOME/.fasd-init-cache"
  if [ "$(command -v fasd)" -nt "$fasd_cache" -o ! -s "$fasd_cache" ]; then
    fasd --init auto >| "$fasd_cache"
  fi
  source "$fasd_cache"
  unset fasd_cache
  alias v='f -e vim'
  alias o='a -e open'

fi

#custom fasd functions
function goto {
        FILE=$(f $1 | head -n1)
        if [ -z "$FILE" ]; then
            echo "Nothing found"
        else
            echo $FILE 
            cd "`dirname $FILE`"
        fi
   }
