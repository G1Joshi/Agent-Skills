---
name: ansible
description: Expert Ansible automation assistance covering playbooks, roles, inventory, idempotent modules, and Ansible Vault. Use when automating server configuration, application deployment, and infrastructure orchestration.
---

# Ansible

Ansible is an agentless automation engine for configuration management, infrastructure provisioning, and multi-tier application deployment via declarative YAML playbooks.

## When to Use

- **Agentless Infrastructure Configuration**: Automating multi-node server setup over SSH without installing client daemons.
- **Application Deployment & Provisioning**: Deploying microservices, security patches, and system packages idempotently.
- **Security Hardening & Compliance**: Enforcing CIS benchmarks, firewall rules, and SSH hardening across fleet servers.
- **Orchestration & Rolling Updates**: Coordinating zero-downtime rolling upgrades across clustered backend nodes.

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

### Idempotent Playbook Structure with Handlers

Configuring web servers with automated restart triggers:

```yaml
---
# playbooks/deploy_web.yml
- name: Configure and Harden Nginx Web Nodes
  hosts: webservers
  become: true
  vars:
    nginx_port: 80
    app_root: /var/www/production

  tasks:
    - name: Install Nginx web server
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true

    - name: Deploy hardened Nginx configuration
      ansible.builtin.template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        owner: root
        group: root
        mode: "0644"
      notify: Reload Nginx Service

    - name: Ensure Nginx is enabled and running
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Reload Nginx Service
      ansible.builtin.service:
        name: nginx
        state: reloaded
```

### Dynamic Inventory & Host Grouping

Targeting cloud infrastructure dynamically:

```ini
# inventory/hosts.ini
[webservers]
web-01.infra.internal ansible_host=10.0.1.10
web-02.infra.internal ansible_host=10.0.1.11

[database]
db-primary.infra.internal ansible_host=10.0.2.20

[production:children]
webservers
database

[production:vars]
ansible_user=deploy
ansible_ssh_private_key_file=~/.ssh/prod_deploy.pem
ansible_python_interpreter=/usr/bin/python3
```

### Ansible Vault for Secret Protection

Encrypting credentials and sensitive environment variables:

```bash
# Encrypt sensitive variables file
ansible-vault create vars/vault_secrets.yml

# Execute playbook passing vault password file
ansible-playbook -i inventory/hosts.ini playbooks/deploy_web.yml --vault-password-file ~/.vault_pass
```

## Common Patterns

### Idempotent Nginx Configuration and Service Handler

**Problem**: Applying configuration changes repeatedly without restarting services unless template files changed.

**Solution**:
Use notification handlers triggered by templated tasks:

```yaml
---
- name: Configure Web Servers
  hosts: webservers
  become: true
  tasks:
    - name: Ensure Nginx is installed
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true

    - name: Deploy Nginx site configuration
      ansible.builtin.template:
        src: templates/site.conf.j2
        dest: /etc/nginx/sites-available/default
        mode: "0644"
      notify: Reload Nginx

  handlers:
    - name: Reload Nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded
```

## Best Practices

**Do**:

- Always use fully qualified collection names (FQCN), e.g. `ansible.builtin.template`, `community.docker.docker_container`.
- Verify idempotency by running playbooks twice in CI; the second run must report `changed=0`.
- Store credentials, certificates, and passwords in `ansible-vault` or retrieve from HashiCorp Vault.
- Test roles and playbooks using Molecule and testinfra in automated CI pipelines.

**Don't**:

- Use `ansible.builtin.shell` or `command` when a dedicated idempotent Ansible module exists.
- Commit unencrypted vault passwords or plain text secrets to version control.
- Perform large inventory operations without `--forks` tuned for network concurrency.

## Troubleshooting

| Error                                                                     | Cause                                                             | Solution                                                                    |
| :------------------------------------------------------------------------ | :---------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `Permission denied (publickey)`                                           | SSH key missing, incorrect user, or host key verification failed. | Specify private key via `--private-key` or set `ansible_user` in inventory. |
| `FAILED! => {"changed": false, "msg": "Destination ... is not writable"}` | Task requires root escalation but `become: true` is missing.      | Add `become: true` at playbook or task level.                               |
| `Syntax Error while loading YAML`                                         | Tab characters or improper indentation in YAML playbook.          | Ensure consistent 2-space indentation and run `ansible-lint playbook.yml`.  |

## References

- [Ansible Documentation](https://docs.ansible.com/)
