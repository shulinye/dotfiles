alias yolo="sudo"
alias :q=exit
alias wq="exit"

alias j="fasd_cd -d"
function mkdate()
{
    currentdate=`date +%F`
    if [ ! -d $currentdate ]; then
        mkdir $currentdate
    fi
    cd $currentdate
}
