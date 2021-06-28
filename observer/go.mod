module github.com/ebi/gsoc-2021/observer

go 1.16

replace (
	github.com/Azure/go-autorest => github.com/Azure/go-autorest v12.2.0+incompatible
	github.com/Microsoft/go-winio => github.com/bi-zone/go-winio v0.4.15
	github.com/Shopify/sarama => github.com/elastic/sarama v1.19.1-0.20210120173147-5c8cb347d877
	github.com/cucumber/godog => github.com/cucumber/godog v0.8.1
	github.com/docker/docker => github.com/docker/engine v0.0.0-20191113042239-ea84732a7725
	github.com/docker/go-plugins-helpers => github.com/elastic/go-plugins-helpers v0.0.0-20200207104224-bdf17607b79f
	github.com/dop251/goja => github.com/andrewkroh/goja v0.0.0-20190128172624-dd2ac4456e20
	github.com/dop251/goja_nodejs => github.com/dop251/goja_nodejs v0.0.0-20171011081505-adff31b136e6
	github.com/fsnotify/fsevents => github.com/elastic/fsevents v0.0.0-20181029231046-e1d381a4d270
	github.com/fsnotify/fsnotify => github.com/adriansr/fsnotify v0.0.0-20180417234312-c9bbe1f46f1d
	github.com/google/gopacket => github.com/adriansr/gopacket v1.1.18-0.20200327165309-dd62abfa8a41
	github.com/insomniacslk/dhcp => github.com/elastic/dhcp v0.0.0-20200227161230-57ec251c7eb3 // indirect
	github.com/kardianos/service => github.com/blakerouse/service v1.1.1-0.20200924160513-057808572ffa
	github.com/tonistiigi/fifo => github.com/containerd/fifo v0.0.0-20190816180239-bda0ff6ed73c
	golang.org/x/tools => golang.org/x/tools v0.0.0-20200602230032-c00d67ef29d0 // release 1.14
)

require (
	github.com/akavel/rsrc v0.10.2 // indirect
	github.com/dlclark/regexp2 v1.4.0 // indirect
	github.com/dop251/goja v0.0.0-20210614154742-14a1ffa82844 // indirect
	github.com/dop251/goja_nodejs v0.0.0-20210225215109-d91c329300e7 // indirect
	github.com/elastic/beats/v7 v7.0.0-alpha2.0.20210628135704-1c9a488fbd5a
	github.com/elastic/elastic-agent-client/v7 v7.0.0-20210407144825-cc1c33cfa1d0 // indirect
	github.com/fatih/color v1.12.0 // indirect
	github.com/go-sourcemap/sourcemap v2.1.3+incompatible // indirect
	github.com/gofrs/uuid v4.0.0+incompatible // indirect
	github.com/hashicorp/errwrap v1.1.0 // indirect
	github.com/hashicorp/go-multierror v1.1.1 // indirect
	github.com/josephspurrier/goversioninfo v1.2.0 // indirect
	github.com/magefile/mage v1.11.0
	github.com/mattn/go-isatty v0.0.13 // indirect
	github.com/mitchellh/gox v1.0.1
	github.com/mitchellh/hashstructure v1.1.0 // indirect
	github.com/pierrre/gotestcover v0.0.0-20160517101806-924dca7d15f0
	github.com/poy/eachers v0.0.0-20181020210610-23942921fe77 // indirect
	github.com/prometheus/procfs v0.6.0 // indirect
	github.com/rcrowley/go-metrics v0.0.0-20201227073835-cf1acfcdf475 // indirect
	github.com/tsg/go-daemon v0.0.0-20200207173439-e704b93fd89b
	go.elastic.co/apm v1.12.0 // indirect
	go.elastic.co/ecszap v1.0.0 // indirect
	go.uber.org/atomic v1.8.0 // indirect
	go.uber.org/multierr v1.7.0 // indirect
	go.uber.org/zap v1.17.0 // indirect
	golang.org/x/crypto v0.0.0-20210616213533-5ff15b29337e // indirect
	golang.org/x/lint v0.0.0-20210508222113-6edffad5e616
	golang.org/x/net v0.0.0-20210614182718-04defd469f4e // indirect
	golang.org/x/sys v0.0.0-20210616094352-59db8d763f22 // indirect
	golang.org/x/tools v0.1.4
	google.golang.org/genproto v0.0.0-20210624195500-8bfb893ecb84 // indirect
	google.golang.org/protobuf v1.27.0 // indirect
	gopkg.in/yaml.v2 v2.4.0 // indirect
	gotest.tools/gotestsum v1.6.4
	honnef.co/go/tools v0.2.0 // indirect
	howett.net/plist v0.0.0-20201203080718-1454fab16a06 // indirect
)
