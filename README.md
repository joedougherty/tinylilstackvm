tinylilstackvm
==============

A Python implementation of the VM described in Andrea Bergia's series [_Stack Based Virtual Machines_](https://andreabergia.com/stack-based-virtual-machines/).

This series is a great read on the topic -- _would highly recommend_!


Supported Instructions
======================

Please note:

**"TOS"** means "top of stack".

_a_, _b_, and _c_ refer to the three top-most items on the stack.

* _a_: the top-most item on the stack
* _b_: the item below _a_
* _c_: the item below _b_


| Instruction | Argument(s)         | Action                                                              |
| ----------- | ------------------- | ------------------------------------------------------------------- |
| `PUSH`      | _n_ (int)           | Pushes _n_ on TOS                                                   |   
| `POP`       | n/a                 | Pops the TOS                                                        |
| `DUP`       | n/a                 | Duplicates TOS and pushes on TOS                                    |
| `ROT`       | n/a                 | Rotates top 3 elements on stack  ( _a_ _b_ _c_ ) -> ( _b_ _c_ _a_ ) |
| `OVER`      | n/a                 | Copies the element below TOS and pushes on TOS                |
| `HALT`      | n/a                 | Stops the program                                             |     
| `NOT`       | n/a                 | Negates TOS                                                   |
| `AND`       | n/a                 | Pushes logical AND of _b_ and _a_ on TOS                      |
| `OR`        | n/a                 | Pushes logical OR of _b_ and _a_ on TOS                       |
| `ADD`       | n/a                 | Pushes _b_ + _a_ on TOS                                       |
| `SUB`       | n/a                 | Pushes _b_ - _a_ on TOS                                       |
| `MUL`       | n/a                 | Pushes _b_ * _a_ on TOS                                       |   
| `DIV`       | n/a                 | Pushes _b_ // _a_ on TOS                                      |
| `ISEQ`      | n/a                 | Pushes `True` on TOS if _b_ == _a_, else push `False` on TOS  |   
| `ISGE`      | n/a                 | Pushes `True` on TOS if _b_ >= _a_, else push `False` on TOS  |
| `ISGT`      | n/a                 | Pushes `True` on TOS if _b_ > _a_, else push `False` on TOS   |
| `ISLT`      | n/a                 | Pushes `True` on TOS if _b_ < _a_, else push `False` on TOS   |
| `ISLE`      | n/a                 | Pushes `True` on TOS if _b_ <= _a_, else push `False` on TOS  |
| `JMP`       | _loc_ (int)         | Unconditionally jumps to location _loc_                       |
| `JIF`       | _loc_ (int)         | Jumps to location _loc_ if TOS is `True`                      |
| `JNZ`       | _loc_ (int)         | Jumps to location _loc_ if TOS is `False`                     |
| `JGT`       | _loc_ (int)         | Jumps to location _loc_ if _b_ > _a_                          |
| `JGE`       | _loc_ (int)         | Jumps to location _loc_ if _b_ >= _a_                         |
| `JLT`       | _loc_ (int)         | Jumps to location _loc_ if _b_ < _a_                          |
| `JLE`       | _loc_ (int)         | Jumps to location _loc_ if _b_ <= _a_                         |                                 
| `STORE`     | _loc_ (int)         | Pop TOS and store in variable given by _loc_                  |
| `LOAD`      | _loc_ (int)         | Push variable given by _loc_ on TOS                           | 
| `CALL`      | _loc_ (int)         | Call function at _loc_                                        |
| `RET`       | n/a                 | Jump back to calling context after executing function         |


Example
=======


    # Countdown from 10 to 1
    PUSH 10
    JMP loopStart

    loopStart:
      DUP
      PUSH 1
      ISGT
      JNZ loopExit
      PUSH 1 
      SUB
      JMP loopStart

    loopExit:
      HALT


Tests
=====

You can run the tests with `pytest`.
