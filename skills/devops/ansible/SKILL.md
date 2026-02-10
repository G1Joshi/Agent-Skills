---
name: ansible
description: Ansible configuration management with playbooks and roles. Use for server provisioning.
---

# Ansible

Ansible is an agentless automation tool. It handles Configuration Management (installing Nginx, editing configs). 2025 sees the **Automation Platform 2.5** unified UI and AI Lightspeed assistance.

## When to Use

- **Configuration Mgmt**: Terraform creates the VM, Ansible installs the software inside it.
- **Agentless**: No software to install on targets. Needs only SSH.
- **Network Automation**: Configuring Routers/Switches.

## Quick Start

```yaml
# playbook.yml
- name: Configure Webservers
  hosts: web
  become: true
  tasks:
    - name: Install Nginx
      ansible.builtin.apt:
        name: nginx
        state: present

    - name: Start Service
      ansible.builtin.service:
        name: nginx
        state: started
```

## Core Concepts

### Inventory

List of hosts (`hosts.ini` or YAML). Can be dynamic (AWS plugin).

### Playbooks

YAML files defining the desired state.

### Roles / Collections

Reusable units of code. Download from Ansible Galaxy.

## Best Practices (2025)

**Do**:

- **Use Collections**: The modern packaging format. `ansible.builtin` is better than short modules.
- **Use `ansible-lint`**: Enforce best practices.
- **Idempotency**: Ensure running a playbook twice produces the same result without errors.

**Don't**:

- **Don't use `shell` module**: Unless absolutely necessary. Use specific modules (`user`, `file`, `apt`) for key tasks.

## References

- [Ansible Documentation](https://docs.ansible.com/)
