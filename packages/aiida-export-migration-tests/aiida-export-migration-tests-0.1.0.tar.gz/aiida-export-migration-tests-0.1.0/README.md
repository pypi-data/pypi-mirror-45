# Testing of AiiDA export file migrations

Test modules for migration of [AiiDA](http://www.aiida.net) export files.

Can be installed by adding `testing` package, when installing AiiDA:

```shell
pip install aiida-core[testing]
```

> **Note**: This only works for AiiDA *v1.0.0* and newer.

Historical table of version comparisons between releases of this module and AiiDA,
including when tests for the different export versions are first included.

| This module | AiiDA | Export versions (when first included) |
| ----------- | ----- | ------------------------------------- |
| 0.1.0 | [1.0.0](https://github.com/aiidateam/aiida_core/releases/tag/v1.0.0) | 0.1 -> 0.2 ; 0.2 -> 0.3 ; 0.3 -> 0.4 |

## Q&A

**Q: Why not include these tests in the core of AiiDA?**  
**A:** These tests demand fixed AiiDA export files.
In order to not take up unneccesary disk space, when installing AiiDA,
these tests have been separated out of [aiida-core](https://github.com/aiidateam/aiida_core).
Furthermore, the legacy export versions will never change,
i.e. the incremental migration functions need only be thoroughly tested once,
and will therefore not be affected by changes to the core of the AiiDA code in any way.

**Q: What happens when the export version is upped?**  
**A:** A new export file will be added to this repo as well as a new test-filled file.

**Q: What if the import system changes in AiiDA core?**  
**A:** Tests relying on importing exported files into the AiiDA database
will still be found in [aiida-core](https://github.com/aiidateam/aiida_core).
This repo is only for testing the incremental migration functions for different export versions.

## Release notes

### 0.1.0 (April 2019)

**AiiDA version**: _1.0.0_

First release.

Tests for step-wise export migrations from versions 0.1, 0.2, and 0.3.  
Representative export files created in specialized
[Quantum Mobile](https://materialscloud.org/work/quantum-mobile)
virtual machines by @yakutovicha to test currently known migrations
from the basis of what could be exported at the time of the different export versions.

Table of version comparisons
(similar to the one in [aiida-core](https://github.com/aiidateam/aiida_core)
PR [#2478](https://github.com/aiidateam/aiida_core/pull/2478)).

| Export version | AiiDA version | AiiDA version release date | Found changed in commit |
| -------------- | ------------- | -------------------------- | ----------------------- |
| ~~v0.1~~* | ~~0.6.0.1~~ | ~~01.03.2016~~ | ~~as exported by 0.6.0~~ |
| v0.2 | 0.9.1 | 01.09.2017 | [189e29fea4c7f4213d0be0914d55cccaa581c364](https://github.com/aiidateam/aiida_core/commit/189e29fea4c7f4213d0be0914d55cccaa581c364) (v0.7.0) |
| v0.3 | 0.12.3 | 04.03.2019 | [788d3206e0eaaf062d1a13710aaa64a18a0bbbcd](https://github.com/aiidateam/aiida_core/commit/788d3206e0eaaf062d1a13710aaa64a18a0bbbcd) (v0.10.0rc1) |
| v0.4 | 1.0.0b2 | 09.04.2019 | [1673ec28e8b594693a0ee4cdec82669e72abcc4c](https://github.com/aiidateam/aiida_core/commit/1673ec28e8b594693a0ee4cdec82669e72abcc4c) (v1.0.0b1) |

\*Due to the following reasons, we decided **not** to invest an effort in making
the representative archive migration for 0.1:

1. The earliest version released on PyPi is 0.8.0rc1 (22.03.2017).
1. The previous stable version (AiiDA 0.5.0) was not working in a virtual environment.
1. The migration from v0.1 to v0.2 is small and quite simple.
   If an export file should be found that cannot be properly migrated, due to this step,
   it can be migrated manually with little effort.

## Representative export files creation

To create the representative export files, a simple workflow was developed by @yakutovicha
that runs two consequtive [QuantumESPRESSO](https://www.quantum-espresso.org) PW calculations.
First an SCF calculation, followed by an MD calculation.

The workflows can be found in the repository's folder `.qm`,
and correspond to the following export versions and
[Quantum Mobile](https://github.com/marvel-nccr/quantum-mobile/releases/) editions:

| Export version | Workflow | Run workflow script | Quantum Mobile |
| -------------- | -------- | ------------------- | -------------- |
| ~~v0.1~~* | - | - | - |
| v0.2 | [wf.py](.qm/wf.py) | [run_wf.py](.qm/run_wf.py) | [historical_aiida_0.9.1](https://github.com/marvel-nccr/quantum-mobile/tree/historical_aiida_0.9.1) |
| v0.3 | [wf.py](.qm/wf.py) | [run_wf.py](.qm/run_wf.py) | [v19.03.0](https://github.com/marvel-nccr/quantum-mobile/releases/tag/19.03.0) |
| v0.4 | [wf_aiida_1.0.py](.qm/wf_aiida_1.0.py) | [run_wf_aiida_1.0.py](.qm/run_wf_aiida_1.0.py) | _in development_ |

\*See section _Release notes#0.1.0 (April 2019)_.

They contain the following AiiDA node types (according to AiiDA **1.0.0**):

| Node type | Parent-type tree, up to `Node` |
| --------- | -------- |
| Float | NumericType -> BaseType/Data -> Node |
| Int | NumericType -> BaseType/Data -> Node |
| Dict | Data -> Node |
| FolderData | Data -> Node |
| RemoteData | Data -> Node |
| StructureData | Data -> Node |
| UpfData | SinglefileData -> Data -> Node |
| KpointsData | ArrayData -> Data -> Node |
| BandsData | KpointsData -> ArrayData -> Data -> Node |
| TrajectoryData | ArrayData -> Data -> Node |
| Code | Data -> Node |
| WorkChainNode | WorkflowNode -> ProcessNode -> Node |
| CalcJobNode | CalculationNode -> ProcessNode -> Node |
