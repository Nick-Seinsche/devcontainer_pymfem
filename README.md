MFEM Development Environment in a Dev Container
===

This repository provides a development environment for working with MFEM outside of a linux environment (e.g. Windows) by using a Docker Dev Container and Visual Studio Code. This environment comes preconfigured with PyMfem and necessary tools for running an visualizing calculations and results respecively.

Skills/learnings: - Docker - MFEM - DevOps

Features
---

- Write your solutions to a file and interact with them on your host machine.
- Download GLVIS on your host machine to send solutions inside the devcontainer
 to the GLVIS server on your host machine.

Requirements
---

- Docker: Make sure Docker is installed.
- Visual Studio Code: Install VS Code and the Remote - Containers extension
- Opzional: Have GLVIS installed on the host machine and server running (port 19916 by default)

How to get Started
---

- Make sure the ports are mapped correctly. The port GLVIS listens to should be the same
as the port in the projects/demo_project/main.NET_CONF
- Run and start developing!

