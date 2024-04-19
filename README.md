# CPP-RV-Tool
For CS 6156: Runtime Verification final project.

## Description of Example Specs

### Locks
This example is about Lock objects which can be acquired and released.
Lock objects are used by procedures in the LockUser class.

Specification: If LockUser acquires a lock in a procedure, it must be released in the procedure.

The ERE (good behavior) is (begin (acquire+ release+ | release*)* end)*

The executable supports 3 scenarios:
1. A non-violating trace
2. A violating trace which is detected by non-parametric monitoring
3. A violating trace which requires parameterization to detect

### Cars
This example is about Persons who drive Cars. 

Specification: A Car can only drive if a Person has entered as a driver.

The ERE (good behavior) is createCar (driverEnter | driverExit)* (driverEnter) drive*

The executable supports 3 scenarios:
1. A non-violating trace
2. A violating trace which is detected by non-parametric monitoring
3. A violating trace which requires parameterization to detect

## Usage

Run on Cornell's ugclinux machines.

### Running the Locks example

```
cd mytool/examples/Locks 
```

To run the normal version of the program (replace SCENARIO# with 1, 2, or 3):
```
make normal
src/main [SCENARIO#]
```

To run the monitored version of the program:
```
make withrv
rv/main-instrumented-Spec1 [SCENARIO#]
```

You should see that a spec violation is detected for Scenario 2 but not 3, because currently only non-parametric monitoring is supported.

### Running the Cars example

```
cd mytool/examples/Cars
```

The instructions are now the essentially the same as for Locks.

To run the normal version of the program (replace SCENARIO# with 1, 2, or 3):
```
make normal
src/main [SCENARIO#]
```

To run the monitored version of the program:
```
make withrv
rv/main-instrumented-Spec1 [SCENARIO#]
```

You should see that a spec violation is detected for Scenario 2 but not 3, because currently only non-parametric monitoring is supported.

