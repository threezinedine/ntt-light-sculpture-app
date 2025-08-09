# Light Sculpture Application

## Overview

The Light Sculpture Application is a specialized tool designed to assist users in creating 3D models optimized for shadow projection. By leveraging inverse design principles, the application generates 3D geometries such that, when illuminated from a specific direction, the resulting shadow forms a predefined, intriguing shape that is not intuitively derivable from the model's original form. This enables artists, designers, and engineers to craft optical illusions and artistic installations where shadows reveal hidden patterns, images, or messages.
The core functionality revolves around computational geometry and light simulation, allowing users to input desired shadow shapes and receive output 3D models ready for fabrication (e.g., via 3D printing).

## Features

-   [ ] **Inverse Shadow Design**: User starts with 2D image and create the 3D model with the help of this application.
-   [ ] **Simulation preview**: User can see the preview of the shadow projection.
-   [ ] **3D model export**: User can export the 3D model to a file.
-   [ ] **Multiple shadow projection**: User can create multiple shadow projections.

## Requirements

-   Python [3.11](https://www.python.org/downloads/) or higher
-   CMake [3.20](https://cmake.org/download/) or higher
-   Clang [18.1.1](https://github.com/llvm/llvm-project/releases/tag/llvmorg-18.1.1) or higher
-   Git [2.30](https://git-scm.com/downloads) or higher
-   [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/)

## Instalation

### Build from source

Firstly, ensure that you have `python` installed and be added to the `PATH` environment variable.

```bash
python --version # should be 3.11 or higher
```

After that, you can run `config.py` to setup and build the project.

```bash
python config.py config # to configure the project
python config.py run # to run the application
python config.py test all # to run all the tests (or autogen, engine, app for each subproject)
python config.py install # to install the application -> bin/LightSculpture.exe
```

## Examples

## Contributing

I welcome any contributions to the project. If you have any ideas, suggestions, or bug reports, please feel free to open an issue or submit a pull request.

Please feel free to contact me at [threezinedine@gmail.com](mailto:threezinedine@gmail.com)

## License

This project has no license - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, support, or collaboration, please feel free to contact me at [threezinedine@gmail.com](mailto:threezinedine@gmail.com)
