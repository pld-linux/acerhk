# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# don't build SMP module

%define _rel		1
%define _orig_name	acerhk

Summary:	Driver for a special Acer Hot Keys.
Summary(pl):	Sterownik obsluguj±cy specjalne klawisze w notebookach Acer.
Name:		kernel-misc-%{_orig_name}
Version:	0.5.18
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.informatik.hu-berlin.de/~tauber/acerhk/archives/%{_orig_name}-%{version}.tgz
# Source0-md5:	2627c1760a1d8e22ad4d4519475cf0c6
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.0}
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
URL:		http://www.informatik.hu-berlin.de/~tauber/acerhk/
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a driver for a special Acer Hot Keys.

%description -l pl
Sterownik pozwalaj±cy uaktywniæ specjalne przyciski w notebookach Acer.

%description -n kernel-misc-%{_orig_name}
This is a driver for a special Acer Hot Keys.

%description -n kernel-misc-%{_orig_name} -l pl
Sterownik pozwalaj±cy uaktywniæ specjalne przyciski w notebookach Acer.

%package -n kernel-smp-misc-%{_orig_name}
Summary:	This is a driver for a special Acer Hot Keys.
Summary(pl):	Sterownik pozwalaj±cy uaktywniæ specjalne przyciski w notebookach Acer.
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-misc-%{_orig_name}
This is a driver for a special Acer Hot Keys.

%description -n kernel-smp-misc-%{_orig_name} -l pl
Sterownik pozwalaj±cy uaktywniæ specjalne przyciski w notebookach Acer.

%prep
%setup -q -n %{_orig_name}-%{version}

%build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
    if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
        exit 1
    fi
    rm -rf include
    install -d include/{linux,config}
    ln -sf %{_kernelsrcdir}/config-$cfg .config
    ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
    ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
    touch include/config/MARKER
    %{__make} -C %{_kernelsrcdir} clean modules \
    EXTRA_CFLAGS="-I../include -DFUSE_VERSION='1.1'" \
    RCS_FIND_IGNORE="-name '*.ko' -o" \
    M=$PWD O=$PWD \
    %{?with_verbose:V=1}
    mv %{_orig_name}.ko %{_orig_name}-$cfg.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install %{_orig_name}-up.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.ko
install %{_orig_name}-smp.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.ko

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-%{_orig_name}
%depmod %{_kernel_ver}

%postun	-n kernel-misc-%{_orig_name}
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-%{_orig_name}
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-misc-%{_orig_name}
%depmod %{_kernel_ver}smp

%files -n kernel-misc-%{_orig_name}
%defattr(644,root,root,755)
%doc NEWS INSTALL README doc/*
/lib/modules/%{_kernel_ver}/misc/*.ko*

%files -n kernel-smp-misc-%{_orig_name}
%defattr(644,root,root,755)
%doc NEWS INSTALL README doc/*
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
