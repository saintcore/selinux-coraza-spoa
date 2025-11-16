# selinux-coraza-spoa

[![build](https://github.com/saintcore/selinux-coraza-spoa/actions/workflows/ci.yml/badge.svg)](https://github.com/saintcore/selinux-coraza-spoa/actions/workflows/ci.yml)
[![changelog](https://github.com/saintcore/selinux-coraza-spoa/actions/workflows/changelog.yml/badge.svg)](https://github.com/saintcore/selinux-coraza-spoa/actions/workflows/changelog.yml)
[![publish](https://github.com/saintcore/selinux-coraza-spoa/actions/workflows/release.yml/badge.svg)](https://github.com/saintcore/selinux-coraza-spoa/actions/workflows/release.yml)

This document details the SELinux policy module for the Coraza Stream Processing Offloader Agent (SPOA), an external agent used by HAProxy for stream data analysis. The coraza-spoa SELinux policy enforces Mandatory Access Control (MAC) for the coraza-spoa daemon. This policy defines and limits the permissions of the service, which runs under the coraza_spoa_t SELinux type.

## Components

| Component | SELinux Type Name | Description | Default Path / Value |
| :--- | :--- | :--- | :--- |
| **Domain** | `coraza_spoa_t` | The SELinux type for the running process. | N/A |
| **Execution** | `coraza_spoa_exec_t` | The file type required to transition to the domain. | `/usr/sbin/coraza-spoa` |
| **Configuration** | `coraza_config_t` | Used for configuration files. | `/etc/coraza-spoa(/.*)?` |
| **Logging** | `coraza_log_t` | Used for logging output. | `/var/log/coraza-spoa(/.*)?` |
| **Port** | `coraza_spoa_port_t` | Defines the TCP port the service listens on. | *Typically* **`tcp 9000`** (Managed by `semanage port`) |

---
## Installation

The SELinux policy requires two steps: installing the RPM package and configuring the SELinux port context. The policy RPM is available in the project's GitHub releases. Use the following command to install the package and define your port:

```bash
# Note: Replace v1.1.0 with your desired version
sudo dnf install -y https://github.com/saintcore/selinux-coraza-spoa/releases/download/v1.1.0/coraza_spoa_selinux-1.1.0-1.el9.noarch.rpm
# Map TCP port 9000 to the policy's defined port type
sudo semanage port -a -t coraza_spoa_port_t -p tcp 9000
```

### Verify Policy Installation

After installation, the policy module should be automatically loaded. You can verify the installation and current status:

```bash
# Check if the policy module is loaded
sudo semodule -l | grep coraza_spoa

# Check the file contexts applied to the service files
sudo ls -Z /usr/sbin/coraza-spoa
sudo ls -Zd /etc/coraza-spoa /var/log/coraza-spoa
```

If contexts are not applied correctly (e.g., after a manual file move or creation), you must relabel the files using the installed contexts:

```bash
sudo restorecon -Rv /etc/coraza-spoa
sudo restorecon -Rv /var/log/coraza-spoa
```

### Custom paths

If you need to place configuration or log files in a non-default location (e.g., `/opt/coraza/`), you must define the new file context mapping using `semanage fcontext` and then apply it.

| File Type | SELinux Type Name |
| :--- | :--- |
| Configuration | `coraza_config_t` |
| Logging | `coraza_log_t` |

**Example: Defining a Custom Configuration Directory**

```bash
# This maps all files under /opt/coraza/conf/ to coraza_config_t
sudo semanage fcontext -a -t coraza_config_t "/opt/coraza/conf(/.*)?"

# Apply the new context to the filesystem
sudo restorecon -Rv /opt/coraza/conf
```

**Example: Defining a Custom Log File Location**

```bash
# This maps all files under /var/log/custom-coraza/ to coraza_log_t
sudo semanage fcontext -a -t coraza_log_t "/var/log/custom-coraza(/.*)?"

# Apply the new context to the filesystem
sudo restorecon -Rv /var/log/custom-coraza
```


### Manpage

Detailed information about the SELinux types, domains, and contexts is available in the manpage file generated for the policy:

```bash
man coraza_spoa_selinux
```

## Troubleshooting

If you encounter SELinux denial errors (AVCs), you can use the following steps to troubleshoot:

- Check for denials: Use ausearch to find recent SELinux denials related to the service.

    ```bash
    sudo ausearch -m AVC -ts recent
    ```

- For debugging purposes only, you can temporarily disable enforcement for the service to see if SELinux is the source of the issue.

    ```bash
    # Set permissive
    sudo semanage permissive -a coraza_spoa_t

    # Re-enable enforcing when finished
    sudo semanage permissive -d coraza_spoa_t
    ```
