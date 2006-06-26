#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# don't build SMP module
#
%define _rel		1
%define _orig_name	acerhk

Summary:	Linux driver for Acer notebook special Hot Keys
Summary(pl):	Sterownik dla Linuksa obsługujący specjalne klawisze w notebookach Acer
Name:		kernel-misc-%{_orig_name}
Version:	0.5.33
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.informatik.hu-berlin.de/~tauber/acerhk/archives/%{_orig_name}-%{version}.tgz
# Source0-md5:	51221e791dc5c3dccd4d9c9fd42cb249
URL:		http://www.informatik.hu-berlin.de/~tauber/acerhk/
BuildRequires:	%{kgcc_package}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.0}
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for Acer notebook special Hot Keys.

%description -l pl
Sterownik dla Linuksa pozwalający uaktywnić specjalne przyciski w
notebookach Acer.

%package -n kernel-smp-misc-%{_orig_name}
Summary:	This is a Linux SMP driver for special Acer Hot Keys
Summary(pl):	Sterownik dla Linuksa SMP obsługujący specjalne przyciski w notebookach Acer
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-misc-%{_orig_name}
This is a Linux SMP driver for Acer notebook special Hot Keys.

%description -n kernel-smp-misc-%{_orig_name} -l pl
Sterownik dla Linuksa SMP pozwalający uaktywnić specjalne przyciski w
notebookach Acer.

%prep
%setup -q -n %{_orig_name}-%{version}

%build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o -name nv-kernel.o -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	mv %{_orig_name}.ko %{_orig_name}-$cfg.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install %{_orig_name}-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.ko
%if %{with smp} && %{with dist_kernel}
install %{_orig_name}-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.ko
%endif

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

%files
%defattr(644,root,root,755)
%doc NEWS INSTALL README doc/*
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp}
%files -n kernel-smp-misc-%{_orig_name}
%defattr(644,root,root,755)
%doc NEWS INSTALL README doc/*
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
