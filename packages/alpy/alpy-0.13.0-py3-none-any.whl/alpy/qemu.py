# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib
import logging
import pathlib
import shutil
import subprocess

from qmp import QEMUMonitorProtocol

import alpy.console
import alpy.utils

QMP_SOCKET_FILENAME = "qmp.sock"
OVMF_VARS_COPY_FILENAME = "OVMF_VARS.fd"


@contextlib.contextmanager
def run(qemu_args, timeout):
    log = alpy.utils.context_logger(__name__)
    logger = logging.getLogger(__name__)
    with log("Initialize QMP monitor"):
        qmp = QEMUMonitorProtocol(QMP_SOCKET_FILENAME, server=True)
    try:
        with log("Start QEMU"):
            logger.debug(f"Starting subprocess: {qemu_args}")
            process = subprocess.Popen(
                qemu_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
            )
        try:
            with log("Accept connection from QEMU to QMP monitor"):
                qmp.accept()
            try:
                yield qmp
            finally:
                with log("Quit QEMU"):
                    qmp.command("quit")
        finally:
            with log("Close QEMU"):
                alpy.utils.close_verbose_process(
                    process=process, process_name="qemu", timeout=timeout
                )
    finally:
        pathlib.Path(QMP_SOCKET_FILENAME).unlink()


def start_virtual_cpu(qmp):
    log = alpy.utils.context_logger(__name__)
    with log("Start virtual CPU"):
        qmp.command("cont")


def read_events(qmp):
    logger = logging.getLogger(__name__)
    logger.debug("Read QEMU events")
    while qmp.pull_event():
        pass


def wait_shutdown(qmp):

    log = alpy.utils.context_logger(__name__)

    with log("Wait until the VM is powered down"):
        while qmp.pull_event(wait=True)["event"] != "SHUTDOWN":
            pass

    with log("Wait until the VM is stopped"):
        while qmp.pull_event(wait=True)["event"] != "STOP":
            pass


def get_qmp_args():

    return [
        "-chardev",
        "socket,id=id_char_qmp,path=" + QMP_SOCKET_FILENAME,
        "-mon",
        "chardev=id_char_qmp,mode=control",
    ]


def get_network_interface_args(interface_index, interface_name):

    packet_capture_filename = f"link{interface_index}.pcap"
    netdev_id = f"id_net{interface_index}"

    return [
        "-netdev",
        f"tap,id={netdev_id},ifname={interface_name},script=no,downscript=no",
        "-device",
        f"e1000,netdev={netdev_id}",
        "-object",
        f"filter-dump,id=id_dump{interface_index},netdev={netdev_id},file="
        + packet_capture_filename,
    ]


def get_network_interfaces_args(tap_interfaces):

    args = []
    for interface_index, interface_name in enumerate(tap_interfaces):
        args.extend(get_network_interface_args(interface_index, interface_name))
    return args


def get_serial_port_args(tcp_port=alpy.console.PORT):

    return [
        "-chardev",
        f"socket,id=id_char_serial,port={tcp_port},"
        "host=127.0.0.1,ipv4,nodelay,server,nowait,telnet",
        "-serial",
        "chardev:id_char_serial",
    ]


@contextlib.contextmanager
def temporary_copy_ovmf_vars():
    # Make a copy of UEFI firmware variable store from a template.
    shutil.copy("/usr/share/OVMF/OVMF_VARS.fd", OVMF_VARS_COPY_FILENAME)
    yield
    pathlib.Path(OVMF_VARS_COPY_FILENAME).unlink()


def get_uefi_firmware_args():

    args = []

    # firmware executable code
    args.append("-drive")
    args.append(
        "if=pflash,format=raw,unit=0,readonly,file=/usr/share/OVMF/OVMF_CODE.fd"
    )

    # firmware variable store
    args.append("-drive")
    args.append("if=pflash,format=raw,unit=1,file=" + OVMF_VARS_COPY_FILENAME)

    return args
