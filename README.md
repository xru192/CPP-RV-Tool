# CPP-RV-Tool
For CS 6156: Runtime Verification final project.

## Description of Example Specs

### Locks
This example is about `Lock` objects which can be acquired and released.
`Lock` objects are used by procedures in the `LockUser` class.

Specification: If LockUser acquires a lock in a procedure, it must be released in the procedure.

The ERE (good behavior) is 

`(begin (acquire+ release+ | release*)* end)*`

The executable supports 3 scenarios:
1. A non-violating trace
2. A violating trace which is detected by non-parametric monitoring
3. A violating trace which requires parameterization to detect

### Cars
This example is about `Person`s who drive `Car`s. 

Specification: A car can only drive if a person has entered as a driver.

The ERE (bad behavior) is 

`createCar (epsilon | ((driverEnter | driverExit)* driverExit)) drive`

The executable supports 3 scenarios:
1. A non-violating trace
2. A violating trace which is detected by non-parametric monitoring
3. A violating trace which requires parameterization to detect

### CarsBridges
This example extends the previous, with `Person`s who drive `Car`s on `OneLaneBridge`s.

Specification: No person may drive on the same bridge in the same car twice.

The ERE (bad behavior) is 

`(enterCar | exitCar)* enterCar takeBridge exitBridge (((enterCar | exitCar)* enterCar) | epsilon) takeBridge`

The executable supports 3 scenarios:
1. A non-violating trace
2. A violating trace which is detected by non-parametric monitoring
3. A violating trace which requires parameterization to detect

## Usage

Run on Cornell's ugclinux machines.

### Setup

Prior to running, you may need to grant execution permission for the binaries.

```bash
cd mytool/bin
chmod u+x *
```

### Running the Locks example

```bash
cd mytool/examples/Locks 
```

To run the normal version of the program (replace SCENARIO with 1, 2, or 3):
```bash
make normal
src/main SCENARIO
```

To run the version of the program with non-parametric monitoring:
```bash
make withrv
rv/main-instrumented-Spec1 SCENARIO
```

You should see that a spec violation is detected for Scenario 2 but not 3, because non-parametric monitoring is used here.

To run the version of the program with parametric monitoring:
```bash
make withprv
rv/main-instrumented-Spec1 SCENARIO
```

You should see that a spec violation is detected for Scenario 2 and 3.

### Running the Cars example

```bash
cd mytool/examples/Cars
```

The instructions are now the essentially the same as for Locks.

To run the normal version of the program (replace SCENARIO with 1, 2, or 3):
```bash
make normal
src/main SCENARIO
```

To run the version of the program with non-parametric monitoring:
```bash
make withrv
rv/main-instrumented-Spec1 SCENARIO
```

You should see that a spec violation is detected for Scenario 2 but not 3, because non-parametric monitoring is used here.

To run the version of the program with parametric monitoring:
```bash
make withprv
rv/main-instrumented-Spec1 SCENARIO
```

You should see that a spec violation is detected for Scenario 2 and 3.

### Running the CarsBridges example

```bash
cd mytool/examples/CarsBridges
```

Same as above.
