whspchars = "\t\n "
nonwhite = bytearray(set(range(0x00, 0x100)) - {9, 10, 32})
"""http://compsoc.dur.ac.uk/whitespace/tutorial.html
Whitespace tutorial

The only lexical tokens in the whitespace language are Space (ASCII 32), Tab (ASCII 9) and Line Feed (ASCII 10).
By only allowing line feed as a token, CR/LF problems are avoided across DOS/Unix file conversions.
(Um, not sure. Maybe we'll sort this in a later version.).

The language itself is an imperative, stack based language.
Each command consists of a series of tokens, beginning with the Instruction Modification Parameter (IMP).
These are listed in the table below."""
IMP = {}
IMP[" "] = "Stack_Manipulation"
IMP["\t "] = "Arithmetic"
IMP["\t\t"] = "Heap_access"
IMP["\n"] = "Flow_Control"
IMP["\t\n"] = "I/O"
"""The virtual machine on which programs run has a stack and a heap.
The programmer is free to push arbitrary width integers onto the stack (only integers, currently there is no implementation of floating point or real numbers).
The heap can also be accessed by the user as a permanent store of variables and data structures.

Many commands require numbers or labels as parameters.
Numbers can be any number of bits wide, and are simply represented as a series of [Space] and [Tab], terminated by a [LF].
[Space] represents the binary digit 0, [Tab] represents 1.
The sign of a number is given by its first character, [Space] for positive and [Tab] for negative.
Note that this is not twos complement, it just indicates a sign.

Labels are simply [LF] terminated lists of spaces and tabs. There is only one global namespace so all labels must be unique."""
########################################################################################################################################################################################################################
"""Stack Manipulation (IMP: [Space])

Stack manipulation is one of the more common operations, hence the shortness of the IMP [Space]. There are four stack instructions."""
SM = {}
SM[" "] = "Push the number onto the stack - Parameters Number"
SM["\n "] = "Duplicate the top item on the stack"
SM["\n\t"] = "Swap the top two items on the stack"
SM["\n\n"] = "Discard the top item on the stack"