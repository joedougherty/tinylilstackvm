tinylilstackvm
==============

A Python implementation of the VM described in Andrea Bergia's series [_Stack Based Virtual Machines_](https://andreabergia.com/stack-based-virtual-machines/).

This series is a great read on the topic -- _would highly recommend_!


Supported Instructions
======================

    | Instruction | Argument(s)         | Effects                                                   |
    | `PUSH`      | _n_ (int)           | Push _n_ on TOS                                           |   
    | `POP`       | n/a                 | Pops the TOS                                              |
    | `DUP`       | n/a                 | Duplicate TOS and push on TOS                             |
    | `HALT`      | n/a                 | Stops the program                                         |    
    | `NOT`       | n/a                 | Negates _b_ on TOS                                        |
    | `AND`       | n/a                 | Pushes logical AND of _a_ and _b_                         |
    | `OR`        | n/a                 | Pushes logical OR of _a_ and _b_                          |
    | `ADD`       | n/a                 | Pushes _b_ + _a_ on TOS                                   |
    | `SUB`       | n/a                 | Pushes _b_ - _a_ on TOS                                   |
    | `MUL`       | n/a                 | Pushes _b_ * _a_ on TOS                                   |   
    | `DIV`       | n/a                 | Pushes _b_ // _a_ on TOS                                  |
    | `ISEQ`      | n/a                 | Pushes True on TOS if _b_ == _a_, else push False on TOS  |   
    | `ISGE`      | n/a                 | Pushes True on TOS if _b_ >= _a_, else push False on TOS  |
    | `ISGT`      | n/a                 | Pushes True on TOS if _b_ > _a_, else push False on TOS   |
    | `JMP`       | _loc_ (int)         | Unconditionally jump to location _loc_                    |
    | `JIF`       | _loc_ (int)         | Jump to location _loc_ if TOS is TRUE                     |
    | `STORE`     | _loc_ (int)         | Pop TOS and store in variable given by _loc_              |
    | `LOAD`      | _loc_ (int)         | Push variable given by _loc_ on TOS                       | 
    | `CALL`      | _loc_ (int)         | Call function at _loc_                                    |
    | `RET`       | n/a                 | Jump back to calling context after executing function     |



Tests
=====

You can run the tests with `pytest`.
