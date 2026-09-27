---
name: vagrant
description: Expert HashiCorp Vagrant assistance covering Vagrantfile configuration, virtualization providers (VirtualBox, Libvirt), and provisioners (Shell, Ansible). Use when automating reproducible local virtual machines.
---

# Vagrant

Vagrant provides reproducible, portable development environments using Virtual Machines (VirtualBox, VMWare, Hyper-V).

## When to Use

- **Local Multi-VM Development Environments**: Creating isolated virtual machines using VirtualBox, VMware, or Libvirt.
- **Testing Infrastructure Playbooks**: Validating Ansible, Chef, and shell provisioning scripts before cloud deployment.
- **Legacy System Emulation**: Simulating specific enterprise Linux OS distributions and kernel versions locally.
- **Cross-Platform Team Alignment**: Providing identical developer VM environments across macOS, Windows, and Linux.

## Quick Start

```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 80, host: 8080

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y apache2
  SHELL
end
```

`vagrant up` -> `vagrant ssh`

## Core Concepts

#Multi-Machine Vagrantfile with Ansible Provisioning

Declaring clustered VM topologies:

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Base box image
  config.vm.box = "bento/ubuntu-24.04"

  # Master Node
  config.vm.define "control-plane" do |master|
    master.vm.hostname = "control-plane.local"
    master.vm.network "private_network", ip: "192.168.56.10"

    master.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.cpus = 2
    end

    master.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbooks/setup_k8s_master.yml"
    end
  end

  # Worker Node
  config.vm.define "worker-01" do |worker|
    worker.vm.hostname = "worker-01.local"
    worker.vm.network "private_network", ip: "192.168.56.11"

    worker.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end
  end

  # Shared folder mapping
  config.vm.synced_folder "./shared", "/mnt/shared", type: "nfs"
end
```

#Essential Vagrant CLI Commands

Managing VM lifecycle:

```bash
# Launch and provision all machines
vagrant up

# SSH into specific defined machine
vagrant ssh control-plane

# Re-run provisioners on active VM
vagrant provision

# Suspend or destroy environment
vagrant suspend
vagrant destroy -f
```

## Common Patterns

### Multi-Machine Cluster with Private Network and Shell Provisioning

**Problem**: Simulating a multi-node cluster locally with hardcoded IPs and dependencies.

**Solution**:
Define multi-machine topology in `Vagrantfile`:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/noble64"

  # Master Node
  config.vm.define "master" do |master|
    master.vm.network "private_network", ip: "192.168.56.10"
    master.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end
  end

  # Worker Node
  config.vm.define "worker" do |worker|
    worker.vm.network "private_network", ip: "192.168.56.11"
    worker.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
  end

  config.vm.provision "shell", inline: "apt-get update && apt-get install -y curl"
end
```

## Best Practices (2026)

- **Do** use official, verified boxes (e.g. `bento/*` or `generic/*`) to ensure clean base operating system states.
- **Do** commit `Vagrantfile` to source control while adding `.vagrant/` to `.gitignore`.
- **Do** use NFS or VirtioFS for synced folders to improve file system I/O performance on macOS and Linux.
- **Do** test provisioning idempotency with `vagrant provision`.
- **Don't** allocate more RAM than available on the host machine; check host resources before launching multi-VM setups.
- **Don't** store credentials or SSH private keys inside synced shared folders.
- **Don't** use Vagrant for production deployments; it is strictly intended for local development and testing.

## Troubleshooting

| Error                                             | Cause                                                                  | Solution                                                          |
| :------------------------------------------------ | :--------------------------------------------------------------------- | :---------------------------------------------------------------- |
| `Timed out while waiting for the machine to boot` | VirtualBox hardware virtualization (VT-x/AMD-V) disabled in BIOS.      | Enable hardware virtualization in host BIOS settings.             |
| `Failed to mount VirtualBox shared folders`       | Guest Additions version mismatch or not installed inside VM.           | Install vagrant plugin: `vagrant plugin install vagrant-vbguest`. |
| `SSH authentication failed for 'vagrant'`         | Corrupted insecure private key in `~/.vagrant.d/insecure_private_key`. | Delete `.vagrant/` directory and recreate with `vagrant up`.      |

## References

- [Vagrant Documentation](https://developer.hashicorp.com/vagrant)
