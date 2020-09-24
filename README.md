# TLView

## Overview

TLView is a program that provides descriptions of all TCP and UDP endpoints on a host, including local and remote addresses and the status of TCP connections.

![overview](https://user-images.githubusercontent.com/88273034/215495687-b2fd7f12-9d46-4986-8157-d72cab346d41.png)

## Requirements

- Windows
- Python `~3.7.4`
- Pip `^19.0.3`

## Installation

```bash
git clone https://github.com/itfray/TLView.git
cd ./TLView
python -m pip install -r requirements.txt
```

## Launch

```bash
python main.py
```

## Usage

* ### Display of all current TCP, UDP, TCP6, UDP6 connections

    All <span style="color:green">**new**</span> connections are colored <span style="color:green">**green**</span>. All compounds that <span style="color:red">**disappear**</span> are colored <span style="color:red">**red**</span>. The data line where the data has been <span style="color:yellow">**updated**</span> is colored <span style="color:yellow">**yellow**</span>.
    
    To sort a table by a specific column, the user needs to click on the corresponding table column headings.
    The sort indicator is the arrow `⯅/⯆`, which is signed next to the sorted column.

    ![Display feature](https://user-images.githubusercontent.com/88273034/215495977-210ec979-59d1-487e-9a0d-50ddb01cd65c.gif)

    Using the `View > Update Speed` menu, you can adjust how often the table is updated.

    ![Update rate change feature](https://user-images.githubusercontent.com/88273034/215496042-0ddf2f43-6b79-48e5-bfc5-cbca911e1867.png)

* ### Domain and service name resolution

    If `Options > Resolve Addresses` option is activated, all connection addresses are displayed in the form domain names. Otherwise, all addresses are displayed in the form IPv4/IPv6.

    ![Resolve domain name feature](https://user-images.githubusercontent.com/88273034/215496025-6926f761-cd52-4789-9324-a119c0c579a5.png)

* ### Save the current state of network connections to a file

    `File > Save` allows you to save the current state of the connection table in a text file in `CSV` format.

    ![Save file feature](https://user-images.githubusercontent.com/88273034/215496030-f62ea272-5d4c-4e85-81d2-b9e0dd351fcb.png)

* ### Terminate a process by specified connection

    You need to select the connection by clicking the left mouse button and open the context menu by clicking the right mouse button. To terminate the process, select the `End Process...` menu item and click `Yes`.

    ![Terminate process feature](https://user-images.githubusercontent.com/88273034/215496045-5ba1ebac-a611-4e64-a8af-fbf237490294.png)

## License

MIT. See [LICENSE](LICENSE).