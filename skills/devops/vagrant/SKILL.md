---
name: vagrant
description: Vagrant development environments with VMs. Use for dev environments.
---

# Vagrant

Vagrant provides reproducible, portable development environments using Virtual Machines (VirtualBox, VMWare, Hyper-V).

## When to Use

- **Legacy/Full OS Dev**: You need to simulate a full Linux Kernel or multi-vm network that Docker cannot easily do.
- **Local Testing**: Testing Ansible Playbooks locally on a clean VM.
- **Windows/Mac**: Running Linux VMs on non-Linux hardware with ease.

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

### Boxes

Base images. Analogous to Docker Images. (e.g. `ubuntu/trusty64`).

### Providers

The hypervisor backend. VirtualBox (default), VMWare, Hyper-V, Docker, Libvirt.

### Provisioners

Scripts that run on first boot (Shell, Ansible, Chef) to set up the software.

## Best Practices (2025)

**Do**:

- **Use Multi-Machine**: Simulate a network (DB + Web) in one Vagrantfile.
- **Sync Folders**: Edit code in VS Code on Host, run it on Guest VM.
- **Consider Docker**: For most "App Dev" use cases, Docker/DevContainers are preferred in 2025. Use Vagrant for "Infra Dev".

**Don't**:

- **Don't check in `.vagrant/`**: Add it to `.gitignore`.

## References

- [Vagrant Documentation](https://developer.hashicorp.com/vagrant)
