from __future__ import annotations

import subprocess
import sys
import warnings

import pkg_resources

def get_tag_version() -> str:
    """
    Use git describe to get current version
    """
    cmd = ["git", "describe", "--tags", "--long", "--dirty"]
    try:
        version_bytes = subprocess.check_output(cmd, shell=False).strip()

    except subprocess.CalledProcessError as e:
        version_bytes = bytes("v0.0.0-0-callerror", "ascii")
        cmd_str = " ".join(cmd)
        stdout = e.stdout.decode(sys.getfilesystemencoding()) if e.stdout is not None else ""
        stderr = e.stdout.decode(sys.getfilesystemencoding()) if e.stderr is not None else ""
        warnings.warn(
            f"Process error while getting version out: {stdout}\nErr: {stderr}\nCMD: {cmd_str}",
            category=UserWarning,
        )
    except IOError:
        version_bytes = bytes("v0.0.0-0-gitnotfound","ascii")
        warnings.warn("Git not found", category=UserWarning)
    except Exception as e:
        cmd_str = " ".join(cmd)
        warnings.warn(f"Error while getting version CMD: {cmd_str}", category=UserWarning)
        version_bytes = bytes("v0.0.0-0-unknown", "ascii")


    if isinstance(version_bytes, str):
        version_str = version_bytes
    else:
        version_str = str(version_bytes.decode('ascii'))
    
    if version_str[0] == "v":
        version_str = version_str[1:]

    version_str = version_str.split("-")[0]
    return "%s" % version_str


def get_pkg_version(app_name: str) -> str:
    return pkg_resources.require(app_name)[0].version


def get_version(app_name: str = "face-morphing") -> str:
    try:
        version_str = get_pkg_version(app_name)
        if version_str == "0.0.0":
            version_str = str(get_tag_version)
        return version_str
    except Exception:
        return str(get_tag_version)



