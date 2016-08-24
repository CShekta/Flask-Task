Vagrant.configure('2') do |config|
  config.vm.hostname = 'FlaskTask'
  config.vm.box = 'ubuntu/trusty64'
  config.ssh.forward_agent = true

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provider 'virtualbox' do |provider, override|
    # Needed to resolve hostnames from VPN DNS (when out
    # of office) on OS X
    provider.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    provider.customize ['modifyvm', :id, '--memory', '1024']
  end

  %w(vmware_fusion vmware_workstation).each do |vmware|
    config.vm.provider vmware do |provider, override|
      provider.name = 'FlaskTask'
      override.vm.box = 'netsensia/ubuntu-trusty64'
    end
  end

  config.vm.provision :shell, path: 'scripts/provision.sh', privileged: false
end
