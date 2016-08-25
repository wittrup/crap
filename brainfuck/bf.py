"""Brainfuck in One Line of Python

A question that has bugged me for a while is whether or not it is possible to simulate a Turing Machine in one semicolon-free expression of Python.
If you allow for liberal use of eval then the answer is (trivially) positive, but it's not directly obvious that it would be true without such workarounds.
Python's lack of tail-call elimination makes its lambda calculus bounded in scope, as the user is bound to quickly hit the recursion limit1.
Thus, it wasn't a priori obvious (to me at least) that a TM can be simulated using only the tools provided by Python's standard library, minus eval (and equivalent "cheats", such as exec, system calls, etc).

As luck would have it, my university held a code-obfuscation night one Friday, where the goal was to attempt writing obfuscated code (and, apparently, play scrabble and break into each other's voicemails).
I took this opportunity to write the following brainfuck interpreter, settling the question once and for all:
"""
(lambda t:(lambda a:(lambda b:(lambda l,e,s:((lambda(Y,o,N,A,t),a,n:e('v',(Y,o,N,A,t))or[e('v',(lambda(Y,o,N,A,t):({'>':(lambda(Y,o,N,A,t),a,n:(Y,o,N+1,A+1,t)),'<':(lambda(Y,o,N,A,t),a,n:(Y,o,N-1,A+1,t)),'+':(lambda(Y,o,N,A,t),a,n:((Y[:N]+[Y[N]+1]+Y[N+1:],o,N,A+1,t)if N>=0 else(Y,o[:-N-1]+[o[-N-1]+1]+o[-N:],N,A+1,t))),'-':(lambda(Y,o,N,A,t),a,n:((Y[:N]+[Y[N]-1]+Y[N+1:],o,N,A+1,t)if N>=0 else(Y,o[:-N-1]+[o[-N-1]-1]+o[-N:],N,A+1,t))),'.':(lambda(Y,o,N,A,t),a,n:__import__('sys').stdout.write(chr(Y[N] if N>=0 else o[-N-1]))or(Y,o,N,A+1,t)),',':(lambda(Y,o,N,A,t),a,n:(Y[:N]+[ord(t[0])if len(t)else -1]+Y[N+1:]if A>=0 else Y,o[:-N-1]+[ord(t[0])if len(t)else -1]+o[-N:]if A<0 else o,N,A+1,t[1:])),'[':(lambda(Y,o,N,A,t),a,n:(Y,o,N,n[A]+1 if(Y[N]==0 if N>=0 else o[-N-1]==0)else A+1,t)),']':(lambda(Y,o,N,A,t),a,n:(Y,o,N,n[A]+1 if(Y[N]>=1 if N>=0 else o[-N-1]>=1)else A+1,t))}[a[A]]((Y+[0]*(9+len(Y)) if A>=len(Y)-5 else Y,o+[0]*(9+len(o)) if -A>=len(o)-5 else o,N,A,t),a,n)if A<len(a)else False))(l('v')))for i in s.takewhile(lambda x:l('v')!=False,s.count())])(([],[],0,0,t),a,dict(e('g',[])or e('l',[])or[e('l',l('l')+[i])if a[i]=='['else(e('g',l('g')+[(l('l')[-1],i),(i,l('l')[-1])])or e('l',l('l')[:-1]))for i in range(len(a))if a[i] in'[]'][:0]or l('g'))))[:0])(b.__getattribute__,b.__setattr__,__import__('itertools')))(lambda:a)or None)(filter("<.+[,->]".count,open(__import__('sys').argv[1]).read())))(raw_input())
"""
To use this, simply save the above code as, say, bf.py and execute $ python bf.py blah.bf from the terminal.
If you have no clue what you're doing in brainfuck (I sure don't), Wikipedia has some amusing code for calculating the rot13 of an input string (which this interpreter will take on stdin).

To be perfectly honest, I don't completely remember every detail of how the above code works, but I can figure it out and put an explanation here given sufficient demand.

Here's to bad code!

-Yonatan
One could argue that the stack can be extended indefinitely by using sys.setrecursionlimit which is completely true,
but stack space just feels a whole lot more "finite" than does the heap, particularly when you allow for virtual memory usage.
Of course, if you're being completely technical, you can't parse any non-regular language on any given computer.
However, when has that ever stopped us from pretending we can?"""