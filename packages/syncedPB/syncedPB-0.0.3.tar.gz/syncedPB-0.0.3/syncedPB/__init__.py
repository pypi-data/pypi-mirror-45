from time import time as timmer
import sys
import os
from IPython.display import display, Javascript

def _genStr(it, total, eta, time_it, beginning_time, length_bar=20):
    outstr = str(it)+'/'+str(total)+'  ['
    perc_it = it/total * length_bar

    for i in range(length_bar):
        if i < perc_it:
            outstr = outstr + chr(9608)
        else:
            outstr = outstr + ' '
    outstr = outstr + '] \t\t '

    min_eta = round(eta//60)
    sec_eta = round(eta - 60 * min_eta)

    if min_eta > 1:
        outstr = outstr+'\t eta: '+str(min_eta)+' mins  and  '+str(sec_eta)+' secs'
    elif min_eta == 1:
        outstr = outstr+'\t eta: '+str(min_eta)+' min  and  '+str(sec_eta)+' secs'
    else:
        outstr = outstr+'\t eta: '+str(sec_eta)+' secs'
        
    outstr = outstr+'\t ('+str(round(time_it,6))+' secs/it)'
    
    elapsed = round(timmer() - beginning_time)
    min_elap = round(elapsed//60)
    sec_elap = round(elapsed - 60 * min_elap)
    
    if min_eta > 1:
        outstr = outstr+'\t elapsed: '+str(min_elap)+' mins  and  '+str(sec_elap)+' secs'
    elif min_eta == 1:
        outstr = outstr+'\t elapsed: '+str(min_elap)+' min  and  '+str(sec_elap)+' secs'
    else:
        outstr = outstr+'\t elapsed: '+str(sec_elap)+' secs'

    return outstr
    
def _ema(x, mu, alpha=0.8):
    return (alpha * x) + (1 - alpha) * mu

def foo():
    
    js = """

    require(
        ["base/js/dialog"], 
        function(dialog) {
            dialog.modal({
                title: 'Completed !',
                body: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam pretium nulla at nisl hendrerit, sit amet facilisis erat ultrices. Integer ac mauris eget sem egestas tempus sit amet a neque. In nec gravida arcu. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque non velit eu lectus feugiat gravida. Duis vitae dui non quam bibendum bibendum eget eu orci. Sed eget dui sed sapien mattis tempus id in nisl. Duis sagittis lectus ante. Praesent id imperdiet ipsum. Ut nec fermentum ante. Donec nec tortor lorem. Quisque condimentum sapien eget lacus varius, id mattis mauris molestie. Curabitur pharetra feugiat sem, eget faucibus tortor rutrum nec.',
            });
        }
    );

    """

    display(Javascript(js))

class syncedPB():
    def __init__(self, target, file=sys.stderr, popup=False):
        self.__popup = popup
        self.__file = file
        self.__target = target
        self.__tick = timmer()
        self.__it = 0
        self.__time_it = 0
        self.__beginning_of_time = timmer()
        self.__alpha_init = 1.0 
        self.__update_iters = max( 1, int(0.05*len(self)) )
    
    def __len__(self):
        return len(self.__target)

    def __getitem__(self, i):
        
        self.__time_it = _ema(timmer() - self.__tick, self.__time_it, max(0.3, self.__alpha_init/(1+0.1*self.__it)  ))
        
        eta = int((len(self) - self.__it)*self.__time_it)
        
        if self.__it % self.__update_iters == 0:
            print(_genStr(self.__it, len(self), eta, self.__time_it, self.__beginning_of_time), file=self.__file, end='\r')
        
        self.__tick = timmer()
        self.__it += 1
        
        if i == len(self)-1 and self.__popup:
            foo()
        
        return self.__target[i]
